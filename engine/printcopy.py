"""Produce a print-ready copy of a filled Maine SoS business-entity form.

The reference filler (:mod:`engine.fill`) sets AcroForm field values and the
``NeedAppearances`` flag, but it bakes no appearance streams -- so what actually
prints depends on the viewer, and a viewer that ignores ``NeedAppearances`` can
print blank fields. That is unacceptable for a wet-ink workflow where the filing
is *printed and signed by hand*.

This module closes that gap deterministically with PyMuPDF:

* **Appearance bake** -- regenerate every widget's appearance from its value so
  the rendered output is faithful in any viewer.
* **Overflow -> continuation schedules** -- a value that does not fit its field
  rectangle is replaced in-place with a short pointer ("See Schedule A
  attached") and the full text is spilled onto a clean, Word-style schedule page
  appended after the form. Schedules are auto-lettered and back-referenced.
* **Flatten** -- optionally convert widgets to static page content so the print
  copy cannot be re-edited and prints identically everywhere.

The official blank PDFs are never modified; this operates on a *filled copy*.
Wet-ink signature lines are text fields for the signer's *printed* name only, so
flattening never fabricates a signature -- the signature line stays blank for the
pen.
"""

from __future__ import annotations

import io
import json
import string
from dataclasses import dataclass
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover - import guard
    raise ImportError(
        "engine.printcopy requires PyMuPDF (fitz). Install with `pip install pymupdf`."
    ) from exc

from . import fill as _fill
from .mapping import entries as _mapping_entries

# PDF text-field flag bits (PDF 32000-1, Table 226).
_FF_MULTILINE = 1 << 12  # 4096

# Conservative average glyph width as a fraction of font size for Helvetica-ish
# fonts. Real widths vary; we only need a safe lower bound on capacity so we err
# toward *not* spilling borderline content.
_AVG_GLYPH_FRAC = 0.50
_LINE_HEIGHT_FRAC = 1.18
# Auto-size (font size 0) fields shrink to fit; assume they bottom out here.
_MIN_AUTOSIZE_PT = 6.0
_DEFAULT_PT = 10.0
# Only spill when we exceed capacity by a margin, to avoid noise on near-fits.
_OVERFLOW_SLACK = 1.05


@dataclass
class Overflow:
    """One field whose value did not fit and was spilled to a schedule."""

    field_name: str
    label: str
    full_text: str
    schedule_id: str
    page: int


def _labels_by_widget_name(mapping: dict) -> dict:
    """Map AcroForm widget name -> human label from a form's mapping.json."""
    out: dict = {}
    for spec in _mapping_entries(mapping).values():
        label = spec.get("label") or ""
        wid = spec.get("widget_id")
        names = wid if isinstance(wid, list) else ([wid] if wid else [])
        for name in names:
            if isinstance(name, str):
                out.setdefault(name, label)
    return out


def _measure_capacity(widget) -> int:
    """Approximate the character capacity of a text widget."""
    rect = widget.rect
    width = max(rect.width - 4.0, 1.0)  # padding
    height = max(rect.height - 2.0, 1.0)
    size = float(getattr(widget, "text_fontsize", 0) or 0)
    multiline = bool(int(getattr(widget, "field_flags", 0) or 0) & _FF_MULTILINE)
    if size <= 0:
        # Auto-size: single-line fields shrink to fit, so capacity is large;
        # only genuinely huge single-line values overflow. Use the min size.
        size = _MIN_AUTOSIZE_PT if not multiline else _DEFAULT_PT
    glyph = max(size * _AVG_GLYPH_FRAC, 1.0)
    chars_per_line = max(int(width / glyph), 1)
    if not multiline:
        return chars_per_line
    line_h = max(size * _LINE_HEIGHT_FRAC, 1.0)
    lines = max(int(height / line_h), 1)
    return chars_per_line * lines


