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
    return {"pdfs": [{
        "form_id": "TEST_X", "filename": "TEST_X.pdf",
        "sha256": _sha(blank), "bytes": len(blank),
        "url": "https://example.test/TEST_X.pdf", "fetch": True,
    }]}


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
    import tools.check_upstream as cu
    # Whatever the URL, the "server" returns these bytes for every form.
    upstream = b"%PDF-1.7 what the portal serves today\n"

    def fake_download(url, timeout, retries):
        if "gone" in url:
            raise OSError("404 Not Found")
        return upstream

    monkeypatch.setattr(cu, "_download", fake_download)

    # ok: manifest hash equals what the portal serves.
    assert cu.check_one(
        {"form_id": "A", "url": "u", "sha256": _sha(upstream), "bytes": len(upstream)},
        timeout=1, retries=0)["status"] == "ok"
    # CHANGED: manifest pins an older hash than the portal now serves.
    assert cu.check_one(
        {"form_id": "B", "url": "u", "sha256": _sha(b"older revision"), "bytes": 14},
        timeout=1, retries=0)["status"] == "CHANGED"
    # GONE: the URL no longer resolves.
    assert cu.check_one(
        {"form_id": "C", "url": "gone", "sha256": _sha(b"x"), "bytes": 1},
        timeout=1, retries=0)["status"] == "GONE"


# ---- the real manifest is internally consistent ----------------------------

def test_real_manifest_every_entry_anchored():
    man = verify.load_manifest()
    assert man["pdfs"], "manifest is empty"
    for e in man["pdfs"]:
        assert e.get("sha256") and len(e["sha256"]) == 64, e["form_id"]
        assert e.get("bytes"), e["form_id"]
        assert e.get("url", "").startswith("https://"), e["form_id"]
