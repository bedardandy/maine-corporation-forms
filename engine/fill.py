"""Fill a Maine Secretary of State entity-form PDF from canonical case data.

Shim over the shared ``maine-forms-engine`` PDF fill core
(``maine_forms_engine.fill.form_filler.fill_form``, PyMuPDF), with this repo's
policy applied around it — the same convergence pattern as the sibling repos'
``engine/*.py`` shims. The engine package stays repo-agnostic; everything
Maine-SoS-specific lives here:

1. **Preflight gate** — :mod:`engine.preflight` runs first and error-severity
   issues refuse the fill (``--no-preflight`` / ``preflight="off"`` /
   ``MCORP_PREFLIGHT`` skip the gate; partial drafts are legitimate).
2. **Blank-revision guard** — :mod:`engine.verify` checks the on-disk blank
   against ``catalog/pdf_manifest.json`` (``MCORP_VERIFY_BLANK``, legacy
   ``MCF_VERIFY_BLANK``).
3. **Resolution policy** — ``mapping.json`` bindings (via
   ``engine.mapping.entries``) are resolved with :mod:`engine.canonical`
   (dotted keys with list indexing) under the same ``when`` gates as
   ``engine.plan``; ``canonical_key`` overrides, multi-widget fan-outs and the
   corp field types are honored here, before the core ever sees a widget name.
4. **Shared-field runtime split** — multi-page shared checkbox ``/Btn``
   defects are split on a working copy first (:mod:`engine.field_split`), so
   mappings can address the promoted ``<T>__p<page>`` names.
5. **Radio writes** — the shared core deliberately never writes radio groups
   (its soft-lock safety net). This repo's ``radio`` bindings carry the
   per-option on-state export names extracted from the PDF, so selecting one
   is deterministic; a post-pass here sets the group ``/V`` and aligns every
   kid's ``/AS`` exactly like the pre-migration pypdf filler.

Field types in ``mapping.json`` (see ``engine/mapping.py`` for the dialect;
the semantics below are unchanged from the pypdf reference filler):

- ``text`` (default) — a text widget, or a list of text widgets that all
  receive the same string value.
- ``checkbox`` / ``boolean`` — a button field set to its on-state when the
  resolved value is truthy; a falsy value leaves the box untouched.
- ``radio`` — a mutually-exclusive button *group*; ``options`` maps each
  canonical enum value to that option's export (on-state) name.
- ``enum_select`` — one choice among N independent checkboxes; ``options``
  maps each enum value to the widget that is checked, every sibling is forced
  off so a "choose one" field can never show two marks.
- ``enum_text_select`` — like ``enum_select`` but the "boxes" are text
  widgets; the chosen one receives ``mark`` (default ``"X"``), the rest ``""``.

The engine is deterministic: no network access and no LLM at fill time. The
official blank on disk is never modified.
"""
import json
import os
import re
import sys
import tempfile
from pathlib import Path

from maine_forms_engine.fill.form_filler import fill_form as _core_fill_form

from . import canonical, field_split, verify
from .mapping import entries as mapping_entries
from .mapping import load_mapping  # noqa: F401  (re-export; callers use fill.load_mapping)
from .plan import eval_when


def _preflight_mode(preflight):
    mode = preflight or os.environ.get("MCORP_PREFLIGHT", "error")
    if mode not in ("error", "off"):
        raise ValueError(f"preflight must be 'error' or 'off', got {mode!r}")
    return mode


def _run_preflight_gate(form_id, case_data, forms_root, preflight, report):
    """Refuse to fill when preflight finds error-severity issues.

    ``preflight`` is ``"error"`` (default; raise
    :class:`engine.preflight.PreflightError` on any error-severity issue) or
    ``"off"`` (skip the gate — filling a partial draft is legitimate). The
    default can be changed with the ``MCORP_PREFLIGHT`` environment variable.
    When a ``report`` dict is passed, the full preflight result is stored in
    ``report["preflight"]``.
    """
    if _preflight_mode(preflight) == "off":
        return
    from . import preflight as preflight_engine
    result = preflight_engine.preflight(form_id, case_data, forms_root)
    if isinstance(report, dict):
        report["preflight"] = result
    if not result["ok"]:
        raise preflight_engine.PreflightError(result)


