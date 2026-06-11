# CORP_MBCA-21A — Articles of Entity Conversion (Domestic or Foreign Unincorporated Entity → Maine Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 24  
**Mapped fields:** 23  
**Filer role:** officer or other duly authorized representative of the unincorporated entity (signs at bottom of page 0 per 13-C MRSA §955.5)

## Purpose

Convert a domestic or foreign unincorporated entity (LLC, LP, LLLP, GP, etc.) into a Maine business corporation under 13-C MRSA §955.2 (domestic unincorporated → corporation) or §955.3 (foreign unincorporated → corporation). Records the pre-conversion entity name, the new corporate name, foreign-origin info (if applicable), the source-organic-law approval recital, an attached Articles of Incorporation provisions exhibit (Form MBCA-6-1), an optional future effective date, and an authorized signature.

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

- `conversion.approval_type` binds as a single enum_select selecting among 2 option widgets (accepted values: domestic, foreign).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: filing.entities[1].name on the cover letter is likely populated with the bundled MBCA-6-1 (Articles of Incorporation) entity name — analogous to MBCA-21 bundling MLLC-6/MLPA-6. A canonical filing.bundled_forms[] family is not yet defined; tracked via filing.entities[N].name conventionally.
- Open question: Pre-conversion entity type (LLC vs LP vs LLLP vs GP) is not captured by any widget — only implied by THIRD's organic-law reference. A future schema-gap could propose entity.pre_conversion_type if downstream synth/validation needs it explicitly.
- Open question: When converting a foreign unincorporated entity, entity.name (the form's 21a1 widget) may legitimately equal the home-jurisdiction name. There is no second 'home-jurisdiction-name' widget on this form (unlike MLLC-12). Synth should populate entity.name with the foreign-jurisdiction legal name in the foreign-conversion case.
