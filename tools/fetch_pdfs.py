#!/usr/bin/env python3
"""Fetch the blank Maine SoS PDFs from the official portal, verified by SHA-256.

The blank forms are public records of the Maine Secretary of State. To avoid
re-hosting them, none is committed to this repository; this script downloads each
one from the state portal and checks it byte-for-byte against the hash recorded
in ``catalog/pdf_manifest.json``. A download whose hash does not match is
rejected. Every manifest entry carries ``"fetch": true``.

Usage:
    python3 tools/fetch_pdfs.py                       # all fetchable forms
    python3 tools/fetch_pdfs.py --forms CORP_MBCA-6,LLC_MLLC-6
    python3 tools/fetch_pdfs.py --list               # show what would be fetched
"""
import argparse
import hashlib
import json
import pathlib
import ssl
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "catalog" / "pdf_manifest.json"
USER_AGENT = "maine-corporation-forms/fetch_pdfs (+https://www.maine.gov/sos)"


def _download(url: str, timeout: int, retries: int) -> bytes:
    ctx = ssl.create_default_context()
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
    raise last


def _verify(data: bytes, entry: dict) -> str | None:
    if len(data) != entry["bytes"]:
        return f"size {len(data)} != expected {entry['bytes']}"
    got = hashlib.sha256(data).hexdigest()
    if got != entry["sha256"]:
        return f"sha256 mismatch (got {got[:12]}…)"
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch verified blank Maine SoS PDFs")
    ap.add_argument("--forms", help="comma-separated form ids (default: all fetchable)")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--list", action="store_true", help="list and exit, do not download")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    entries = {e["form_id"]: e for e in manifest["pdfs"]}

    if args.forms:
        want = [f.strip() for f in args.forms.split(",") if f.strip()]
        missing = [f for f in want if f not in entries]
        if missing:
            print(f"unknown form ids (not in manifest): {', '.join(missing)}")
            return 2
        ids = want
    else:
        ids = list(entries)

    fetchable = [f for f in ids if entries[f].get("fetch")]

    if args.list:
        for f in fetchable:
            print(f"fetch  {f}  {entries[f]['url']}")
        return 0

    ok = fail = skip = 0
    for fid in fetchable:
        entry = entries[fid]
        dest = ROOT / "forms" / fid / f"{fid}.pdf"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            err = _verify(dest.read_bytes(), entry)
            if err is None:
                print(f"  skip   {fid}: present and verified")
                skip += 1
                continue
            print(f"  stale  {fid}: on-disk file fails verify ({err}); re-fetching")
        try:
            data = _download(entry["url"], args.timeout, args.retries)
        except Exception as e:  # noqa: BLE001
            print(f"  FAIL   {fid}: download error: {e}")
            fail += 1
            continue
        err = _verify(data, entry)
        if err:
            print(f"  FAIL   {fid}: {err}  ({entry['url']})")
            fail += 1
            continue
        dest.write_bytes(data)
        print(f"  ok     {fid}: fetched and verified")
        ok += 1

    print(f"\nfetched={ok} skipped={skip} failed={fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
