"""Regenerate a form's ``fields.csv`` widget inventory from its live blank PDF.

``fields.csv`` is a flat, human-readable inventory of every AcroForm widget. For
forms the state revised after the original capture, the committed inventory can
list the old widget names while ``mapping.json`` (re-bound and verified against
the current blank) is correct. This rebuilds the inventory from the live PDF so
the two agree again.

The blank must be on disk (``python3 tools/fetch_pdfs.py --forms <ID>``). Source
precedence per row: ``widget_id`` / ``page`` / ``field_type`` come from the live
PDF; ``canonical_key`` / ``confidence`` / label come from the current mapping
where the widget is mapped; the original ``rationale`` (and label, for unmapped
widgets) is carried over for widgets that still exist.

    python3 tools/rebuild_fields_csv.py CORP_ASUM-5 MARK_mark2
    python3 tools/rebuild_fields_csv.py --forms-file /tmp/lagging_forms.txt
"""
import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.mapping import entries as mapping_entries  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "forms"
COLUMNS = ["widget_id", "page", "field_type", "label_verbatim",
           "canonical_key", "confidence", "rationale"]
_TYPE = {"Text": "text", "CheckBox": "checkbox", "RadioButton": "radio",
         "ComboBox": "combobox", "ListBox": "listbox", "Signature": "signature"}


def _mapping_index(form_dir):
    """widget_id (base, no __pN) -> {keys:[..], confidence, label}."""
    mapping = json.loads((form_dir / "mapping.json").read_text(encoding="utf-8"))
    idx = {}
    for key, spec in mapping_entries(mapping).items():
        if not isinstance(spec, dict):
            continue
        wid = spec.get("widget_id")
        refs = list(wid if isinstance(wid, list) else ([wid] if wid else []))
        # enum_select / enum_text_select bind through options (no widget_id);
        # radio options are on-states, not widgets.
        opts = spec.get("options")
        if isinstance(opts, dict) and not wid:
            refs.extend(opts.values())
        for w in refs:
            base = re.sub(r"__p\d+$", "", str(w))
            e = idx.setdefault(base, {"keys": [], "confidence": "", "label": ""})
            e["keys"].append(key)
            e["confidence"] = spec.get("confidence", e["confidence"])
            e["label"] = e["label"] or spec.get("label", "")
    return idx


def _old_rows(form_dir):
    fc = form_dir / "fields.csv"
    rows = {}
    if fc.exists():
        with open(fc, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("widget_id"):
                    rows[r["widget_id"]] = r
    return rows


def _live_widgets(form_dir, fid):
    pdf = form_dir / f"{fid}.pdf"
    if not pdf.exists():
        raise FileNotFoundError(f"{pdf} not on disk; run tools/fetch_pdfs.py --forms {fid}")
    doc = fitz.open(pdf)
    seen, out = set(), []
    for pno in range(doc.page_count):
        for w in doc[pno].widgets() or []:
            name = w.field_name
            if not name or name in seen:
                continue
            seen.add(name)
            out.append((name, pno, _TYPE.get(w.field_type_string, "text")))
    doc.close()
    return out


def rebuild_one(fid):
    d = ROOT / fid
    idx = _mapping_index(d)
    old = _old_rows(d)
    rows = []
    for name, page, ftype in _live_widgets(d, fid):
        m = idx.get(name)
        prev = old.get(name, {})
        if m:
            label = m["label"] or prev.get("label_verbatim", "") or name
            ckey = "; ".join(dict.fromkeys(m["keys"]))
            conf = m["confidence"]
            rationale = prev.get("rationale") or "Mapped widget (live blank)."
        else:
            label = prev.get("label_verbatim", "") or name
            ckey = ""
            conf = ""
            rationale = prev.get("rationale") or "Unmapped widget (live blank)."
        rows.append({"widget_id": name, "page": page, "field_type": ftype,
                     "label_verbatim": label, "canonical_key": ckey,
                     "confidence": conf, "rationale": rationale})

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS)
    w.writeheader()
    w.writerows(rows)
    text = buf.getvalue()
    path = d / "fields.csv"
    if path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
        return len(rows)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("forms", nargs="*")
    ap.add_argument("--forms-file", help="file with one form id per line")
    args = ap.parse_args(argv)
    targets = list(args.forms)
    if args.forms_file:
        targets += Path(args.forms_file).read_text().split()
    if not targets:
        ap.error("name at least one form id, or pass --forms-file")
    changed = 0
    for fid in targets:
        n = rebuild_one(fid)
        if n:
            changed += 1
            print(f"rebuilt {fid}: {n} widgets")
        else:
            print(f"unchanged {fid}")
    print(f"\n{changed} fields.csv rewritten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
