# Provenance

## Blank PDF forms

The blank fillable forms are public records of the **Maine Secretary of State**,
Bureau of Corporations, Elections and Commissions, distributed by the state as
AcroForm PDFs for public use.

To avoid re-hosting them, the blanks are **fetched on demand** rather than
committed. `catalog/pdf_manifest.json` records each form's official source URL,
SHA-256, byte size, and page count; `tools/fetch_pdfs.py` downloads each blank
from the state portal and verifies it byte-for-byte against that hash before
writing it. A download whose hash does not match is rejected.

All 156 blanks are fetched on demand; none is committed to this repository. Where
the state has revised a form's cover/transmittal block since the original
capture, the mapping was re-bound to the **current** blank and re-verified
(every widget reference resolves, no fill failures). For those revised forms the
flat `fields.csv` inventory can still list the originally-captured widget names —
`mapping.json` is the authoritative binding, and `tools/validate_form.py` flags
the lag per form so it is visible, not hidden. Regenerating `fields.csv` from a
freshly fetched blank closes it.

## Field mappings, schemas, and skills

The canonical-key mappings (`mapping.json`), JSON Schemas (`schema.json`),
validation rubrics (`rubric.yaml`), and agent skills (`SKILL.md`) were produced
by **multimodal LLM analysis** of each form — reading the rendered PDF together
with its AcroForm field list to propose a canonical data key, field type, and
confidence for every widget, plus the conditional rules that govern it.

This is **AI-derived metadata**, not an official artifact of the Secretary of
State. Treat it as a strong starting point that still needs human review:

- **Per-field confidence** (`high` / `medium` / `low`) is recorded in every
  `mapping.json` and `fields.csv`. Low-confidence fields need review.
- **Widget validation:** every mapped `widget_id` is cross-checked against the
  real AcroForm field names in the PDF. Mappings that reference a widget the PDF
  lacks, and PDF widgets no mapping covers, are reported per form in
  `docs/STATUS.md`.
- **Known ambiguities** surfaced during analysis (page-null checkbox groups,
  shared-name widgets, missing signature widgets) are recorded in each form's
  `README.md` under "Known ambiguities".

## Verification status

`CORP_MBCA-6` (Articles of Incorporation) has a hand-curated, PDF-validated
mapping and a worked synthetic example; ten forms are hand-maintained in total
(`tools/HAND_MAINTAINED.txt`). All other forms carry generated mappings that have
not yet been individually fill-verified. Run `python3 tools/validate_form.py
--all` for the live per-form review worklist; see `docs/STATUS.md` for the
coverage and mismatch report.

## Experimental sidecars

`catalog/caselaw.json` (case-law background, keyed by transaction category) and
the per-form `statutes.json` are **AI-proposed reference layers**, not citation
lists. Every entry carries `verified=false`: it was located by search and
paraphrased, not read end-to-end from the primary source. They are background
only and must be confirmed against the current Maine Revised Statutes and primary
case law before being relied on. They are not legal advice.

## Not legal advice

Nothing in this repository is legal advice. Filled output is a draft and must be
verified against the official form, and against current Maine law, before filing.
