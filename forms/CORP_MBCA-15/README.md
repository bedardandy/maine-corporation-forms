# CORP_MBCA-15 — Application for the Use of an Indistinguishable Name

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 18  
**Filer role:** duly authorized officer of the consenting corporation (per the page-0 footnote: 'This document MUST be signed by any duly authorized officer'). Single-signer Shape D — printed name and capacity combined in one widget.

## Purpose

Allow a Maine business corporation that holds rights to a name to consent to another applicant's use of an indistinguishable name under 13-C MRSA §401.4. The consenting corporation simultaneously commits to changing its own name to a distinguishable form. Per the form's footnote, this application MUST be accompanied by the applicable name-change form (Articles of Amendment, MBCA-9) carrying the new distinguishable name.

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
- Open question: Page-0 footnote states 'This application must be accompanied by the applicable form to change its name as provided in Item Third.' That accompanying form is typically Articles of Amendment (CORP_MBCA-9) carrying entity.new_distinguishable_name as the new corporate name. Synth at full-roundtrip should bundle MBCA-15 + MBCA-9 with consistent entity.new_distinguishable_name across both filings; this can be enforced as an inter-form rubric check at v1.
- Open question: The 'SECOND' clause appears as static text (no widgets) — it states 'The entity in possession of the name undertakes to change to a name that is distinguishable on the records of the Secretary of State from the name of the applicant.' Captured implicitly by the THIRD widget (entity.new_distinguishable_name).
- Open question: Per the MBCA-9 cross-reference, the 'consenting corporation' must amend its articles to reflect the new name BEFORE the requestor's name application is granted. This is a sequencing requirement enforced procedurally by SOS staff, not a per-form rubric concern.
