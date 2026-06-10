"""Drift detection: the on-disk and upstream blanks must match the manifest hash.

All offline — a synthetic manifest and a stubbed downloader, so the suite stays
network-free.
"""
import hashlib
import json
from pathlib import Path

import pytest

from engine import verify

ROOT = Path(__file__).resolve().parent.parent


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _manifest(blank: bytes):
    return {"forms": {"TEST_X": {
        "filename": "TEST_X.pdf",
        "sha256": _sha(blank), "bytes": len(blank),
        "url": "https://example.test/TEST_X.pdf", "fetch": True,
    }}}


# ---- verify_blank / guard_blank (fill-time, on-disk) -----------------------

def test_verify_blank_matches(tmp_path):
    blank = b"%PDF-1.7 the enriched revision\n"
    man = _manifest(blank)
    d = tmp_path / "TEST_X"
    d.mkdir()
    (d / "TEST_X.pdf").write_bytes(blank)
    ok, detail = verify.verify_blank("TEST_X", forms_root=str(tmp_path), manifest=man)
    assert ok, detail


def test_verify_blank_detects_swap(tmp_path):
    blank = b"%PDF-1.7 the enriched revision\n"
    man = _manifest(blank)
    d = tmp_path / "TEST_X"
    d.mkdir()
    (d / "TEST_X.pdf").write_bytes(b"%PDF-1.7 a DIFFERENT revision Maine swapped in\n")
    ok, detail = verify.verify_blank("TEST_X", forms_root=str(tmp_path), manifest=man)
    assert not ok
    assert "mismatch" in detail.lower() or "size" in detail.lower()


def test_verify_blank_missing_file(tmp_path):
    man = _manifest(b"x")
    ok, detail = verify.verify_blank("TEST_X", forms_root=str(tmp_path), manifest=man)
    assert not ok and "not present" in detail


def test_guard_strict_raises_on_mismatch(tmp_path):
    man = _manifest(b"original")
    d = tmp_path / "TEST_X"
    d.mkdir()
    (d / "TEST_X.pdf").write_bytes(b"swapped")
    with pytest.raises(verify.BlankRevisionError):
        verify.guard_blank("TEST_X", forms_root=str(tmp_path), mode="strict", manifest=man)


def test_guard_warn_does_not_raise(tmp_path, recwarn):
    man = _manifest(b"original")
    d = tmp_path / "TEST_X"
    d.mkdir()
    (d / "TEST_X.pdf").write_bytes(b"swapped")
    result = verify.guard_blank("TEST_X", forms_root=str(tmp_path), mode="warn", manifest=man)
    assert result is False
    assert any(issubclass(w.category, verify.BlankRevisionWarning) for w in recwarn.list)


def test_guard_off_skips(tmp_path):
    man = _manifest(b"original")  # no file on disk at all
    assert verify.guard_blank("TEST_X", forms_root=str(tmp_path), mode="off", manifest=man) is True


# ---- check_upstream classification (re-download vs manifest) ----------------

def test_check_upstream_classifies(monkeypatch):
    import urllib.error

    import tools.check_upstream as cu
    # Whatever the URL, the "server" returns these bytes for every form.
    upstream = b"%PDF-1.7 what the portal serves today\n"

    def fake_download(url, timeout, retries):
        if "gone" in url:
            raise urllib.error.HTTPError(url, 404, "Not Found", None, None)
        if "flake" in url:
            raise TimeoutError("timed out")
        if "outage" in url:
            raise urllib.error.HTTPError(url, 503, "Service Unavailable",
                                         None, None)
        if "maintenance" in url:
            return b"<html>We'll be back soon</html>"
        return upstream

    monkeypatch.setattr(cu, "_download", fake_download)

    def status(form_id, url, pinned):
        return cu.check_one(
            {"form_id": form_id, "url": url, "sha256": _sha(pinned),
             "bytes": len(pinned)}, timeout=1, retries=0)["status"]

    # ok: manifest hash equals what the portal serves.
    assert status("A", "u", upstream) == "ok"
    # CHANGED: manifest pins an older hash than the portal now serves.
    assert status("B", "u", b"older revision") == "CHANGED"
    # GONE: a definitive HTTP 404.
    assert status("C", "gone", b"x") == "GONE"
    # GONE: the URL serves an HTML error/maintenance page, not a PDF —
    # never hash and report it as an adoptable revision.
    assert status("D", "maintenance", b"x") == "GONE"
    # ERROR: transient failures (timeout, 5xx) must not read as GONE.
    assert status("E", "flake", b"x") == "ERROR"
    assert status("F", "outage", b"x") == "ERROR"


# ---- the real manifest is internally consistent ----------------------------

def test_real_manifest_every_entry_anchored():
    man = verify.load_manifest()
    assert man["forms"], "manifest is empty"
    for fid, e in man["forms"].items():
        assert e.get("sha256") and len(e["sha256"]) == 64, fid
        assert e.get("bytes"), fid
        assert e.get("url", "").startswith("https://"), fid


def test_real_manifest_validates_against_shared_schema():
    """The converged manifest must satisfy the shared dialect's JSON Schema
    (shipped with maine-forms-engine), so the drift tooling stays pointable
    at all four sibling catalogs."""
    jsonschema = pytest.importorskip("jsonschema")
    from maine_forms_engine.specs import pdf_manifest_schema
    jsonschema.validate(verify.load_manifest(), pdf_manifest_schema())