def _leaf_keys(obj, prefix=""):
    """Yield dotted canonical leaf paths present in a nested case object."""
    if isinstance(obj, dict) and obj:
        for k, v in obj.items():
            sub = f"{prefix}.{k}" if prefix else str(k)
            yield from _leaf_keys(v, sub)
    elif (isinstance(obj, list)
          and any(isinstance(x, (dict, list)) for x in obj)):
        for i, v in enumerate(obj):
            yield from _leaf_keys(v, f"{prefix}[{i}]")
    elif prefix:
        yield prefix


# The token the shared core's checkbox path treats as affirmative; the core
# resolves it to the widget's real on-state at write time.
_CHECK = "Yes"


def resolve_fill(form_id, case_data, forms_root="forms", report=None):
    """Resolve a form's mapping against ``case_data`` into a write plan.

    Pure (no PDF): returns ``{"field_data": {widget_name: str},
    "radio_selections": [(group_name, on_state), ...]}``. ``field_data`` is
    what the shared fill core writes (text values, ``enum_text_select``
    marks, and checkbox/enum-select tokens — :data:`_CHECK` for on, ``""``
    for explicitly-off siblings). Radio groups are returned separately for
    the policy post-pass, because the shared core never writes them.

    ``report``, if a dict, is populated with fill diagnostics:

    - ``written``          — mapping entries whose value was resolved for
                             writing.
    - ``skipped_when``     — entries gated off by a false ``when`` condition.
    - ``dropped_enums``    — enum/radio values with no option mapping; the
                             field is left untouched instead of silently
                             no-opping or blanking the group.
    - ``ignored_case_keys`` — case leaf keys no mapping entry consumes.
    """
    mapping = load_mapping(form_id, forms_root)

    diag = report if isinstance(report, dict) else {}
    diag["written"] = []
    diag["skipped_when"] = []
    diag["dropped_enums"] = []
    diag["ignored_case_keys"] = []

    field_data = {}
    radio_selections = []

    consumed_keys = set()
    for key, spec in mapping_entries(mapping).items():
        ckey = spec.get("canonical_key", key)
        consumed_keys.add(ckey)
        # Honor the same `when` gates as engine.plan: a field whose condition is
        # definitively false for this case is not applicable and must not be
        # written, even if the case carries a value for it. An unknown
        # controller (eval_when -> None) leaves the field fillable — the same
        # conservative default plan uses.
        when = spec.get("when")
        if when is not None:
            m = re.match(r"\s*([A-Za-z0-9_.\[\]]+)", when)
            if m:
                consumed_keys.add(m.group(1))  # the gate's controller key
            if eval_when(when, case_data) is False:
                diag["skipped_when"].append({"key": key, "when": when})
                continue
        value = canonical.get(case_data, ckey)
        if value is None:
            continue
        field_type = spec.get("field_type", "text")

        if field_type == "radio":
            options = spec.get("options") or {}
            on_state = options.get(str(value))
            if on_state:
                radio_selections.append((spec["widget_id"], on_state))
                diag["written"].append(key)
            else:
                diag["dropped_enums"].append(
                    {"key": key, "value": str(value),
                     "allowed": sorted(options)})
            continue

        if field_type == "enum_text_select":
            # Single choice among N independent /Tx widgets drawn to look like
            # checkboxes (no real checkbox exists). Write a mark into the chosen
            # widget and blank the others, so a "choose one" text field can never
            # show two marks. ``options`` maps each enum value to its widget.
            # An unmapped value leaves the group untouched and is reported.
            options = spec.get("options") or {}
            mark = spec.get("mark", "X")
            chosen = options.get(str(value))
            if chosen is None:
                diag["dropped_enums"].append(
                    {"key": key, "value": str(value),
                     "allowed": sorted(options)})
                continue
            for wname in options.values():
                field_data[wname] = mark if wname == chosen else ""
            diag["written"].append(key)
            continue

        if field_type == "enum_select":
            # A single choice among N independent checkbox widgets. ``options``
            # maps each enum value to the widget that should be checked. Mark the
            # chosen widget ON and force every sibling OFF so a "choose one" field
            # can never render with two boxes marked. An unmapped value leaves
            # the group untouched and is reported.
            options = spec.get("options") or {}
            chosen = options.get(str(value))
            if chosen is None:
                diag["dropped_enums"].append(
                    {"key": key, "value": str(value),
                     "allowed": sorted(options)})
                continue
            for wname in options.values():
                field_data[wname] = _CHECK if wname == chosen else ""
            diag["written"].append(key)
            continue

        widget = spec["widget_id"]
        widgets = widget if isinstance(widget, list) else [widget]
        wrote = False
        for wname in widgets:
            if field_type in ("checkbox", "boolean"):
                # Truthiness matches the pypdf reference filler: any non-empty
                # value checks the box; a falsy value leaves it untouched
                # (never an explicit uncheck).
                if bool(value):
                    field_data[wname] = _CHECK
                wrote = True
            else:
                field_data[wname] = str(value)
                wrote = True
        if wrote:
            diag["written"].append(key)

    diag["ignored_case_keys"] = sorted(
        set(_leaf_keys(case_data)) - consumed_keys)

    return {"field_data": field_data, "radio_selections": radio_selections}


