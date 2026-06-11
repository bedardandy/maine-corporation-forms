# CORP_REVIVAL — Application for Certificate of Revival

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 38  
**Mapped fields:** 32  
**Filer role:** any duly authorized person (per signature caption '(signature of any duly authorized person)') — typically a former officer, director, member, or partner of the dissolved entity

## Purpose

Apply for a Certificate of Revival to restore a dissolved domestic Maine entity (Nonprofit Corporation, Business Corporation, LLC, or Limited Partnership) to active status. The applicant identifies the entity, the original filing date, the entity type, the clerk/registered agent on record at dissolution, the purposes for revival, the time period needed, and the parties requesting revival.

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

- `revival.entity_type` binds as a single enum_select selecting among 4 option widgets (accepted values: domestic_nonprofit_corp, domestic_business_corp, domestic_llc, domestic_lp).
- `revival.purpose` maps to 4 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: FIFTH section has four physical /Tx widgets (Text5, Text8, Text11, Text10 in y order) for a single conceptual 'purpose' field. Synth/fill must split the value across the four widgets at fill time; rubric should resolve `revival.purpose` as the joined string. Confirm this is the intended pattern (vs. a single-widget /Tx with line wrapping).
- Open question: SEVENTH caps inline at three requesting parties — no exhibit-letter override is provided on the form. If more than three parties exist, the form has no canonical extension point; an attached schedule is the likely workaround but is not formally referenced here.
- Open question: Filer signs as 'any duly authorized person' but the form does not constrain that capacity (no enum), and footnotes do not cite which statute governs who is authorized. Practitioners likely rely on the per-statute revival authority cited in THIRD (e.g., 13-C §1425 for business corps).
- Open question: Header lists '$150.00' for business entity and '$25.00' for nonprofit — fee depends on revival.entity_type. Synth must compute total_fees_dollars from entity_type + expedite_service.
