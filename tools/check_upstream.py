#!/usr/bin/env python3
"""Detect when Maine has revised a blank form out from under the mappings.

Shim over the shared ``maine-forms-engine``
(``maine_forms_engine.drift.check_upstream``), configured with this repo's
policy; the CLI is unchanged:

- only manifest entries flagged ``"fetch": true`` are probed by default;
- transient download failures (timeout, DNS, HTTP 5xx) are classified ERROR
  and reported, but do NOT gate the exit code: a scheduled run should not
  false-alarm on network flake — only a definitive 404/410 (or a non-PDF
  response at the form's URL) means the blank is GONE.

Maine periodically re-uploads a revised form at the *same URL* — when that
happens the bytes change, the widget layout may shift, and a fill built on
the old mapping can land values in the wrong place. Read-only by default;
exit code is non-zero if any form is CHANGED or GONE, so it gates a pipeline.

Usage:
    python3 tools/check_upstream.py                      # check every fetchable form
    python3 tools/check_upstream.py --forms CORP_MBCA-6,LLC_MLLC-6
    python3 tools/check_upstream.py --json               # machine-readable report
    python3 tools/check_upstream.py --update-manifest    # after human review: adopt new hashes
"""
import pathlib
import sys
import urllib.error

from maine_forms_engine.drift import check_upstream as _cu

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools.fetch_pdfs import _download  # noqa: E402,F401 — kept patchable for tests

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "catalog" / "pdf_manifest.json"


def _classify_download_error(e: Exception) -> str:
    """Only a definitive not-found means the form is gone; any other failure
    (5xx, auth wall, timeout, DNS, connection reset) is transient."""
    if isinstance(e, urllib.error.HTTPError):
        return "GONE" if e.code in (404, 410) else "ERROR"
    return "ERROR"


def check_one(entry: dict, timeout: int, retries: int) -> dict:
    """Probe one form's official URL and classify it against the manifest."""
    return _cu.check_one(entry["form_id"], entry, timeout, retries,
                         downloader=lambda u, t, r: _download(u, t, r),
                         on_download_error=_classify_download_error)


def main() -> int:
    return _cu.main(
        default_manifest=MANIFEST,
        update_hint="Re-run enrichment + audit for each before publishing.",
        downloader=lambda u, t, r: _download(u, t, r),
        on_download_error=_classify_download_error,
        entry_filter=lambda fid, e: e.get("fetch"),
        default_retries=2)


if __name__ == "__main__":
    sys.exit(main())
