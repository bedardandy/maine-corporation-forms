"""Geometry-verified widget inspection for enum/checkbox mapping repair.

The audit's adversarial vision pass found the dominant risk in fixing enum
fields: mapping.json lists widget ids, but binding ``enum[i] -> widget_id[i]`` by
list order silently marks the WRONG box when the PDF stores widgets in a
different order than the enum (observed on CORP_MBCA-2 — ``Check Box8`` before
``Check Box1`` — and CORP_REVIVAL — column-major A,C,B,D). Marking the wrong box
certifies a false legal fact (wrong revoking authority, wrong fee tier, wrong
required signer).

This module reads the *actual* AcroForm so a fix can bind by verified geometry
(rect position) and by each widget's real ``/AP`` on-state name — never by list
order, never assuming the on-state is ``'Yes'`` or the enum token.

Read-only: it never modifies a PDF. ``probe_field`` returns, for one field's
widget list, each widget's type, rect, reading-order rank, and on-states.
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover - import guard
    raise ImportError(
        "tools.widget_probe requires PyMuPDF (fitz)."
    ) from exc


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _form_pdf(form_id: str, forms_root: str) -> Path:
    root = Path(forms_root)
    if not root.is_absolute():
        root = _repo_root() / forms_root
    return root / form_id / f"{form_id}.pdf"


def _on_states(widget) -> list:
    """Non-Off appearance-state names for a button widget (the value to write)."""
    states = []
    try:
        bs = widget.button_states() or {}
    except Exception:
        return states
    for group in bs.values():
        for s in group:
            if s and s != "Off" and s not in states:
                states.append(s)
    return states


def probe_widgets(form_id: str, forms_root: str = "forms") -> list:
    """Every widget in the form with type, rect, page, and on-states."""
    pdf = _form_pdf(form_id, forms_root)
    doc = fitz.open(str(pdf))
    out = []
    try:
        for pno in range(doc.page_count):
            for w in doc[pno].widgets() or []:
                r = w.rect
                out.append(
                    {
                        "name": w.field_name or "",
                        "type": w.field_type_string,
                        "page": pno,
                        "rect": [round(r.x0, 1), round(r.y0, 1), round(r.x1, 1), round(r.y1, 1)],
                        "on_states": _on_states(w),
                    }
                )
    finally:
        doc.close()
    return out


def probe_field(form_id: str, widget_ids, forms_root: str = "forms") -> dict:
    """Resolve a mapping field's widget list to verified per-widget geometry.

    Returns the widgets in the field's listed order AND in reading order
    (top-to-bottom, then left-to-right), so a caller can see whether list order
    matches visual order before binding enum values.
    """
    names = widget_ids if isinstance(widget_ids, list) else [widget_ids]
    allw = {w["name"]: w for w in probe_widgets(form_id, forms_root)}
    listed = []
    for n in names:
        w = allw.get(n)
        listed.append(w if w else {"name": n, "type": "MISSING", "rect": None, "on_states": []})

    def _key(w):
        r = w.get("rect")
        if not r:
            return (9999, 9999, 9999)
        return (w.get("page", 0), round(r[1]), round(r[0]))  # page, y, x

    present = [w for w in listed if w.get("rect")]
    reading_order = sorted(present, key=_key)
    list_order_names = [w["name"] for w in listed]
    reading_order_names = [w["name"] for w in reading_order]

    return {
        "form_id": form_id,
        "widget_ids": names,
        "all_present": all(w.get("type") != "MISSING" for w in listed),
        "all_buttons": all(w.get("type") in ("CheckBox", "RadioButton") for w in present),
        "any_text": any(w.get("type") == "Text" for w in present),
        "list_order_matches_reading_order": list_order_names == reading_order_names,
        "widgets_in_list_order": listed,
        "widgets_in_reading_order": reading_order,
    }


def probe_mapping_field(form_id: str, key: str, forms_root: str = "forms") -> dict:
    """Probe one canonical key from a form's mapping.json."""
    root = Path(forms_root)
    if not root.is_absolute():
        root = _repo_root() / forms_root
    mapping = json.loads((root / form_id / "mapping.json").read_text())
    import sys
    repo = str(_repo_root())
    if repo not in sys.path:
        sys.path.insert(0, repo)
    from engine.mapping import entries as mapping_entries
    spec = mapping_entries(mapping).get(key)
    if not spec:
        return {"error": f"{key} not in {form_id} mapping"}
    res = probe_field(form_id, spec.get("widget_id"), forms_root)
    res["key"] = key
    res["mapped_field_type"] = spec.get("field_type")
    return res


def _main(argv) -> int:
    if len(argv) >= 2:
        print(json.dumps(probe_mapping_field(argv[0], argv[1]), indent=2), flush=True)
        return 0
    if len(argv) == 1:
        print(json.dumps(probe_widgets(argv[0]), indent=2), flush=True)
        return 0
    print("usage: python3 -m tools.widget_probe <FORM_ID> [canonical.key]", flush=True)
    return 2


if __name__ == "__main__":
    import sys

    raise SystemExit(_main(sys.argv[1:]))