def _widget_on_state(widget):
    """A button widget's on-state name (the /AP key that isn't Off)."""
    try:
        on = widget.on_state()
        if on:
            return on
    except Exception:
        pass
    try:
        states = (widget.button_states() or {}).get("normal") or []
        on = [s for s in states if s != "Off"]
        return on[0] if on else None
    except Exception:
        return None


def _apply_radio_selections(pdf_path, selections):
    """Select radio-group options on a filled PDF (policy post-pass).

    The shared fill core soft-locks radio groups (it can only *suggest*); this
    repo's ``radio`` bindings carry the exact on-state export name per enum
    value, so the selection is deterministic. For each ``(group_name,
    on_state)``: every widget of the group gets ``/AS`` set to the on-state it
    renders (or ``/Off``), and the group field's ``/V`` is set to the
    selection — the same end state the pre-migration pypdf filler produced.
    """
    if not selections:
        return
    import fitz

    doc = fitz.open(str(pdf_path))
    try:
        for group_name, on_state in selections:
            target = f"/{on_state}"
            parent_xrefs = set()
            terminal_xrefs = []
            for page in doc:
                for w in page.widgets() or []:
                    if w.field_name != group_name:
                        continue
                    state = _widget_on_state(w)
                    doc.xref_set_key(
                        w.xref, "AS", target if state == on_state else "/Off")
                    ptype, pval = doc.xref_get_key(w.xref, "Parent")
                    if ptype == "xref":
                        parent_xrefs.add(int(pval.split()[0]))
                    else:
                        terminal_xrefs.append(w.xref)
            for xref in parent_xrefs or terminal_xrefs:
                doc.xref_set_key(xref, "V", target)
        doc.saveIncr()
    finally:
        doc.close()


def fill_pdf_bytes(form_id, case_data, forms_root="forms", verify_blank=None,
                   report=None):
    """Fill ``form_id`` with ``case_data`` and return the PDF bytes.

    The shared work behind :func:`fill` and :func:`fill_to_stream` (no
    preflight here — the public entry points gate first). The official PDF on
    disk is never modified.

    Before reading the blank, the on-disk PDF is checked against the SHA-256 in
    ``catalog/pdf_manifest.json`` — the revision the mapping was enriched
    against. ``verify_blank`` is ``"warn"`` (default; mismatch emits a
    :class:`engine.verify.BlankRevisionWarning` and still fills), ``"strict"``
    (mismatch raises :class:`engine.verify.BlankRevisionError`), or ``"off"``.
    The default can be set with the ``MCORP_VERIFY_BLANK`` environment
    variable (``MCF_VERIFY_BLANK`` is honored as a legacy fallback).

    ``report``, if a dict, receives the :func:`resolve_fill` diagnostics plus
    the shared core's write report: ``missing_widgets`` (mapped names absent
    from the PDF — a stale-mapping signal), ``overflowed`` (values that did
    not fit), and ``radio_groups_skipped`` (the core's yellow light; entries
    this repo's radio post-pass then writes are removed from it).
    """
    pdf_path = Path(forms_root) / form_id / f"{form_id}.pdf"

    mode = (verify_blank
            or os.environ.get("MCORP_VERIFY_BLANK")
            or os.environ.get("MCF_VERIFY_BLANK", "warn"))
    verify.guard_blank(form_id, forms_root, mode=mode)
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"{pdf_path} not on disk; run tools/fetch_pdfs.py --forms {form_id}")

    diag = report if isinstance(report, dict) else {}
    plan = resolve_fill(form_id, case_data, forms_root, report=diag)

    with tempfile.TemporaryDirectory(prefix=f"mcorp_fill_{form_id}_") as td:
        tmp = Path(td)
        src = pdf_path
        # Repair shared multi-page checkbox fields (a defect in some SoS PDFs
        # where one /Btn drives two unrelated boxes on different pages) on a
        # working copy, so each box is independently settable under its
        # promoted name (e.g. ``Check Box15__p4``). The official PDF on disk
        # stays byte-faithful.
        split_map = field_split.split_to_copy(pdf_path, tmp / "split.pdf")
        if split_map:
            src = tmp / "split.pdf"
        out_pdf = tmp / "filled.pdf"
        core = _core_fill_form(
            str(src), dict(plan["field_data"]), str(out_pdf),
            form_id=form_id, addendum_policy="none",
            supported_policies=frozenset({"none"}), return_report=True)
        # Policy post-pass: deterministic radio selection (see module doc).
        _apply_radio_selections(out_pdf, plan["radio_selections"])
        data = out_pdf.read_bytes()

    diag["missing_widgets"] = core["missing_fields"]
    diag["overflowed"] = core["overflowed"]
    written_groups = {g for g, _ in plan["radio_selections"]}
    diag["radio_groups_skipped"] = [
        e for e in core.get("radio_groups_skipped") or []
        if e["field_id"] not in written_groups]
    if split_map:
        diag["fields_split"] = split_map
    return data