def _is_text_widget(widget) -> bool:
    return getattr(widget, "field_type", None) == fitz.PDF_WIDGET_TYPE_TEXT


def _next_schedule_id(n: int) -> str:
    """0 -> 'A', 1 -> 'B', ... 26 -> 'AA' (rare)."""
    letters = string.ascii_uppercase
    if n < 26:
        return letters[n]
    return letters[n // 26 - 1] + letters[n % 26]


def _detect_and_pointer(doc, mapping: dict) -> list:
    """Find overflowing text widgets, replace with pointers, return Overflows."""
    labels = _labels_by_widget_name(mapping)
    overflows: list = []
    sched = 0
    for pno in range(doc.page_count):
        page = doc[pno]
        for w in page.widgets() or []:
            if not _is_text_widget(w):
                continue
            value = (w.field_value or "").strip()
            if not value:
                continue
            cap = _measure_capacity(w)
            if len(value) <= cap * _OVERFLOW_SLACK:
                continue
            sid = _next_schedule_id(sched)
            sched += 1
            label = labels.get(w.field_name, w.field_name or "field")
            overflows.append(
                Overflow(
                    field_name=w.field_name or "",
                    label=label,
                    full_text=value,
                    schedule_id=sid,
                    page=pno + 1,
                )
            )
            w.field_value = f"See Schedule {sid} (attached)"
            w.update()
    return overflows


def _fit_autosize(widget) -> None:
    """Set a box-fitted font size on an auto-size (DA size 0) text widget.

    PyMuPDF bakes a size-0 field at a large default, so short values (dates,
    phone numbers, names) print far larger than the surrounding form text. Fit
    the value to the box: by height for the cap, shrinking by width so the whole
    string fits on one line. Clamp to a sane body range.
    """
    value = (widget.field_value or "").strip()
    if not value:
        return
    rect = widget.rect
    usable_w = max(rect.width - 4.0, 1.0)
    usable_h = max(rect.height - 2.0, 1.0)
    multiline = bool(int(getattr(widget, "field_flags", 0) or 0) & _FF_MULTILINE)
    if multiline:
        size = _DEFAULT_PT
    else:
        by_height = usable_h * 0.85
        by_width = usable_w / (max(len(value), 1) * _AVG_GLYPH_FRAC)
        size = min(by_height, by_width)
    size = max(_MIN_AUTOSIZE_PT, min(size, _DEFAULT_PT))
    try:
        widget.text_fontsize = round(size, 1)
    except Exception:
        pass


def _bake_appearances(doc) -> None:
    """Force every text widget to regenerate its appearance from its value.

    Auto-size fields are fitted to their box first so they don't bake oversized.
    """
    for pno in range(doc.page_count):
        for w in doc[pno].widgets() or []:
            try:
                if _is_text_widget(w):
                    cur = float(getattr(w, "text_fontsize", 0) or 0)
                    if cur <= 0:
                        _fit_autosize(w)
                w.update()
            except Exception:
                pass


def _append_schedule_pages(doc, overflows: list, form_title: str, entity_name: str) -> None:
    """Append clean, simple continuation pages for each overflow."""
    if not overflows:
        return
    width, height = fitz.paper_size("letter")
    margin = 72.0
    title_font, body_font = "Helvetica-Bold", "Helvetica"
    for ov in overflows:
        page = doc.new_page(width=width, height=height)
        y = margin
        page.insert_text(
            (margin, y), f"SCHEDULE {ov.schedule_id}", fontname=title_font, fontsize=14
        )
        y += 22
        sub = f"Continuation of: {ov.label}"
        page.insert_text((margin, y), sub, fontname=body_font, fontsize=10)
        y += 14
        ref = f"Attachment to {form_title}"
        if entity_name:
            ref += f" — {entity_name}"
        page.insert_text((margin, y), ref, fontname=body_font, fontsize=9)
        y += 10
        page.draw_line(
            fitz.Point(margin, y), fitz.Point(width - margin, y), width=0.5
        )
        y += 18
        box = fitz.Rect(margin, y, width - margin, height - margin)
        page.insert_textbox(
            box, ov.full_text, fontname=body_font, fontsize=11, lineheight=1.3
        )
        page.insert_text(
            (margin, height - margin + 18),
            f"Schedule {ov.schedule_id}",
            fontname=body_font,
            fontsize=8,
        )


def _entity_name(case_data: dict) -> str:
    ent = case_data.get("entity") if isinstance(case_data, dict) else None
    if isinstance(ent, dict):
        return str(ent.get("name") or "")
    return ""


def make_print_copy(
    filled_pdf,
    mapping: dict,
    out_path: str,
    *,
    form_title: str = "",
    entity_name: str = "",
    flatten: bool = True,
    handle_overflow: bool = True,
) -> dict:
    """Turn a filled PDF (path/bytes/stream) into a print-ready copy.

    Returns a small report dict: ``{"out": path, "overflows": [...], "flattened": bool}``.
    """
    if isinstance(filled_pdf, (bytes, bytearray)):
        doc = fitz.open(stream=bytes(filled_pdf), filetype="pdf")
    elif hasattr(filled_pdf, "read"):
        doc = fitz.open(stream=filled_pdf.read(), filetype="pdf")
    else:
        doc = fitz.open(str(filled_pdf))

    overflows: list = []
    if handle_overflow:
        overflows = _detect_and_pointer(doc, mapping)

    _bake_appearances(doc)
    _append_schedule_pages(doc, overflows, form_title, entity_name)

    if flatten:
        try:
            doc.bake(annots=False, widgets=True)
        except TypeError:
            # Older PyMuPDF signatures.
            doc.bake()

    out = Path(out_path)
    doc.save(str(out), garbage=4, deflate=True)
    doc.close()
    return {
        "out": str(out),
        "overflows": [ov.__dict__ for ov in overflows],
        "flattened": bool(flatten),
    }


def _resolve_root(forms_root):
    """Resolve ``forms_root`` to an absolute path so it works from any CWD."""
    p = Path(forms_root)
    if p.is_absolute():
        return p
    if (Path.cwd() / p).is_dir():
        return Path.cwd() / p
    return Path(__file__).resolve().parent.parent / p


def fill_print_copy(
    form_id: str,
    case_data: dict,
    out_path: str,
    forms_root: str = "forms",
    *,
    flatten: bool = True,
    handle_overflow: bool = True,
) -> dict:
    """Fill ``form_id`` then produce a print-ready copy in one call."""
    root = _resolve_root(forms_root)
    mapping = _fill.load_mapping(form_id, str(root))
    buf = io.BytesIO()
    _fill.fill_to_stream(form_id, case_data, buf, str(root))
    buf.seek(0)
    form_title = ""
    try:
        import yaml  # optional

        meta = yaml.safe_load((root / form_id / "form.yaml").read_text())
        form_title = (meta or {}).get("title", "") or form_id
    except Exception:
        form_title = form_id
    return make_print_copy(
        buf.getvalue(),
        mapping,
        out_path,
        form_title=form_title,
        entity_name=_entity_name(case_data),
        flatten=flatten,
        handle_overflow=handle_overflow,
    )


def _main(argv) -> int:
    if len(argv) < 3:
        print(
            "usage: python -m engine.printcopy <FORM_ID> <case.json> <out.pdf> "
            "[--no-flatten] [--no-overflow]",
            flush=True,
        )
        return 2
    form_id, case_path, out_path = argv[0], argv[1], argv[2]
    flatten = "--no-flatten" not in argv
    overflow = "--no-overflow" not in argv
    case_data = json.loads(Path(case_path).read_text())
    report = fill_print_copy(
        form_id, case_data, out_path, flatten=flatten, handle_overflow=overflow
    )
    print(json.dumps(report, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(_main(sys.argv[1:]))
