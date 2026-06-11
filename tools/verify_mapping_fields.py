#!/usr/bin/env python3
"""Re-verify a mapping.json against the pinned blank, then stamp it.

Shim over the shared ``maine-forms-engine``
(``maine_forms_engine.verify_mapping``); the CLI is unchanged, anchored to
this repo's ``forms/`` tree and ``catalog/pdf_manifest.json``.
``built_against_sha256`` is the staleness gate of the MRS-1041ME incident
class: a status flag that says fillable while mapped widgets no longer exist
in a re-issued blank. A mapping must only carry the stamp after an honest
re-verification against the very revision the manifest pins — never as a
blind back-fill. Per form this tool checks blank identity (on-disk
``forms/<ID>/<ID>.pdf`` matches the manifest SHA-256 byte-for-byte) and field
survival (every mapped field resolves to a live AcroForm widget).

Two of the engine's format hooks are swapped for this repo's dialect:

- ``resolve_widgets`` is the engine's ``direct_widget_names``: this repo's
  canonical-direction ``mapping.json`` keys ``map`` by the AcroForm field
  name itself (text/checkbox widget, radio *group* name, or an enum-select
  group's first option widget — all live names), so there is no schema.json
  indirection to walk.
- ``split_names`` reflects this repo's *runtime* shared-field split
  (:mod:`engine.field_split`): promoted ``<T>__p<page>`` names are computed
  from the blank at fill time, not declared in a ``field_splits.json``, so
  the hook runs the same promotion in memory and counts those names as
  present (e.g. ``LLC_MLLC-12A``'s ``Check Box16__p1``).

Read-only by default. ``--stamp`` writes ``built_against_sha256`` only for
forms that fully verify; a form that fails stays unstamped and is reported
(re-map it before it may fill). Exit code is non-zero when any checked form
fails, so it gates a pipeline. ``tests/test_built_against.py`` pins every
stamped mapping to the manifest hash.

Usage:
    python3 tools/verify_mapping_fields.py                    # verify all 156
    python3 tools/verify_mapping_fields.py --forms NP_MNPCA-6
    python3 tools/verify_mapping_fields.py --json             # machine report
    python3 tools/verify_mapping_fields.py --stamp            # verify + stamp
"""
import pathlib
import sys

from maine_forms_engine import verify_mapping as _vm
from maine_forms_engine.verify_mapping import direct_widget_names

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import field_split  # noqa: E402

FORMS = ROOT / "forms"
MANIFEST = ROOT / "catalog" / "pdf_manifest.json"


def split_names(fdir: pathlib.Path) -> set:
    """Widget names this repo's runtime shared-field split introduces.

    The fill path promotes each kid of a shared multi-page checkbox ``/Btn``
    to ``<T>__p<page>`` on a working copy (:mod:`engine.field_split`);
    mappings address the promoted names, which never exist in the blank's own
    AcroForm tree. Re-run the same promotion on an in-memory copy of the
    pinned blank and return the names it would create.
    """
    pdf = fdir / f"{fdir.name}.pdf"
    if not pdf.exists():
        return set()
    import pypdf
    reader = pypdf.PdfReader(str(pdf))
    writer = pypdf.PdfWriter()
    writer.append(reader)
    promoted = field_split.split_shared_fields(writer)
    return {name for names in promoted.values() for name in names}


def verify_form(fid: str, manifest: dict,
                forms_root: pathlib.Path = FORMS) -> dict:
    """Verify one form's mapping against the pinned blank.

    Returns ``{form_id, ok, ...}``; ``ok`` is True only when the blank
    matches the manifest hash AND every mapped field name resolves to a live
    (or runtime-promoted) widget. Failure modes carry a ``reason`` plus the
    offending lists.
    """
    return _vm.verify_form(fid, manifest, forms_root,
                           resolve_widgets=direct_widget_names,
                           split_names=split_names)


def stamp(fid: str, sha: str, forms_root: pathlib.Path = FORMS) -> bool:
    """Write ``built_against_sha256`` into mapping.json (appended after the
    existing keys — this repo's mappings carry no ``model``/``status``
    anchor). Returns True when the file changed."""
    return _vm.stamp(fid, sha, forms_root)


def main(argv=None) -> int:
    return _vm.main(argv, default_forms_root=FORMS, default_manifest=MANIFEST,
                    resolve_widgets=direct_widget_names,
                    split_names=split_names)


if __name__ == "__main__":
    sys.exit(main())
