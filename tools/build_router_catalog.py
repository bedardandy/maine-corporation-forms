#!/usr/bin/env python3
"""Build the compact router catalog from the form index.

The router (``tools/route_form.py``) sends this catalog to an LLM in one prompt,
so it must stay small. Each entry is ``{form_id, title, hints}`` where ``hints``
are short, factual disambiguators derived from the form's own metadata
(entity type, category, statute) — never invented prose. With ~156 forms the
whole catalog is a few thousand tokens, well under a single context.

    python3 tools/build_router_catalog.py            # write catalog/router_catalog.json
    python3 tools/build_router_catalog.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Readable labels for the entity-type prefix; factual, not editorial.
_ENTITY_LABEL = {
    "business_corporation": "business corporation (13-C)",
    "nonprofit_corporation": "nonprofit corporation (13-B)",
    "limited_liability_company": "LLC (Title 31)",
    "limited_partnership": "limited partnership",
    "limited_liability_partnership": "LLP",
    "general_partnership": "general partnership",
    "trademark": "trademark / service mark",
}


def _hints(form):
    hints = []
    ent = form.get("entity_type")
    if ent:
        hints.append(_ENTITY_LABEL.get(ent, ent.replace("_", " ")))
    cat = form.get("category")
    if cat and cat not in ("?", "", None):
        hints.append(cat.replace("_", " "))
    code = form.get("code")
    if code:
        hints.append(f"form {code}")
    return hints


def build():
    idx = json.loads((ROOT / "catalog" / "forms_index.json").read_text())
    forms = idx.get("forms", idx) if isinstance(idx, dict) else idx
    catalog = []
    for f in forms:
        catalog.append({
            "form_id": f["form_id"],
            "title": f.get("title", f["form_id"]),
            "hints": _hints(f),
        })
    return {"forms": catalog}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    catalog = build()
    out = ROOT / "catalog" / "router_catalog.json"
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    if a.dry_run:
        print(f"{len(catalog['forms'])} forms; "
              f"~{len(text) // 4} tokens (rough)")
        return 0
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out} ({len(catalog['forms'])} forms)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
