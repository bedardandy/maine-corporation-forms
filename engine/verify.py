"""Pin each blank PDF to the exact revision the mappings were built against.

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
import hashlib
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_MANIFEST = _ROOT / "catalog" / "pdf_manifest.json"


class BlankRevisionWarning(UserWarning):
    """The on-disk blank does not match the manifest hash (non-fatal)."""


class BlankRevisionError(RuntimeError):
    """The on-disk blank does not match the manifest hash (strict mode)."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest(manifest_path=None) -> dict:
    path = Path(manifest_path) if manifest_path else _MANIFEST
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_entry(form_id: str, manifest=None):
    """Return the manifest record for ``form_id`` (or ``None``).

    The manifest is the shared ``{"forms": {form_id: {...}}}`` dialect
    (``maine_forms_engine.specs.pdf_manifest_schema()``) — converged from
    this repo's historical ``{"pdfs": [...]}`` fork by
    ``tools/convert_pdf_manifest.py``.
    """
    man = manifest if manifest is not None else load_manifest()
    return man.get("forms", {}).get(form_id)


def verify_blank(form_id, forms_root="forms", manifest=None):
    """Check the on-disk blank for ``form_id`` against the manifest.

    Returns ``(ok, detail)``. ``ok`` is ``True`` only when a manifest entry with
    a SHA-256 exists and the on-disk PDF matches it byte-for-byte. A missing
    file, a missing manifest hash, or a size/hash mismatch returns ``False`` with
    a human-readable reason.
    """
    entry = manifest_entry(form_id, manifest)
    if entry is None:
        return False, f"{form_id}: not in manifest"
    expected = entry.get("sha256")
    if not expected:
        return False, f"{form_id}: manifest has no sha256 to verify against"
    pdf = Path(forms_root) / form_id / f"{form_id}.pdf"
    if not pdf.exists():
        return False, f"{form_id}: blank not present ({pdf}); run tools/fetch_pdfs.py"
    data = pdf.read_bytes()
    if entry.get("bytes") is not None and len(data) != entry["bytes"]:
        return False, (f"{form_id}: size {len(data)} != manifest {entry['bytes']} — "
                       "on-disk blank is not the revision the mapping was built against")
    got = sha256_bytes(data)
    if got != expected:
        return False, (f"{form_id}: SHA-256 mismatch — on-disk blank is not the "
                       f"revision the mapping was built against "
                       f"(got {got[:12]}…, manifest {expected[:12]}…); "
                       "re-run enrichment for this form")
    return True, f"{form_id}: verified against manifest"


def guard_blank(form_id, forms_root="forms", mode="warn", manifest=None) -> bool:
    """Fill-time guard. ``mode`` is ``"warn"`` (default), ``"strict"``, or ``"off"``.

    ``warn``  — emit :class:`BlankRevisionWarning` on mismatch, return ``False``.
    ``strict`` — raise :class:`BlankRevisionError` on mismatch.
    ``off``   — skip the check, return ``True``.

    A clean verify always returns ``True``. The mismatch reason is the warning /
    exception message so the caller can surface it to the user.
    """
    if mode == "off":
        return True
    ok, detail = verify_blank(form_id, forms_root, manifest)
    if ok:
        return True
    if mode == "strict":
        raise BlankRevisionError(detail)
    import warnings
    warnings.warn(detail, BlankRevisionWarning, stacklevel=3)
    return False
