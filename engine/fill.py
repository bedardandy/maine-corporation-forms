"""Fill a Maine Secretary of State entity-form PDF from canonical case data.

Reads ``forms/<FORM_ID>/mapping.json`` and the form's blank AcroForm PDF,
resolves each canonical key from a nested case-data dict, and writes the
values back into the PDF's form fields with pypdf.

The engine is deterministic: no network access and no LLM at fill time.

Field types in ``mapping.json``:

- ``text`` (default) — a text widget, or a list of text widgets that all
  receive the same string value.
- ``checkbox`` / ``boolean`` — a button field set to its on-state when the
  resolved value is truthy. Parent fields whose checkboxes are split into
  multiple kid widgets (a quirk of some SoS forms) are handled by setting the
  parent ``/V`` and every kid's ``/AS``.
- ``radio`` — a mutually-exclusive button *group*. ``widget_id`` is the group
  field name and ``options`` maps each canonical enum value to that option's
  export (on-state) name. The selected kid's appearance is turned on and all
  siblings are set to ``/Off``.

A field entry normally resolves the case value at its own dict key. When one
canonical key must feed *different* widgets under different ``when`` gates
(e.g. separate commercial / noncommercial agent-name lines), the mapping uses
two uniquely named entries that each carry ``canonical_key`` — the dotted key
actually resolved against the case.
"""
import json
import os
import sys
from pathlib import Path

import pypdf
from pypdf.generic import NameObject, TextStringObject

from . import canonical, verify
from .plan import eval_when


def load_mapping(form_id, forms_root="forms"):
    path = Path(forms_root) / form_id / "mapping.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_writer(form_id, case_data, forms_root="forms", verify_blank=None):
    """Return a ``pypdf.PdfWriter`` for ``form_id`` filled with ``case_data``.

    The shared work behind :func:`fill` and :func:`fill_to_stream`. The official
    PDF on disk is never modified.

    Before reading the blank, the on-disk PDF is checked against the SHA-256 in
    ``catalog/pdf_manifest.json`` — the revision the mapping was enriched
    against. ``verify_blank`` is ``"warn"`` (default; mismatch emits a
    :class:`engine.verify.BlankRevisionWarning` and still fills), ``"strict"``
    (mismatch raises :class:`engine.verify.BlankRevisionError`), or ``"off"``.
    The default can be set with the ``MCF_VERIFY_BLANK`` environment variable.
    """
    mapping = load_mapping(form_id, forms_root)
    pdf_path = Path(forms_root) / form_id / f"{form_id}.pdf"

    mode = verify_blank or os.environ.get("MCF_VERIFY_BLANK", "warn")
    verify.guard_blank(form_id, forms_root, mode=mode)

    reader = pypdf.PdfReader(str(pdf_path))
    writer = pypdf.PdfWriter()
    writer.append(reader)

    # Repair shared multi-page checkbox fields (a defect in some SoS PDFs where
    # one /Btn drives two unrelated boxes on different pages) so each box is
    # independently settable. Only the in-memory writer is changed; the official
    # PDF on disk stays byte-faithful. Mappings address the resulting fields by
    # their promoted names, e.g. ``Check Box15__p4``.
    split_shared_fields(writer)

    text_values = {}
    checkbox_widgets = []
    radio_selections = []
    enum_checkbox_select = []  # (chosen_widget_or_None, [all_sibling_widgets])
    enum_text_select = []  # (chosen_widget_or_None, [all_widgets], mark)

    for key, spec in mapping["fields"].items():
        # Honor the same `when` gates as engine.plan: a field whose condition is
        # definitively false for this case is not applicable and must not be
        # written, even if the case carries a value for it. An unknown
        # controller (eval_when -> None) leaves the field fillable — the same
        # conservative default plan uses.
        when = spec.get("when")
        if when is not None and eval_when(when, case_data) is False:
            continue
        value = canonical.get(case_data, spec.get("canonical_key", key))
        if value is None:
            continue
        field_type = spec.get("field_type", "text")

        if field_type == "radio":
            on_state = (spec.get("options") or {}).get(str(value))
            if on_state:
                radio_selections.append((spec["widget_id"], on_state))
            continue

        if field_type == "enum_text_select":
            # Single choice among N independent /Tx widgets drawn to look like
            # checkboxes (no real checkbox exists). Write a mark into the chosen
            # widget and blank the others, so a "choose one" text field can never
            # show two marks. ``options`` maps each enum value to its widget.
            options = spec.get("options") or {}
            mark = spec.get("mark", "X")
            chosen = options.get(str(value))
            for wname in options.values():
                text_values[wname] = mark if wname == chosen else ""
            continue

        if field_type == "enum_select":
            # A single choice among N independent checkbox widgets. ``options``
            # maps each enum value to the widget that should be checked. Mark the
            # chosen widget ON and force every sibling OFF so a "choose one" field
            # can never render with two boxes marked.
            options = spec.get("options") or {}
            siblings = list(options.values())
            chosen = options.get(str(value))
            enum_checkbox_select.append((chosen, siblings))
            continue

        widget = spec["widget_id"]
        widgets = widget if isinstance(widget, list) else [widget]
        for wname in widgets:
            if field_type in ("checkbox", "boolean"):
                checkbox_widgets.append((wname, bool(value)))
            else:
                text_values[wname] = str(value)

    if text_values:
        for page in writer.pages:
            try:
                writer.update_page_form_field_values(page, text_values)
            except Exception:
                # update_page_form_field_values raises if a page has no fields
                # in older pypdf; ignore and continue.
                pass

    for wname, on in checkbox_widgets:
        if on:
            _set_checkbox(writer, wname)

    for group_name, on_state in radio_selections:
        _set_radio(writer, group_name, on_state)

    for chosen, siblings in enum_checkbox_select:
        for wname in siblings:
            if wname == chosen:
                _set_checkbox(writer, wname)
            else:
                _set_checkbox_off(writer, wname)

    return writer


