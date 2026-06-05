# LP_MLPA-11C — Statement of Termination (Domestic Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 23  
**Mapped fields:** 21  
**Filer role:** all general partners (individuals and/or authorized representatives of entity general partners) — § 1323 requires signature by all GPs

## Purpose

Terminate a Maine domestic limited partnership pursuant to 31 MRSA §1323. Records the original certificate filing date, optional additional information via exhibit, and the signatures of all general partners (individuals or authorized representatives of entity GPs) winding up the partnership.

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
- Open question: The form has 3 inline rows for individual GPs (Text5–7) but only 1 entity-GP block (Text8–9). LP_MLPA-6 (formation) gave 3+3. Termination filings with >1 entity-GP presumably use Text3's 'additional information' exhibit, but the form has no explicit overflow checkbox — confirm whether multiple entity GPs are expected to attach a separate exhibit or stacked-signature page.
- Open question: Text3 (additional-info exhibit letter) has no opt-in checkbox; it's a bare blank. Synth should leave it empty when no exhibit is attached (omitted is the default state).
- Open question: Cover-letter immediate-tier widget is the bare name 'cover' rather than 'cover5' — same upstream naming quirk seen on LP_MLPA-6; preserved verbatim.
