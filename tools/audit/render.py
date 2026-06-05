"""Fill -> print-copy -> rasterize, producing PNGs for the visual audit pass.

Uses the deterministic substrate: :func:`engine.printcopy.fill_print_copy`
(bakes appearances, spills overflow to schedules, flattens) then renders each
page to PNG with PyMuPDF so what Opus sees is what prints.
"""

from __future__ import annotations

from pathlib import Path

import fitz

from engine import printcopy


def render_case(form_id: str, case: dict, out_dir: str, *, dpi: int = 150) -> dict:
    """Fill+print a case and rasterize to PNG pages.

    Returns ``{"pdf": path, "pages": [png, ...], "overflows": [...]}``.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pdf_path = out / f"{form_id}.pdf"
    report = printcopy.fill_print_copy(form_id, case, str(pdf_path))

    doc = fitz.open(str(pdf_path))
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pages = []
    for pno in range(doc.page_count):
        pix = doc[pno].get_pixmap(matrix=mat)
        png = out / f"{form_id}_p{pno + 1}.png"
        pix.save(str(png))
        pages.append(str(png))
    doc.close()
    return {"pdf": str(pdf_path), "pages": pages, "overflows": report["overflows"]}


def extract_filled_values(pdf_path: str) -> dict:
    """Read back the field/value pairs from a filled (pre-flatten) PDF.

    If the print copy was flattened its widgets are gone, so callers that need
    values should fill once without flattening; this helper reads whatever
    widgets remain.
    """
    doc = fitz.open(pdf_path)
    out = {}
    for pno in range(doc.page_count):
        for w in doc[pno].widgets() or []:
            if w.field_value:
                out[w.field_name] = w.field_value
    doc.close()
    return out
