# CORP_MBCA-1A — Transfer of Reserved Name

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 18  
**Filer role:** the original applicant (transferor) or any duly authorized person signing on the transferor's behalf (per the page-0 'ORIGINAL APPLICANT (Transferor)' signature block label)

## Purpose

Transfer a corporate name previously reserved under 13-C MRSA §402.1 to a new transferee, per 13-C MRSA §402.2. The unexpired balance of the original 120-day reservation runs in favor of the transferee. Records the reserved name (top), original applicant (transferor) name, transferee name and address, signature date, and the transferor's printed name and capacity. Filing fee is $20 per the page-0 header. 2 pages, 20 widgets.

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
- Open question: The transfer does NOT extend the 120-day reservation period (the page-0 footnote: 'This transfer of reserved name will expire 120 days from the date of filing the original application.'). The form does not capture the original reservation date — SOS tracks it via filing record. No additional schema key needed.
- Open question: Form has no widget for the actual signature line — only the typed-name-and-capacity widget. Wet-ink only (same convention as MBCA-1 and other reservation/Shape-D forms).
- Open question: Drafter initially proposed a top-level transfer.* namespace (transfer.original_applicant_name, transfer.transferee_name, transfer.transferee_address) and entity.reserved_name; corrected during review to keep the entire reservation lifecycle under name_reservation.* per MBCA-1 precedent (name_to_reserve, applicant.name, applicant.address, applicant.printed_name_and_capacity).
- Open question: filing.entities[1].name on the cover letter is unlikely to be populated for a name-transfer filing (the form is not bundled with another filing).
