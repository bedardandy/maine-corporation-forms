"""Generate diverse synthetic cases for a form.

Strategy (matches the project's division of labor):

* A **deterministic** builder assigns synthetic identities and schema-valid
  values to every mapped canonical key, so the loop runs fully offline and never
  depends on -- or leaks -- real data.
* **Qwen** optionally enriches form-specific fields (enums, booleans, counts) for
  diversity. Because Qwen paraphrases enum tokens and invents names, its output
  is *canonicalized against the schema* and only non-identity fields are merged.

Each form yields a handful of named variants: ``typical``, ``minimal``,
``overflow`` (forces a continuation schedule), and ``signer_bad`` (an
out-of-capacity signer, to prove the signer-rule gate fires).
"""

from __future__ import annotations

import json
from pathlib import Path

from . import synthetic as syn
from .. import signer_rules
from engine.mapping import entries as mapping_entries


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _load(form_id: str):
    fd = _repo_root() / "forms" / form_id
    mapping = json.loads((fd / "mapping.json").read_text())
    schema = json.loads((fd / "schema.json").read_text())
    meta = {}
    try:
        import yaml

        meta = yaml.safe_load((fd / "form.yaml").read_text()) or {}
    except Exception:
        pass
    return mapping, schema, meta


def _schema_node(schema: dict, dotted: str):
    node = schema
    for part in dotted.split("."):
        if part.isdigit():
            node = (node or {}).get("items", {}) if isinstance(node, dict) else {}
            continue
        props = node.get("properties") if isinstance(node, dict) else None
        if not isinstance(props, dict) or part not in props:
            return {}
        node = props[part]
    return node if isinstance(node, dict) else {}


def _set_dotted(case: dict, dotted: str, value) -> None:
    parts = dotted.split(".")
    cur = case
    for i, p in enumerate(parts):
        last = i == len(parts) - 1
        if p.isdigit():
            idx = int(p)
            if not isinstance(cur, list):
                return
            while len(cur) <= idx:
                cur.append({})
            if last:
                cur[idx] = value
            else:
                cur = cur[idx]
            continue
        if last:
            cur[p] = value
        else:
            nxt = parts[i + 1]
            if nxt.isdigit():
                cur = cur.setdefault(p, [])
            else:
                cur = cur.setdefault(p, {})


def _value_for_key(key: str, node: dict, seed: int):
    """Pick a synthetic, schema-valid value for one canonical key."""
    kl = key.lower()
    typ = (node.get("type") if isinstance(node, dict) else None) or ""
    enum = node.get("enum") if isinstance(node, dict) else None

    if enum:
        return enum[seed % len(enum)]
    if typ == "boolean":
        return (seed % 2) == 0
    if typ == "integer" or kl.endswith("_count") or kl.endswith("count"):
        return 1 + (seed % 3)

    if kl.endswith("cra_public_number"):
        return syn.cra_number(seed)
    if "email" in kl:
        return f"contact{seed % 97}@example.com"
    if "phone" in kl:
        return f"207-555-{1000 + (seed % 9000):04d}"
    if kl.endswith("date") or "date_signed" in kl:
        return "2026-05-30"
    if "agent" in kl and kl.endswith("name"):
        return syn.agent(seed)
    if "clerk" in kl and kl.endswith("name"):
        return syn.agent(seed)
    if kl.endswith("printed_name_and_title"):
        return f"{syn.person(seed)}, Authorized Person"
    if kl.endswith("printed_name_and_capacity"):
        return f"{syn.person(seed)}, General Partner"
    if kl.endswith("printed_name") or (
        kl.endswith(".name")
        and key.split(".")[0]
        in ("incorporator_1", "signer", "officer", "member", "manager", "partner")
    ):
        return syn.person(seed)
    if "address" in kl or kl.endswith("line1"):
        return syn.address(seed)["line1"]
    if kl.endswith(".city"):
        return syn.address(seed)["city"]
    if kl.endswith(".state"):
        return "ME"
    if kl.endswith(".zip"):
        return syn.address(seed)["zip"]

    return None


def base_case(form_id: str, seed: int = 1) -> dict:
    mapping, schema, _meta = _load(form_id)
    prefix = form_id.split("_", 1)[0].upper()
    case: dict = {}

    _set_dotted(case, "entity.name", syn.entity_name(prefix, seed))

    for key in mapping_entries(mapping):
        if key == "entity.name":
            continue
        node = _schema_node(schema, key)
        val = _value_for_key(key, node, seed)
        if val is not None:
            _set_dotted(case, key, val)

    rules = signer_rules.rules_for(form_id)
    allowed = rules["allowed_signer_capacities"]
    case["signature"] = {
        "printed_name": syn.person(seed + 5),
        "capacity": allowed[0] if allowed else "authorized person",
        "date": "2026-05-30",
    }
    return case


def variants(form_id: str, seed: int = 1) -> dict:
    """Return {variant_name: case} covering typical / minimal / overflow / signer_bad."""
    typical = base_case(form_id, seed)

    minimal = {"entity": {"name": typical.get("entity", {}).get("name", "")}}

    overflow = json.loads(json.dumps(typical))
    overflow.setdefault("entity", {})["name"] = syn.long_purpose(seed)
    mapping, _, _ = _load(form_id)
    for key in mapping_entries(mapping):
        if "purpose" in key.lower() or "description" in key.lower():
            _set_dotted(overflow, key, syn.long_purpose(seed + 2))

    signer_bad = json.loads(json.dumps(typical))
    rules = signer_rules.rules_for(form_id)
    allowed = {c.lower() for c in rules["allowed_signer_capacities"]}
    bad = next(
        (c for c in ["general partner", "officer", "member", "applicant", "partner",
                     "notary public"] if c not in allowed),
        "notary public",
    )
    signer_bad["signature"]["capacity"] = bad

    return {
        "typical": typical,
        "minimal": minimal,
        "overflow": overflow,
        "signer_bad": signer_bad,
    }


_ENRICH_SYS = (
    "You generate realistic but fictional test data for a U.S. state business "
    "filing form. Output ONLY a JSON object of field_path -> value for the "
    "requested non-identity fields. Use only the allowed enum values given. Do "
    "not invent person or company names."
)


def enrich_with_qwen(form_id: str, case: dict) -> dict:
    """Ask Qwen to diversify enum/boolean fields; canonicalize against schema."""
    from . import llm

    if not llm.qwen_available():
        return case
    mapping, schema, _ = _load(form_id)
    asks = {}
    for key in mapping_entries(mapping):
        node = _schema_node(schema, key)
        enum = node.get("enum") if isinstance(node, dict) else None
        if enum:
            asks[key] = {"enum": enum}
        elif (node.get("type") if isinstance(node, dict) else None) == "boolean":
            asks[key] = {"type": "boolean"}
    if not asks:
        return case
    user = json.dumps({"form": form_id, "fields": asks})
    try:
        raw = llm.qwen_chat(_ENRICH_SYS, user, max_tokens=1024)
        proposed = llm.extract_json(raw) or {}
    except Exception:
        return case
    for key, val in proposed.items():
        if key not in asks:
            continue
        spec = asks[key]
        if "enum" in spec and val in spec["enum"]:
            _set_dotted(case, key, val)
        elif spec.get("type") == "boolean" and isinstance(val, bool):
            _set_dotted(case, key, val)
    return case


def generate(form_id: str, seed: int = 1, use_qwen: bool = False) -> dict:
    vs = variants(form_id, seed)
    if use_qwen:
        for name, case in vs.items():
            if name in ("typical", "overflow"):
                vs[name] = enrich_with_qwen(form_id, case)
    return vs
