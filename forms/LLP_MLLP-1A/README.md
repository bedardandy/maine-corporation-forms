# LLP_MLLP-1A — Transfer of Reserved Name (Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** the original applicant (transferor) or any duly authorized person signing on the transferor's behalf (per the page-0 'ORIGINAL APPLICANT (Transferor)' / '(signature of any duly authorized person)' label). Single-signer Shape D — printed name and capacity combined in one widget.

## Purpose

Transfer a previously reserved Limited Liability Partnership name from the original applicant (transferor) to a new transferee under 31 MRSA §804-A.2. Records the reserved name, the original applicant's name, the transferee's name and address, signature date, and the transferor's printed name and capacity. Filing fee is $20 per the page-0 header. Per the page-0 footnote, the transfer is valid only for the remaining 120-day window from the original reservation's filing date. 2 pages, 20 widgets.

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
- Open question: The transfer does NOT extend the 120-day reservation period (page-0 footnote: 'This transfer of reserved name will expire 120 days from the date of filing the original application.'). The form does not capture the original reservation's filing date — SOS tracks it via the filing record. No additional canonical key required.
- Open question: Form has a wet-ink-only '(signature of any duly authorized person)' line on page 0 (left of the typed-name-and-capacity widget). No AcroForm /Tx widget binds to it — synth produces no value, and the rubric does not check for it. The typed name-and-capacity widget is the canonical signer evidence.
- Open question: The transferee's consent is not collected on this form (no transferee signature widget). Practically the transferee submits their own subsequent formation paperwork; this form only memorializes the transferor's release. No additional canonical keys required.
- Open question: Drafter initially proposed a top-level transfer.* namespace (transfer.transferor.name, transfer.transferee.{name,address}); corrected during review to the existing name_reservation.original_applicant.* / name_reservation.transferee.* keys per MLLC-1A precedent (the predecessor form noted that 'sibling forms (e.g., MLPA-1A, MLLP-1A) likely follow this same shape with parallel name_reservation.* keys').
