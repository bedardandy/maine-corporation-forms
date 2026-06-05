#!/usr/bin/env python3
"""Deterministic PDF/UA-oriented remediation for a Maine SoS AcroForm.

Sets the two things every accessible form PDF needs that we *can* set with no
authoring tool and no guessing, sourced from the shipped per-form contract:

  1. **Field tooltips** (``/TU``) — a screen reader announces a field's ``/TU``
     string. We set it from each field's human ``label`` in ``mapping.json`` (the
     canonical key as a fallback), so every widget speaks. For a field whose
     ``widget_id`` is a list (one value across several widgets) or a split shared
     checkbox, every underlying widget gets the tooltip.
  2. **Document metadata** — ``/Lang`` (reader voice), the document ``/Title``
     (from ``form.yaml``) + ``DisplayDocTitle`` true (title bar shows the form
     name, not the filename).

What we do NOT do: fabricate a structure tree (tags). A correct StructTreeRoot
for an arbitrary form needs layout understanding we don't have here, and faking
``/MarkInfo /Marked true`` without real tags fails PDF/UA worse than honest
absence — so we never set it. That step needs Acrobat / an auto-tagger.

    python3 tools/accessibility/remediate_form.py CORP_MBCA-6 --out out.pdf
    python3 tools/accessibility/remediate_form.py path/to/filled.pdf \
        --mapping forms/CORP_MBCA-6/mapping.json --title "Articles..." --out out.pdf
"""
from __future__ import annotations

import argparse
import json
import pathlib

import pypdf
from pypdf.generic import BooleanObject, NameObject, TextStringObject

_PROMOTED_SUFFIX = "__p"


def _labels_by_acroform_name(mapping):
    """Map every real AcroForm field name -> its human label.

    Handles list ``widget_id`` and split-shared promoted names (``Check Box15``
    and ``Check Box15__p4`` both resolve to their field's label).
    """
    out = {}
    for key, spec in (mapping.get("fields") or {}).items():
        label = spec.get("label") or key
        wid = spec.get("widget_id")
        for w in (wid if isinstance(wid, list) else [wid]):
            w = str(w)
            out.setdefault(w, label)
            # also index the de-promoted base name for the official PDF
            if _PROMOTED_SUFFIX in w:
                out.setdefault(w.split(_PROMOTED_SUFFIX, 1)[0], label)
    return out


def _walk_fields(fields):
    for ref in fields:
        obj = ref.get_object()
        yield obj
        kids = obj.get("/Kids")
        if kids:
            yield from _walk_fields(kids)


def _set_tooltips(writer, labels):
    acro = writer._root_object.get("/AcroForm")
    if not acro:
        return 0
    fields = acro.get_object().get("/Fields") or []
    n = 0
    for obj in _walk_fields(fields):
        name = obj.get("/T")
        if name is None:
            continue
        label = labels.get(str(name))
        if label:
            obj[NameObject("/TU")] = TextStringObject(label)
            n += 1
    return n


def remediate(reader, mapping, title=None, lang="en-US"):
    """Return a writer with /TU tooltips + /Lang + /Title set. Pure, no I/O."""
    writer = pypdf.PdfWriter()
    writer.append(reader)
    labels = _labels_by_acroform_name(mapping)
    n_tu = _set_tooltips(writer, labels)

    root = writer._root_object
    root[NameObject("/Lang")] = TextStringObject(lang)

    acro = root.get("/AcroForm")
    if acro:
        acro.get_object()[NameObject("/NeedAppearances")] = BooleanObject(True)

    if title:
        try:
            writer.add_metadata({"/Title": title})
        except Exception:
            pass
        # DisplayDocTitle so the viewer shows /Title, not the filename
        vp = root.get("/ViewerPreferences")
        if vp is None:
            from pypdf.generic import DictionaryObject
            vp = DictionaryObject()
            root[NameObject("/ViewerPreferences")] = vp
        vp.get_object()[NameObject("/DisplayDocTitle")] = BooleanObject(True)

    return writer, n_tu


def remediate_to_path(pdf_path, mapping, out_path, title=None, lang="en-US"):
    reader = pypdf.PdfReader(str(pdf_path))
    writer, n_tu = remediate(reader, mapping, title=title, lang=lang)
    out = pathlib.Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as fh:
        writer.write(fh)
    return out, n_tu


def _resolve_inputs(arg, mapping_arg, title_arg, repo_root):
    """Accept either a FORM_ID (resolve its blank PDF + mapping + title) or a
    PDF path (+ explicit --mapping)."""
    form_dir = repo_root / "forms" / arg
    if form_dir.is_dir():
        pdf = form_dir / f"{arg}.pdf"
        mapping = json.loads((form_dir / "mapping.json").read_text())
        title = title_arg
        meta = form_dir / "form.yaml"
        if title is None and meta.exists():
            try:
                import yaml
                title = (yaml.safe_load(meta.read_text()) or {}).get("title")
            except Exception:
                pass
        return pdf, mapping, title
    # treat as a PDF path
    if not mapping_arg:
        raise SystemExit("a PDF path needs --mapping forms/<ID>/mapping.json")
    return pathlib.Path(arg), json.loads(pathlib.Path(mapping_arg).read_text()), title_arg


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="a FORM_ID (e.g. CORP_MBCA-6) or a PDF path")
    ap.add_argument("--mapping", help="mapping.json (required if target is a PDF)")
    ap.add_argument("--title", help="document title (defaults to form.yaml title)")
    ap.add_argument("--lang", default="en-US")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    repo_root = pathlib.Path(__file__).resolve().parent.parent.parent
    pdf, mapping, title = _resolve_inputs(a.target, a.mapping, a.title, repo_root)
    out, n_tu = remediate_to_path(pdf, mapping, a.out, title=title, lang=a.lang)
    print(f"wrote {out} — {n_tu} field tooltips, lang={a.lang}, "
          f"title={'set' if title else 'none'}")
    print("NOTE: tag tree (StructTreeRoot) NOT added — run Acrobat/auto-tag for "
          "full PDF/UA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
