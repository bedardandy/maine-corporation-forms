# LP_MLPA-6 — Certificate of Limited Partnership

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 47  
**Mapped fields:** 42  
**Filer role:** all general partners listed in Item Fifth (certificate must be signed by all)

## Purpose

Form a Maine domestic limited partnership under 31 MRSA §1321, including LP name (or LLLP/PLLLP variant), designated-office address, registered agent, list of general partners, and optional series/professional designations.

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

- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `entity.professional_services_description` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Page 1 has 3 individual-signature lines and Page 2 has 3 entity-signature blocks. Is the intent that GPs are split between the two blocks based on whether they're individuals vs entities, or do all 6 slots stack additively when there are >3 GPs total?
- Open question: Page 1 SEVENTH professional-services description is split across two text widgets (Text16, Text17) — fill logic should concatenate them, but confirm whether the form mirrors content automatically or treats them as independent lines.
- Open question: Cover-letter widget for the Immediate expedite tier is named bare 'cover' (not 'cover5') — confirm this is intentional template naming and not a corruption.
