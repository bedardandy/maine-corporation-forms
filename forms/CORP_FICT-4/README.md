# CORP_FICT-4 — Statement of Intention to do Business under a Fictitious Name

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** duly authorized officer/manager/partner of the foreign entity per the form's signature footnotes

## Purpose

Foreign-entity-only filing declaring intent to transact business in Maine under a fictitious name when the entity's real name is unavailable in Maine. Used by foreign corporations, LLCs, LPs, LLPs, and nonprofits.

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
- Open question: All concepts on this form are already proposed elsewhere in the batch (entity.home_jurisdiction_name and entity.maine_fictitious_name from MLLC-12, entity.maine_authorization_date from CLKRA-3). No new schema gaps unique to FICT-4. Confirm dedup at aggregation time.
- Open question: Field NAMES on page 0 are auto-generated descriptive labels ('Exact Legal Name of Entity...', 'and the date on which', 'undefined', 'undefined_2', 'type or print name', 'title of signer'). This template style is unique among the batch — confirm it isn't a problem for downstream PDF-fill libraries that key on field names.
- Open question: FICT-4 is bundled with MLLC-12 (when foreign-LLC's home name is unavailable) per Check Box4 on MLLC-12. Confirm canonical bundling logic: when a foreign-qualification filing references FICT-4, both forms share entity.home_jurisdiction_name and entity.maine_fictitious_name.
