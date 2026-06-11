"""Pin each blank PDF to the exact revision the mappings were built against.

Shim over the shared ``maine-forms-engine`` blank-revision guard
(``maine_forms_engine.fill.verify``) — the check logic lives in the package;
this module only re-anchors the default manifest location to this repo's
``catalog/pdf_manifest.json`` (the package default is cwd-relative).

``catalog/pdf_manifest.json`` records a SHA-256 (plus byte size) for every blank
Maine SoS form. That hash is the anchor: the mapping.json widget ids, the
schema, and the field rationale were all enriched against *that* revision of the
PDF. If Maine later re-uploads a revised form at the same URL, its bytes change
and these checks fail loudly — the signal to re-run enrichment before trusting a
fill, instead of silently filling the wrong revision.

Two checks live here:

- :func:`verify_blank` — does the blank *on disk* still match the manifest? Used
  as a fill-time guard so a swapped-out local file cannot be filled silently.
- the manifest helpers are also reused by ``tools/check_upstream.py``, which
  re-downloads from the official URL to detect upstream drift before it ever
  reaches disk.
"""
from pathlib import Path

from maine_forms_engine.fill import verify as _pkg
from maine_forms_engine.fill.verify import (  # noqa: F401  (re-exports)
    BlankRevisionError,
    BlankRevisionWarning,
    sha256_bytes,
)

_ROOT = Path(__file__).resolve().parent.parent
_MANIFEST = _ROOT / "catalog" / "pdf_manifest.json"


def load_manifest(manifest_path=None) -> dict:
    """Load the manifest (default: this repo's ``catalog/pdf_manifest.json``)."""
    return _pkg.load_manifest(manifest_path or _MANIFEST)


def manifest_entry(form_id, manifest=None):
    """Return the manifest record for ``form_id`` (or ``None``).

    The manifest is the shared ``{"forms": {form_id: {...}}}`` dialect
    (``maine_forms_engine.specs.pdf_manifest_schema()``) — converged from
    this repo's historical ``{"pdfs": [...]}`` fork by
    ``tools/convert_pdf_manifest.py``.
    """
    man = manifest if manifest is not None else load_manifest()
    return _pkg.manifest_entry(form_id, man)


def verify_blank(form_id, forms_root="forms", manifest=None):
    """Check the on-disk blank for ``form_id`` against the manifest.

    Returns ``(ok, detail)``. ``ok`` is ``True`` only when a manifest entry with
    a SHA-256 exists and the on-disk PDF matches it byte-for-byte. A missing
    file, a missing manifest hash, or a size/hash mismatch returns ``False`` with
    a human-readable reason.
    """
    man = manifest if manifest is not None else load_manifest()
    return _pkg.verify_blank(form_id, forms_root=forms_root, manifest=man)


def guard_blank(form_id, forms_root="forms", mode="warn", manifest=None) -> bool:
    """Fill-time guard. ``mode`` is ``"warn"`` (default), ``"strict"``, or ``"off"``.

    ``warn``  — emit :class:`BlankRevisionWarning` on mismatch, return ``False``.
    ``strict`` — raise :class:`BlankRevisionError` on mismatch.
    ``off``   — skip the check, return ``True``.

    A clean verify always returns ``True``. The mismatch reason is the warning /
    exception message so the caller can surface it to the user.
    """
    if mode == "off":  # no manifest read when the check is skipped
        return True
    man = manifest if manifest is not None else load_manifest()
    return _pkg.guard_blank(form_id, forms_root=forms_root, mode=mode,
                            manifest=man)
