"""Normalize the shared cover/transmittal block in every form's ``schema.json``.

The Maine SoS forms share a cover block (expedited-service options, the entity
name(s) the filing covers, a contact, fees). When that block was unified across
all 156 mappings, two ``schema.json`` shapes were left behind that no longer
match the verified ``mapping.json``:

- ``filing.expedited_service`` typed as a ``string`` (the old single-value
  model) where the mapping now uses three independent boolean checkboxes
  (``hold_for_pickup`` / ``expedite_24h`` / ``immediate``).
- the cover entity name(s) emitted as literal ``entities[0]`` / ``entities[1]``
  object properties instead of a single ``entities`` array.

This rewrites only those two keys, and only for forms whose mapping actually
uses them, leaving every other ``filing.*`` property untouched. It is
idempotent: a normalized schema is left unchanged.

    python3 tools/normalize_cover_schema.py            # all forms
    python3 tools/normalize_cover_schema.py CORP_MBCA-6 LLC_MLLC-6
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "forms"

EXPEDITED_SCHEMA = {
    "type": "object",
    "description": "Cover-letter expedited-service options (independent checkboxes).",
    "properties": {
        "hold_for_pickup": {"type": "boolean"},
        "expedite_24h": {"type": "boolean"},
        "immediate": {"type": "boolean"},
    },
}

ENTITIES_SCHEMA = {
    "type": "array",
    "description": "Entity name(s) the filing covers, as listed on the cover block.",
    "items": {"type": "object", "properties": {"name": {"type": "string"}}},
}


def _mapping_keys(form_dir):
    mapping = json.loads((form_dir / "mapping.json").read_text(encoding="utf-8"))
    return set((mapping.get("fields") or {}).keys())


def normalize_one(form_dir):
    schema_path = form_dir / "schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    keys = _mapping_keys(form_dir)

    filing = schema.get("properties", {}).get("filing")
    if not isinstance(filing, dict) or "properties" not in filing:
        return False
    props = filing["properties"]
    changed = False

    uses_expedited = any(k.startswith("filing.expedited_service.") for k in keys)
    if uses_expedited and props.get("expedited_service") != EXPEDITED_SCHEMA:
        props["expedited_service"] = dict(EXPEDITED_SCHEMA)
        changed = True

    uses_entities = any(k.startswith("filing.entities[") for k in keys)
    if uses_entities:
        # drop any literal entities[N] properties; install one array property.
        literals = [p for p in props if re.fullmatch(r"entities\[\d+\]", p)]
        if literals or props.get("entities") != ENTITIES_SCHEMA:
            for p in literals:
                del props[p]
            props["entities"] = dict(ENTITIES_SCHEMA)
            changed = True

    if changed:
        schema_path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    return changed


def main(argv):
    targets = argv[1:] or sorted(d.name for d in ROOT.iterdir() if d.is_dir())
    changed = 0
    for fid in targets:
        d = ROOT / fid
        if not (d / "schema.json").exists():
            print(f"skip {fid}: no schema.json")
            continue
        if normalize_one(d):
            changed += 1
            print(f"normalized {fid}")
    print(f"\n{changed} schema(s) updated; {len(targets) - changed} already normal.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