def fill(form_id, case_data, out_path, forms_root="forms", verify_blank=None,
         report=None, preflight=None):
    """Fill ``form_id`` with ``case_data`` and write to ``out_path``.

    Runs :mod:`engine.preflight` first and raises
    :class:`engine.preflight.PreflightError` on error-severity issues unless
    ``preflight="off"`` (see :func:`_run_preflight_gate`). Returns the output
    ``Path``. See :func:`fill_pdf_bytes` for ``verify_blank`` and the
    ``report`` diagnostics dict.
    """
    _run_preflight_gate(form_id, case_data, forms_root, preflight, report)
    data = fill_pdf_bytes(form_id, case_data, forms_root,
                          verify_blank=verify_blank, report=report)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return out


def fill_to_stream(form_id, case_data, stream, forms_root="forms",
                   verify_blank=None, report=None, preflight=None):
    """Fill ``form_id`` and write the PDF bytes to a binary ``stream``.

    Useful for serving a filled PDF without a temp file (see tools/api_server.py).
    Runs the same preflight gate as :func:`fill`. See :func:`fill_pdf_bytes`
    for ``verify_blank`` and the ``report`` diagnostics dict.
    """
    _run_preflight_gate(form_id, case_data, forms_root, preflight, report)
    data = fill_pdf_bytes(form_id, case_data, forms_root,
                          verify_blank=verify_blank, report=report)
    stream.write(data)
    return stream


def _cli(argv):
    no_preflight = "--no-preflight" in argv
    argv = [a for a in argv if a != "--no-preflight"]
    if len(argv) < 4:
        print("usage: python -m engine.fill <FORM_ID> <case_data.json> <out.pdf> "
              "[forms_root] [--no-preflight]")
        return 1
    form_id = argv[1]
    case_data = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    out_path = argv[3]
    forms_root = argv[4] if len(argv) > 4 else "forms"
    report = {}
    try:
        out = fill(form_id, case_data, out_path, forms_root, report=report,
                   preflight="off" if no_preflight else None)
    except Exception as e:
        from . import preflight as preflight_engine
        if isinstance(e, preflight_engine.PreflightError):
            print(e)
            return 1
        raise
    print(f"wrote {out} ({len(report['written'])} fields written, "
          f"{len(report['skipped_when'])} gated off)")
    pf = report.get("preflight")
    if pf:
        s = pf["summary"]
        print(f"  preflight: {s['warning']} warning(s), {s['manual']} "
              "manual-review rubric check(s) — see python -m "
              f"engine.preflight {form_id} <case.json>")
    for d in report["dropped_enums"]:
        print(f"  UNMAPPED ENUM (not written): {d['key']} = {d['value']!r} "
              f"(allowed: {', '.join(d['allowed'])})")
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv))
