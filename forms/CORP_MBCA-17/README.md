# CORP_MBCA-17 — Articles of Correction (Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 23  
**Mapped fields:** 21  
**Filer role:** any duly authorized officer OR the clerk of the corporation (per 13-C MRSA §121.5; the page-2 footnote restates this requirement)

## Purpose

Correct an inaccurate or defectively executed corporate filing previously delivered to the Maine Secretary of State under 13-C MRSA §126. Identifies the original filing (document name + filing date), describes the inaccuracy or defect, and supplies the corrected text. Applies to both domestic and foreign business corporations (SEVENTH captures the foreign-corp jurisdiction + Maine-authorization-date when applicable). Filing fee $50. Per SIXTH, the correction is effective retroactively to the original document's effective date except as to persons who relied on the uncorrected document and were adversely affected.

## Field mapping

This directory contains a machine-readable mapping between canonical data keys and the PDF's AcroForm widget names.

| File | Purpose |
|------|---------|
| `form.yaml` | Form metadata |
| `mapping.json` | canonical_key to widget mapping |
| `schema.json` | JSON Schema for fill data |
| `fields.csv` | Flat field inventory |
| `rubric.yaml` | Validation checks |
| `README.md` | This file |
| `SKILL.md` | Agent fill guidance |

## Known ambiguities

- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: The (signature of any duly authorized person) line on page 1 is wet-ink only — no AcroForm widget. Synth fills should populate filing.signer.printed_name_and_capacity but cannot fill the signature line itself.
- Open question: SIXTH paragraph (retroactive-effect recital) has no widgets — it is a fixed statutory recital and doesn't require filer input. Same shape as LLC_MLLC-17's FIFTH retroactive-effect recital.
- Open question: THIRD paragraph also has no widgets — it is a fixed recital that lists the eligible types of defects (inaccurate record, defective execution, attestation, sealing, verification, acknowledgement, or electronic transmission). The selection of which defect applies is captured implicitly in correction.error_description rather than as a structured enum.
- Open question: SEVENTH's two underlined blanks are bound to AcroForm widgets with awkward auto-generated names ('and the date on which' for the jurisdiction blank; 'undefined_2' for the maine-authorization-date blank). The filler engine binds these by /T name; rubric reads the canonical keys.
- Open question: The form serves both Maine domestic and foreign corporations. For foreign-corp corrections, entity.name should be the home-jurisdiction name (the name on file with Maine SOS, which is either the home name or a fictitious-Maine-name registered via FICT-4). entity.home_jurisdiction_name is not used here — same convention as LLC_MLLC-17.
