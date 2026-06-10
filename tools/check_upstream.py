#!/usr/bin/env python3
"""Detect when Maine has revised a blank form out from under the mappings.

The mappings, schema, and field inventory for each form were enriched against
one specific revision of the official PDF, pinned by SHA-256 in
``catalog/pdf_manifest.json``. Maine periodically re-uploads a revised form at
the *same URL* — when that happens the bytes change, the widget layout may
shift, and a fill built on the old mapping can land values in the wrong place.

This tool re-downloads each blank from its official URL, hashes it, and compares
to the manifest. It is read-only by default: nothing is written to ``forms/``,
so it is safe to run on a schedule (CI/cron) as an early-warning that a form
needs re-enrichment.

Exit code is non-zero if any form is CHANGED or GONE, so it gates a pipeline.
Transient download failures (timeout, DNS, HTTP 5xx) are classified ERROR and
reported, but do NOT gate the exit code: a scheduled run should not false-alarm
on network flake — only a definitive 404/410 (or a non-PDF response at the
form's URL) means the blank is GONE.

Usage:
    python3 tools/check_upstream.py                      # check every fetchable form
    python3 tools/check_upstream.py --forms CORP_MBCA-6,LLC_MLLC-6
    python3 tools/check_upstream.py --json               # machine-readable report
    python3 tools/check_upstream.py --update-manifest     # after human review: adopt new hashes
"""
import argparse
import json
import pathlib
import sys
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import verify  # noqa: E402
from tools.fetch_pdfs import _download  # reuse the verified-download helper  # noqa: E402

MANIFEST = ROOT / "catalog" / "pdf_manifest.json"


def check_one(entry: dict, timeout: int, retries: int) -> dict:
    """Probe one form's official URL and classify it against the manifest."""
    fid = entry["form_id"]
    url = entry.get("url")
    if not url:
        return {"form_id": fid, "status": "NO_URL"}
    try:
        data = _download(url, timeout, retries)
    except urllib.error.HTTPError as e:
        # Only a definitive not-found means the form is gone; any other HTTP
        # failure (5xx, auth wall, ...) is a transient/server problem.
        status = "GONE" if e.code in (404, 410) else "ERROR"
        return {"form_id": fid, "status": status, "detail": str(e)[:160]}
    except Exception as e:  # noqa: BLE001  (timeout, DNS, connection reset)
        return {"form_id": fid, "status": "ERROR", "detail": str(e)[:160]}
    if data[:5] != b"%PDF-":
        return {"form_id": fid, "status": "GONE",
                "detail": "response is not a PDF (error/HTML page)"}
    got = verify.sha256_bytes(data)
    if got == entry.get("sha256"):
        return {"form_id": fid, "status": "ok", "sha256": got, "bytes": len(data)}
    return {
        "form_id": fid,
        "status": "CHANGED",
        "expected_sha256": entry.get("sha256"),
        "got_sha256": got,
        "expected_bytes": entry.get("bytes"),
        "got_bytes": len(data),
        "url": url,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect upstream revisions of the blank PDFs")
    ap.add_argument("--forms", help="comma-separated form ids (default: all fetchable)")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--json", action="store_true", help="emit a JSON report")
    ap.add_argument("--update-manifest", action="store_true",
                    help="adopt the new sha256/bytes for CHANGED forms "
                         "(only after the mapping has been re-verified)")
    args = ap.parse_args()

    manifest = verify.load_manifest(MANIFEST)
    entries = {e["form_id"]: e for e in manifest["pdfs"]}

    if args.forms:
        want = [f.strip() for f in args.forms.split(",") if f.strip()]
        unknown = [f for f in want if f not in entries]
        if unknown:
            print(f"unknown form ids (not in manifest): {', '.join(unknown)}")
            return 2
        ids = want
    else:
        ids = [f for f, e in entries.items() if e.get("fetch")]

    results = [check_one(entries[f], args.timeout, args.retries) for f in ids]

    changed = [r for r in results if r["status"] == "CHANGED"]
    gone = [r for r in results if r["status"] == "GONE"]
    errors = [r for r in results if r["status"] == "ERROR"]
    ok = [r for r in results if r["status"] == "ok"]

    if args.json:
        print(json.dumps({"ok": len(ok), "changed": changed, "gone": gone,
                          "errors": errors}, indent=2))
    else:
        for r in results:
            if r["status"] == "ok":
                continue
            if r["status"] == "CHANGED":
                print(f"  CHANGED  {r['form_id']}: upstream PDF revised — "
                      f"{r['got_sha256'][:12]}… (was {(r['expected_sha256'] or '')[:12]}…), "
                      f"{r['got_bytes']} bytes (was {r['expected_bytes']}). "
                      f"Re-enrich before trusting fills.")
            elif r["status"] == "GONE":
                print(f"  GONE     {r['form_id']}: {r.get('detail', 'download failed')}")
            elif r["status"] == "ERROR":
                print(f"  ERROR    {r['form_id']}: {r.get('detail', 'download failed')} "
                      f"(transient — does not gate; re-run)")
            else:
                print(f"  {r['status']:<8} {r['form_id']}")
        print(f"\nok={len(ok)} changed={len(changed)} gone={len(gone)} "
              f"errors={len(errors)} checked={len(results)}")

    if args.update_manifest and changed:
        for r in changed:
            entries[r["form_id"]]["sha256"] = r["got_sha256"]
            entries[r["form_id"]]["bytes"] = r["got_bytes"]
        manifest["pdfs"] = list(entries.values())
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"\nmanifest updated for {len(changed)} form(s). "
              "Re-run enrichment + audit for each before publishing.")

    return 1 if (changed or gone) else 0


if __name__ == "__main__":
    sys.exit(main())
