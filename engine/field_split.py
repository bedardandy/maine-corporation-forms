"""Runtime split of shared multi-page checkbox fields (a SoS PDF defect).

Some Maine SoS PDFs reuse one ``/Btn`` field name for two unrelated checkboxes
on different pages (e.g. a substantive certificate box and the cover-letter
"expedited filing" box). Toggling the field then checks both boxes. This
module promotes each kid widget into its own terminal field named
``<T>__p<page>`` (0-based page index; a same-page duplicate gets a ``_N``
suffix) so each box is addressable on its own. Mappings address the promoted
names (e.g. ``Check Box15__p4``).

This is repo policy on top of the shared fill core: the sibling repos drive
their (single-widget, declarative) splits from ``field_splits.json`` via
``maine_forms_engine.fill.field_split``; this repo's defect class needs every
kid promoted with deterministic names, detected at fill time, so the split
stays here. The official PDF on disk is never modified — the split is applied
to an in-memory copy (:func:`split_shared_fields`) or a working-copy file
(:func:`split_to_copy`); detection-only callers use :func:`has_shared_fields`.

Extracted verbatim from the pre-migration ``engine/fill.py`` (the pypdf
reference filler); the promotion logic is unchanged.
"""
from pathlib import Path

import pypdf
from pypdf.generic import NameObject, TextStringObject


def _page_index_map(writer):
    idx = {}
    for i, page in enumerate(writer.pages):
        try:
            idx[page.indirect_reference.idnum] = i
        except Exception:
            pass
    return idx


def _kid_page(writer, kref, page_index):
    """Return the 0-based page index a kid widget lives on, or ``None``."""
    kid = kref.get_object()
    parent_page = kid.get("/P")
    if parent_page is not None:
        try:
            return page_index.get(parent_page.get_object().indirect_reference.idnum)
        except Exception:
            pass
    for i, page in enumerate(writer.pages):
        for annot in page.get("/Annots") or []:
            try:
                if annot.indirect_reference.idnum == kref.indirect_reference.idnum:
                    return i
            except Exception:
                pass
    return None


def _is_radio(obj):
    ff = obj.get("/Ff")
    try:
        return bool(int(ff) & (1 << 15)) if ff is not None else False
    except Exception:
        return False


def _shared_btn_fields(writer):
    """Yield ``(field_ref, field_obj, kid_pages)`` for splittable fields."""
    acro = writer._root_object.get("/AcroForm")
    if not acro:
        return
    fields = acro.get_object().get("/Fields")
    if not fields:
        return
    page_index = _page_index_map(writer)
    for ref in list(fields):
        obj = ref.get_object()
        if obj.get("/FT") != "/Btn" or _is_radio(obj):
            continue
        kids = obj.get("/Kids")
        if not kids or len(kids) < 2:
            continue
        pages = [_kid_page(writer, k, page_index) for k in kids]
        if len({p for p in pages if p is not None}) < 2:
            continue
        if None in pages:
            # A kid whose page cannot be resolved would get a bogus
            # ``<T>__pNone`` name; leave the field unsplit rather than emit
            # unaddressable widgets.
            continue
        yield ref, obj, pages


def split_shared_fields(writer):
    """Split shared multi-page checkbox ``/Btn`` fields into independent fields.

    Radio groups (whose kids share a page and carry the radio flag) are left
    untouched. Only the in-memory ``writer`` is mutated. Returns a mapping of
    ``{original_field_name: [new_field_name, ...]}``.
    """
    acro = writer._root_object.get("/AcroForm")
    if not acro:
        return {}
    fields = acro.get_object().get("/Fields")
    if not fields:
        return {}
    result = {}
    for ref, obj, pages in list(_shared_btn_fields(writer)):
        kids = obj.get("/Kids")
        name = str(obj.get("/T"))
        ff = obj.get("/Ff")
        used = {}
        new_names = []
        for kref, page in zip(list(kids), pages):
            kid = kref.get_object()
            base = f"{name}__p{page}"
            seen = used.get(base, 0)
            used[base] = seen + 1
            new_name = base if seen == 0 else f"{base}_{seen}"
            kid[NameObject("/T")] = TextStringObject(new_name)
            kid[NameObject("/FT")] = NameObject("/Btn")
            if ff is not None:
                kid[NameObject("/Ff")] = ff
            if "/Parent" in kid:
                del kid[NameObject("/Parent")]
            kid[NameObject("/AS")] = NameObject("/Off")
            fields.append(kref)
            new_names.append(new_name)
        try:
            fields.remove(ref)
        except Exception:
            for i, fr in enumerate(list(fields)):
                if fr.get_object() is obj:
                    del fields[i]
                    break
        result[name] = new_names
    return result


def has_shared_fields(pdf_path) -> bool:
    """True when ``pdf_path`` carries at least one splittable shared field."""
    reader = pypdf.PdfReader(str(pdf_path))
    writer = pypdf.PdfWriter()
    writer.append(reader)
    return next(iter(_shared_btn_fields(writer)), None) is not None


def split_to_copy(src_pdf, dst_pdf) -> dict:
    """Apply the runtime split to a working copy at ``dst_pdf``.

    Returns ``{original_field_name: [new_field_name, ...]}`` (empty when the
    PDF has no splittable shared field — ``dst_pdf`` is not written then).
    The source PDF is never modified.
    """
    reader = pypdf.PdfReader(str(src_pdf))
    writer = pypdf.PdfWriter()
    writer.append(reader)
    result = split_shared_fields(writer)
    if result:
        dst = Path(dst_pdf)
        dst.parent.mkdir(parents=True, exist_ok=True)
        with open(dst, "wb") as fh:
            writer.write(fh)
    return result
