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

    python3 tools/sync_schema.py            # all forms
    python3 tools/sync_schema.py CORP_MBCA-10 LLC_MLLC-10
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "forms"
_ARRAY_SEG = re.compile(r"^(.+?)\[\d+\]$")


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


def sync_one(form_dir):
    schema_path = form_dir / "schema.json"
    mapping = json.loads((form_dir / "mapping.json").read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if schema.get("type") != "object":
        return False
    changed = [False]
    for key, spec in (mapping.get("fields") or {}).items():
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
