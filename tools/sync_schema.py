"""Sync every form's ``schema.json`` to cover all of its ``mapping.json`` keys.

The mapping is the authoritative, verified artifact; the JSON Schema describes
the case data the mapping consumes. This walks each mapping field and ensures
the schema has a matching path, inferring the leaf type from the field's
``field_type``:

    text / enum_text_select -> string
    checkbox                -> boolean
    enum_select / radio     -> string with an ``enum`` of the option keys

Path segments like ``parties[0]`` become an ``array`` of objects (every index
shares one item schema); plain segments become nested objects. It is additive
and idempotent for leaves (an existing leaf is never retyped), and it upgrades a
wrong-typed *intermediate* (e.g. a ``string`` where the mapping needs nested
keys) to the object/array it must be. This subsumes the older cover-block fix.

It also **repairs generator artifacts**: an earlier schema generation leaked
index/placeholder notation into literal property names (``"parties[0]"``,
``"class_changes[N]"``, ``"line{1,2}"``, ``"{street,city,county}"``,
``"officer_<role>"``). Such properties are not addressable by
``engine.canonical`` dotted paths and shadow the real array/sibling
properties. The cleanup migrates their descriptions onto the real properties
(filling gaps only — nothing existing is overwritten) and removes the
artifact, and it retypes the one known bad inference (``county`` typed
``integer`` because "count" substring-matched inside "county"; see the
fixed heuristic in ``tools/build_from_pass1.py``).

    python3 tools/sync_schema.py            # all forms
    python3 tools/sync_schema.py CORP_MBCA-10 LLC_MLLC-10
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.mapping import entries as mapping_entries  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "forms"
_ARRAY_SEG = re.compile(r"^(.+?)\[\d+\]$")
_ARTIFACT = re.compile(r"[\[\]{}<>]")
_ARRAY_LITERAL = re.compile(r"^(\w+)\[(?:\d+|N|\*)\]$")
_BRACE_GROUP = re.compile(r"^(\w*)\{([\w\s,]+)\}(\w*)$")


def _leaf(spec):
    ft = spec.get("field_type")
    if ft == "checkbox":
        node = {"type": "boolean"}
    elif ft in ("enum_select", "radio"):
        node = {"type": "string"}
        opts = spec.get("options")
        if isinstance(opts, dict) and opts:
            node["enum"] = sorted(opts)
    else:  # text, enum_text_select, anything else
        node = {"type": "string"}
    label = spec.get("label")
    if label:
        node["description"] = label
    return node


def _ensure(node, segments, leaf, changed):
    """Ensure ``segments`` resolves under object-schema ``node``; return changed."""
    seg = segments[0]
    m = _ARRAY_SEG.match(seg)
    is_array = bool(m)
    name = m.group(1) if m else seg
    props = node.setdefault("properties", {})

    if len(segments) == 1 and not is_array:
        if name not in props:
            props[name] = leaf
            changed[0] = True
        return

    child = props.get(name)
    if is_array:
        if not (isinstance(child, dict) and child.get("type") == "array"):
            child = {"type": "array", "items": {"type": "object", "properties": {}}}
            props[name] = child
            changed[0] = True
        items = child.setdefault("items", {})
        if items.get("type") != "object":
            child["items"] = {"type": "object", "properties": {}}
            items = child["items"]
            changed[0] = True
        if len(segments) > 1:
            _ensure(items, segments[1:], leaf, changed)
    else:
        if not (isinstance(child, dict) and child.get("type") == "object"):
            child = {"type": "object", "properties": {}}
            props[name] = child
            changed[0] = True
        _ensure(child, segments[1:], leaf, changed)


def _merge_into(src, dst, changed):
    """Copy ``src`` schema-node content into ``dst``, filling gaps only.

    Missing descriptions and missing (sub)properties are added; existing
    types, enums, and descriptions are never overwritten.
    """
    if not isinstance(src, dict) or not isinstance(dst, dict):
        return
    if src.get("description") and not dst.get("description"):
        dst["description"] = src["description"]
        changed[0] = True
    if isinstance(src.get("items"), dict) and isinstance(dst.get("items"),
                                                         dict):
        _merge_into(src["items"], dst["items"], changed)
    src_props = src.get("properties")
    if not isinstance(src_props, dict):
        return
    dst_props = dst.setdefault("properties", {})
    for k, v in src_props.items():
        if _ARTIFACT.search(k):
            continue  # never copy an artifact name forward
        if k in dst_props:
            _merge_into(v, dst_props[k], changed)
        else:
            dst_props[k] = v
            changed[0] = True


def _artifact_targets(name, props, changed):
    """Real sibling properties an artifact-named property describes.

    Missing counterparts are created (the artifact is the only carrier of
    that part of the data model) so its content is migrated, not dropped.
    """
    m = _ARRAY_LITERAL.match(name)
    if m:
        base = m.group(1)
        node = props.get(base)
        if not (isinstance(node, dict) and node.get("type") == "array"):
            node = {"type": "array",
                    "items": {"type": "object", "properties": {}}}
            props[base] = node
            changed[0] = True
        items = node.setdefault("items", {"type": "object",
                                          "properties": {}})
        return [items]
    m = _BRACE_GROUP.match(name)
    if m and "{" not in m.group(2):
        prefix, parts, suffix = m.group(1), m.group(2), m.group(3)
        names = [f"{prefix}{p.strip()}{suffix}" for p in parts.split(",")
                 if p.strip()]
        src_type = (props[name].get("type", "string")
                    if isinstance(props.get(name), dict) else "string")
        targets = []
        for n in names:
            if n not in props:
                props[n] = ({"type": "object", "properties": {}}
                            if src_type == "object"
                            else {"type": src_type})
                changed[0] = True
            targets.append(props[n])
        return targets
    # fuzzy placeholder ("line{N}", "officer_<role>", "director_N",
    # malformed nested braces): siblings sharing the literal prefix
    prefix = re.split(r"[\[\]{}<>]", name)[0].rstrip("._")
    if prefix:
        return [v for k, v in props.items()
                if k != name and not _ARTIFACT.search(k)
                and k.startswith(prefix)]
    return []


def _clean_artifacts(node, changed):
    """Remove placeholder-named properties after migrating their content.

    Depth-first: an artifact's own subtree is cleaned before it is merged,
    so nested artifacts (``parties[N].signature_block.signer_{1,2}``) are
    resolved inside the subtree and nothing is dropped.
    """
    props = node.get("properties")
    if isinstance(props, dict):
        for v in list(props.values()):
            if isinstance(v, dict):
                _clean_artifacts(v, changed)
        for name in [k for k in props if _ARTIFACT.search(k)]:
            src = props[name]
            for target in _artifact_targets(name, props, changed):
                _merge_into(src, target, changed)
            del props[name]
            changed[0] = True
    items = node.get("items")
    if isinstance(items, dict):
        _clean_artifacts(items, changed)


def _fix_county_type(node, changed):
    """Retype ``county`` leaves wrongly inferred as integer (substring bug)."""
    props = node.get("properties")
    if isinstance(props, dict):
        for k, v in props.items():
            if not isinstance(v, dict):
                continue
            if k == "county" and v.get("type") == "integer":
                v["type"] = "string"
                changed[0] = True
            _fix_county_type(v, changed)
    items = node.get("items")
    if isinstance(items, dict):
        _fix_county_type(items, changed)


def sync_one(form_dir):
    schema_path = form_dir / "schema.json"
    mapping = json.loads((form_dir / "mapping.json").read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if schema.get("type") != "object":
        return False
    changed = [False]
    _clean_artifacts(schema, changed)
    _fix_county_type(schema, changed)
    for key, spec in mapping_entries(mapping).items():
        if not isinstance(spec, dict):
            continue
        # An entry may resolve a different canonical key than its dict key
        # (two when-gated entries feeding one key; see engine.fill docstring).
        key = spec.get("canonical_key", key)
        _ensure(schema, key.split("."), _leaf(spec), changed)
    if changed[0]:
        schema_path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    return changed[0]


def main(argv):
    targets = argv[1:] or sorted(d.name for d in ROOT.iterdir() if d.is_dir())
    changed = 0
    for fid in targets:
        d = ROOT / fid
        if not (d / "schema.json").exists():
            continue
        if sync_one(d):
            changed += 1
            print(f"synced {fid}")
    print(f"\n{changed} schema(s) updated; {len(targets) - changed} already in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
