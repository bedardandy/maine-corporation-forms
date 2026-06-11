# LP_MLPA-1A — Notice of Transfer of Reserved Name (Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** the original applicant (Transferor) who is transferring the reserved name to the transferee. Reuses the applicant.* role from LP_MLPA-1 (Application for Reservation of Name) — the entity still does not exist at the moment of transfer (a reservation is not an entity), so the signer is the original applicant in their own capacity, not an entity officer. The transferee is captured under a separate transferee.* role prefix.

## Purpose

Transfer a previously reserved limited partnership name from the original applicant to a new transferee under 31 MRSA §1309.1.C. Captures the previously-reserved name, the original applicant (transferor), the transferee's name and address, and the transferor's signature/date. The 120-day reservation window runs from the original application date and is not renewed by this transfer.

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
- Open question: The form has a separate '(signature of transferor)' line with no AcroForm widget — wet-signature only. Text18 ('type or print name and capacity') is the sole digital signer-block field. Consistent with LP_MLPA-1 and other LP/LLC forms.
- Open question: filing.entities[1].name on the cover letter is unused for a single-name transfer; left available for filers bundling multiple notices.
- Open question: 31 MRSA §1309.1.C governs the transfer mechanism; the 120-day reservation window runs from the original application date and is not extended by this transfer (form footnote: 'This transfer of reserved name will expire 120 days from the date of filing the original application').
