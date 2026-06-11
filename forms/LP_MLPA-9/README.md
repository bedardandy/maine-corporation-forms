# LP_MLPA-9 — Certificate of Amendment (Domestic Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 5  
**Fields:** 71  
**Mapped fields:** 69  
**Filer role:** general partner(s) or authorized signatory(ies) depending on the specific amendment item (see signature footnotes on page 3)

## Purpose

Amend the certificate of a domestic limited partnership under 31 MRSA §1322. Covers name changes, LLLP status elections, professional LLLP elections, changes to general partners (additions, dissociations, replacements, address/name changes), dissolution, and other amendments.

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
- `entity.is_lllp` binds as a single enum_select selecting among 2 option widgets (accepted values: True, true, yes, False, false, no).
- `entity.professional_services_description` maps to 2 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: The form has two unnamed checkboxes on page 4 (y≈607 and y≈620) that appear to be the 24h and immediate expedite options. Confirm their exact enum values and whether they follow the standard 'Check Box15'/'Check Box16' naming or are truly unnamed.
- Open question: The signature block on page 2 has three rows of individual signatories and three rows of entity signatories on page 3. The form footnotes specify different signing requirements per amendment item (e.g., Item Third requires ALL general partners). Should the rubric enforce a minimum number of signatories based on the amendment type, or is that too complex for pass-1?
- Open question: Text8 on page 0 is a second line for professional services description. Should this be merged with Text7 into a single canonical key, or kept separate? The form visually presents them as one multi-line field.
