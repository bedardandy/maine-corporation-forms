#!/usr/bin/env python3
"""Extract printed filing-fee amounts from the blank PDFs into catalog/fees.json.

Fee policy (never fabricate legal data): an ``amount`` is stored **only when it
is literally printed on the blank form** as an unconditional base filing fee
("Filing Fee $145.00", "$5.00 Filing Fee", or "Filing Fee $90.00 - (If amending
ONLY ... $35.00)" where the base amount is unambiguous). Forms that print *no*
fee, or only conditional/tiered fees (per-month registration fees, per-class
mark fees, domestic-vs-foreign or for-profit-vs-nonprofit tiers, fee tables),
get ``amount: null`` plus the verbatim printed lines so an agent can read the
conditions itself. ``"No Filing Fee"`` printed on the form is stored as 0.0.
Never recall fee amounts from memory or the web — the SoS fee schedule governs.

Every PDF is verified against ``catalog/pdf_manifest.json`` (SHA-256) before
its text is trusted; drifted or missing PDFs fail the run (fetch first with
``python3 tools/fetch_pdfs.py``).

    python3 tools/extract_fees.py             # all forms -> catalog/fees.json
    python3 tools/extract_fees.py CORP_MBCA-6 # update a subset in place
    python3 tools/extract_fees.py --dry-run   # print, don't write
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "catalog" / "pdf_manifest.json"
OUT = ROOT / "catalog" / "fees.json"

# Lines that mention a fee but are boilerplate or blank-total labels, not the
# form's own filing fee. The expedite block is printed on nearly every form.
_EXCLUDE = re.compile(
    r"additional filing fee per entity|expedite|fee\(s\) enclosed",
    re.IGNORECASE)
_MENTION = re.compile(r"filing fee|no fee required", re.IGNORECASE)
_NO_FEE = re.compile(r"^\s*no (?:filing )?fee(?: required)?\.?\s*$",
                     re.IGNORECASE)
_AMOUNT = r"\$\s?(\d[\d,]*(?:\.\d{2})?)"
# Unconditional base fee, optionally followed by a parenthesized reduced-scope
# variant ("- (If amending ONLY Item FOURTH ... $35.00)") that is also printed.
_BASE = [
    re.compile(rf"^\s*filing fee {_AMOUNT}\.?\s*$", re.IGNORECASE),
    re.compile(rf"^\s*{_AMOUNT} filing fee\s*$", re.IGNORECASE),
    re.compile(rf"^\s*filing fee {_AMOUNT}\.?\s*[-–]?\s*\(if\b.*$",
               re.IGNORECASE),
]
_REV = re.compile(r"Rev\.?\s*(\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}/\d{2,4})")


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _pdf_texts(path: pathlib.Path) -> list[str]:
    """Extract text with every available extractor (pypdf, PyMuPDF).

    The two engines miss different lines (pypdf drops some positioned text
    that PyMuPDF sees, e.g. the fee box on MBCA-12), so the scan runs over
    the union. At least one extractor is required; install ``pymupdf`` too
    before regenerating the committed catalog so no printed fee is missed.
    """
    texts = []
    try:
        from pypdf import PdfReader
        texts.append("\n".join((p.extract_text() or "")
                               for p in PdfReader(path).pages))
    except ImportError:
        pass
    try:
        import fitz  # PyMuPDF
        with fitz.open(path) as doc:
            texts.append("\n".join(p.get_text() for p in doc))
    except ImportError:
        pass
    if not texts:
        raise SystemExit("need pypdf and/or pymupdf installed")
    return texts


def _rev_key(rev: str):
    parts = [int(p) for p in rev.split("/")]
    if len(parts) == 2:
        m, y = parts
        d = 1
    else:
        m, d, y = parts
    if y < 100:
        y += 2000
    return (y, m, d)


def _fee_lines(texts: list[str]) -> list[str]:
    lines = []
    for text in texts:
        for raw in text.splitlines():
            line = re.sub(r"\s+", " ", raw).strip()
            if line and _MENTION.search(line) and not _EXCLUDE.search(line):
                lines.append(line)
    # de-dup while preserving order (pages and extractors repeat lines)
    seen, out = set(), []
    for line in lines:
        if line not in seen:
            seen.add(line)
            out.append(line)
    return out


def extract_one(texts: list[str]) -> dict:
    lines = _fee_lines(texts)
    revs = sorted({r for t in texts for r in _REV.findall(t)}, key=_rev_key)
    entry = {
        "amount": None,
        "currency": None,
        "source": None,
        "note": None,
        "printed_lines": lines,
        "revision": revs[-1] if revs else None,
    }
    if len(revs) > 1:
        entry["revisions"] = revs

    base_amounts = set()
    for line in lines:
        for pat in _BASE:
            m = pat.match(line)
            if m:
                base_amounts.add(float(m.group(1).replace(",", "")))
                break

    if any(_NO_FEE.match(line) for line in lines):
        entry.update(amount=0.0, currency="USD", source="printed on form",
                     note="form states no filing fee")
    elif len(base_amounts) == 1:
        entry.update(amount=base_amounts.pop(), currency="USD",
                     source="printed on form")
        if len(lines) > 1:
            entry["note"] = ("additional fee provisions are printed on the "
                             "form; see printed_lines")
    elif lines:
        entry["note"] = ("fee is conditional or tiered as printed on the "
                         "form (see printed_lines); verify against the SoS "
                         "fee schedule")
    else:
        entry["note"] = ("no filing fee amount printed on the form; see the "
                         "SoS fee schedule")
    return entry


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("forms", nargs="*", help="form ids (default: all)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    manifest = {p["form_id"]: p
                for p in json.loads(MANIFEST.read_text())["pdfs"]}
    targets = args.forms or sorted(manifest)
    unknown = [f for f in targets if f not in manifest]
    if unknown:
        ap.error(f"not in pdf_manifest.json: {', '.join(unknown)}")

    fees = {}
    if OUT.exists():
        fees = json.loads(OUT.read_text()).get("fees", {})

    problems = []
    for form_id in targets:
        meta = manifest[form_id]
        pdf = ROOT / "forms" / form_id / meta["filename"]
        if not pdf.exists():
            problems.append(f"{form_id}: blank PDF missing "
                            "(python3 tools/fetch_pdfs.py)")
            continue
        if _sha256(pdf) != meta["sha256"]:
            problems.append(f"{form_id}: SHA-256 drift vs pdf_manifest.json "
                            "— refusing to extract from an unverified PDF")
            continue
        fees[form_id] = extract_one(_pdf_texts(pdf))

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1

    n_amount = sum(1 for e in fees.values()
                   if e["amount"] not in (None, 0.0))
    n_zero = sum(1 for e in fees.values() if e["amount"] == 0.0)
    n_cond = sum(1 for e in fees.values()
                 if e["amount"] is None and e["printed_lines"])
    n_none = sum(1 for e in fees.values()
                 if e["amount"] is None and not e["printed_lines"])
    doc = {
        "_meta": {
            "tool": "tools/extract_fees.py",
            "method": ("deterministic scan of each SHA-verified blank PDF's "
                       "text (union of pypdf + PyMuPDF extraction) for "
                       "printed filing-fee language; amounts are stored only "
                       "when literally printed as an unconditional base fee"),
            "currency": "USD",
            "note": ("amount=null means the form prints no single "
                     "unconditional fee — read printed_lines and verify "
                     "against the Maine SoS fee schedule; never guess"),
            "coverage": {
                "printed_unconditional": n_amount,
                "printed_no_fee": n_zero,
                "printed_conditional": n_cond,
                "none_printed": n_none,
            },
        },
        "fees": {k: fees[k] for k in sorted(fees)},
    }
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if args.dry_run:
        print(text)
    else:
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)}: "
              f"{n_amount} printed fee(s), {n_zero} no-fee, "
              f"{n_cond} conditional, {n_none} none printed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
