# LLC_MLLC-6A — Restated Certificate of Formation (Maine LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 32  
**Mapped fields:** 27  
**Filer role:** authorized person(s) of the LLC (per 31 MRSA §1676.1.B); up to three parallel signature slots are provided on page 1

## Purpose

File a Restated Certificate of Formation for an existing Maine LLC under 31 MRSA §1532, integrating prior amendments (and optional new amendments) into a single restated document. Records the LLC's current SOS-record name, the post-restatement name (or 'no change'), the original certificate-of-formation date, optional low-profit (L3C) and professional-LLC designations, the registered-agent block, an optional restatement-amendments exhibit, and per-officer signatures by up to three authorized persons.

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

- `entity.name` maps to 2 widgets; all receive the same value.
- `registered_agent.type` maps to 2 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Both 'name' (top, current SOS-record name) and 'new name' (FIRST blank) bind to entity.name. For synth fills with no name change, populate both with the same value; for actual name-change filings, the 'new name' value would diverge from the SOS record. An optional entity.name_changed boolean could disambiguate at the rubric level — deferred until a synth demo for name-change scenarios is added.
- Open question: Field-id 'name and capacity 3' (with internal space before the digit) differs from 'name and capacity1' / 'name and capacity2' (no space). Filler must preserve the literal field-id including whitespace.
- Open question: Check Box4 (low-profit LLC) has no accompanying free-text description of charitable/educational purpose, unlike some other low-profit forms. The §1611 qualifications A–D are statutory and do not require an inline explanation on the form. No proposed schema gap needed.
- Open question: SEVENTH 'Other matters' exhibit letter (entity.restatement_amendments_exhibit_letter) is the only place on the form to capture the actual restatement substance — restated articles are attached as the named exhibit. Synth must produce a letter even when no other matters are amended (form requires the field to be filled when the exhibit is attached).
