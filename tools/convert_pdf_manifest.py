#!/usr/bin/env python3
"""One-shot, reproducible conversion of catalog/pdf_manifest.json to the
shared manifest dialect.

This repo historically forked the manifest format as ``{"pdfs": [{"form_id":
..., ...}, ...]}``; the other three sibling repos — and the shared
``maine-forms-engine`` drift tooling — read ``{"forms": {form_id: {...}}}``
(JSON Schema: ``maine_forms_engine.specs.pdf_manifest_schema()``). This tool
converts in place, losslessly: every entry field except the list-form
``form_id`` (which becomes the key) is preserved, including this repo's
``filename`` and ``fetch`` extras. Idempotent — an already-converted manifest
is left untouched.

    python3 tools/convert_pdf_manifest.py            # convert in place
    python3 tools/convert_pdf_manifest.py --check    # exit 1 if still forked
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "catalog" / "pdf_manifest.json"


def convert(manifest: dict) -> dict:
    """{"pdfs": [...]} -> {"count": N, "forms": {id: {...}}} (lossless)."""
    if "forms" in manifest:
        return manifest  # already the shared dialect
    forms = {}
    for entry in manifest["pdfs"]:
        e = dict(entry)
        fid = e.pop("form_id")
        if fid in forms:
            raise SystemExit(f"duplicate form_id {fid!r} in manifest")
        forms[fid] = e
    return {"count": len(forms), "forms": {k: forms[k] for k in sorted(forms)}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--manifest", type=pathlib.Path, default=MANIFEST)
    ap.add_argument("--check", action="store_true",
                    help="report the dialect, do not write")
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if "forms" in manifest:
        print(f"{args.manifest}: already the shared dialect "
              f"({len(manifest['forms'])} forms)")
        return 0
    if args.check:
        print(f"{args.manifest}: forked {{\"pdfs\": [...]}} dialect")
        return 1
    converted = convert(manifest)
    args.manifest.write_text(
        json.dumps(converted, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"{args.manifest}: converted {converted['count']} entries to the "
          "shared {\"forms\": {...}} dialect")
    return 0


if __name__ == "__main__":
    sys.exit(main())
