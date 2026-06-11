# LLP_MLLP-9 — Certificate of Amendment (Domestic Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 23  
**Mapped fields:** 23  
**Filer role:** at least one partner OR any duly authorized person (per page-1 footnote)

## Purpose

Amend the certificate of a Maine domestic Limited Liability Partnership under 31 MRSA §823. Captures (FIRST) a name change with mandatory LLP suffix, (SECOND) a change to the contact partner's name and/or address, and (THIRD) any other amendments via attached exhibit.

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

- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: SECOND captures 'name and or business, residence or mailing address of contact partner' as two widgets (Name 93 / Address 94) but the address is a single combined widget — no street/city split. This is consistent with the contact_partner.address being a free-form combined string.
- Open question: FIRST instructs the filer to write 'no change' literally if the name is not being amended; the schema treats this as a special-cased string sentinel for the rubric. Synth must emit either 'no change' or a valid suffix-bearing name.
- Open question: MLLP-9 introduces filing.signer_entity.* as a non-formation parallel to the per-officer entity-signer pattern (Shape E). Documenting in a schema-gap doc would be useful once a third example arrives.
