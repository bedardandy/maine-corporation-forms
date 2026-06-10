#!/usr/bin/env python3
"""Fetch the blank Maine SoS PDFs from the official portal, verified by SHA-256.

Shim over the shared ``maine-forms-engine`` (``maine_forms_engine.drift.
fetch_pdfs``), configured with this repo's policy (only manifest entries
flagged ``"fetch": true`` are fetched); the CLI is unchanged.

The blank forms are public records of the Maine Secretary of State. To avoid
re-hosting them, none is committed to this repository; this tool downloads
each one from the state portal and checks it byte-for-byte against the hash
recorded in ``catalog/pdf_manifest.json``. A download whose hash does not
match is rejected.

Usage:
    python3 tools/fetch_pdfs.py                       # all fetchable forms
    python3 tools/fetch_pdfs.py --forms CORP_MBCA-6,LLC_MLLC-6
    python3 tools/fetch_pdfs.py --list               # show what would be fetched
"""
import pathlib
import sys

from maine_forms_engine.drift import fetch_pdfs as _fp
from maine_forms_engine.drift.fetch_pdfs import _verify  # noqa: F401

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "catalog" / "pdf_manifest.json"
USER_AGENT = "maine-corporation-forms/fetch_pdfs (+https://www.maine.gov/sos)"
_fp.USER_AGENT = USER_AGENT  # downloads announce this repo, not the package


def _download(url: str, timeout: int, retries: int) -> bytes:
    return _fp._download(url, timeout, retries)


def main() -> int:
    return _fp.main(default_manifest=MANIFEST,
                    default_forms_root=ROOT / "forms",
                    entry_filter=lambda fid, e: e.get("fetch"),
                    default_retries=2)


if __name__ == "__main__":
    sys.exit(main())