def fill(form_id, case_data, out_path, forms_root="forms", verify_blank=None):
    """Fill ``form_id`` with ``case_data`` and write to ``out_path``.

    Returns the output ``Path``. See :func:`build_writer` for ``verify_blank``.
    """
    writer = build_writer(form_id, case_data, forms_root, verify_blank=verify_blank)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as fh:
        writer.write(fh)
    return out


def fill_to_stream(form_id, case_data, stream, forms_root="forms", verify_blank=None):
    """Fill ``form_id`` and write the PDF bytes to a binary ``stream``.

    Useful for serving a filled PDF without a temp file (see tools/api_server.py).
    See :func:`build_writer` for ``verify_blank``.
    """
    writer = build_writer(form_id, case_data, forms_root, verify_blank=verify_blank)
    writer.write(stream)
    return stream


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


def split_shared_fields(writer):
    """Split shared multi-page checkbox ``/Btn`` fields into independent fields.

    Some Maine SoS PDFs reuse one ``/Btn`` field name for two unrelated
    checkboxes on different pages (e.g. a substantive certificate box and the
    cover-letter "expedited filing" box). Toggling the field then checks both
    boxes. This promotes each kid widget into its own terminal field named
    ``<T>__p<page>`` (0-based page index; a same-page duplicate gets a ``_N``
    suffix) so each box is addressable on its own.

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
    page_index = _page_index_map(writer)
    result = {}
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


def _acroform_fields(writer):
    root = writer._root_object
    acro = root.get("/AcroForm")
    if not acro:
        return []
    return acro.get_object().get("/Fields") or []


def _find_field(fields, name):
    """Depth-first search of the AcroForm field tree for a field named ``name``."""
    for ref in fields:
        obj = ref.get_object()
        if obj.get("/T") == name:
            return obj
        kids = obj.get("/Kids")
        if kids:
            found = _find_field(kids, name)
            if found is not None:
                return found
    return None


def _ap_on_states(obj):
    """Return the set of non-/Off appearance-state names (without the slash)."""
    ap = obj.get("/AP")
    if not ap:
        return set()
    normal = ap.get_object().get("/N")
    if not normal:
        return set()
    return {str(k).lstrip("/") for k in normal.get_object().keys() if str(k) != "/Off"}


def _set_checkbox(writer, widget_name):
    """Turn on a checkbox field, including parent fields split across kid widgets.

    Some SoS forms model one logical checkbox as a parent ``/Btn`` whose kid
    widgets carry the appearance and live on different pages. Setting the
    parent ``/V`` and each kid's ``/AS`` makes the box render checked.
    """
    field = _find_field(_acroform_fields(writer), widget_name)
    if field is None:
        return
    kids = field.get("/Kids")
    on_state = None
    if kids:
        for kref in kids:
            states = _ap_on_states(kref.get_object())
            if states:
                on_state = next(iter(states))
                break
    else:
        states = _ap_on_states(field)
        on_state = next(iter(states)) if states else None
    if not on_state:
        return
    on = NameObject("/" + on_state)
    field[NameObject("/V")] = on
    if kids:
        for kref in kids:
            kid = kref.get_object()
            kid[NameObject("/AS")] = on if on_state in _ap_on_states(kid) \
                else NameObject("/Off")
    else:
        field[NameObject("/AS")] = on


def _set_checkbox_off(writer, widget_name):
    """Force a checkbox field (and any kid widgets) to the /Off state.

    The companion to :func:`_set_checkbox`. Used by ``enum_select`` to guarantee
    every non-chosen option in a "choose one" group renders unmarked, even if a
    prior value or default appearance had set it on.
    """
    field = _find_field(_acroform_fields(writer), widget_name)
    if field is None:
        return
    off = NameObject("/Off")
    field[NameObject("/V")] = off
    kids = field.get("/Kids")
    if kids:
        for kref in kids:
            kref.get_object()[NameObject("/AS")] = off
    else:
        field[NameObject("/AS")] = off


def _set_radio(writer, group_name, on_state):
    """Select one option of a radio ``/Btn`` group by its export (on-state) name."""
    field = _find_field(_acroform_fields(writer), group_name)
    if field is None:
        return
    on = NameObject("/" + on_state)
    field[NameObject("/V")] = on
    kids = field.get("/Kids")
    if kids:
        for kref in kids:
            kid = kref.get_object()
            kid[NameObject("/AS")] = on if on_state in _ap_on_states(kid) \
                else NameObject("/Off")
    else:
        field[NameObject("/AS")] = on


def _cli(argv):
    if len(argv) < 4:
        print("usage: python -m engine.fill <FORM_ID> <case_data.json> <out.pdf> "
              "[forms_root]")
        return 1
    form_id = argv[1]
    case_data = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    out_path = argv[3]
    forms_root = argv[4] if len(argv) > 4 else "forms"
    out = fill(form_id, case_data, out_path, forms_root)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
