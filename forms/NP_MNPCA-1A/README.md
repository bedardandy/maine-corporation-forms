# NP_MNPCA-1A — Transfer of Reserved Name (Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 18  
**Filer role:** the original applicant (transferor) or any duly authorized person signing on the transferor's behalf (per the page-0 'ORIGINAL APPLICANT (Transferor)' signature block label)

## Purpose

Transfer a corporate name previously reserved under 13-B MRSA §302-A.1 to a new transferee, per 13-B MRSA §302-A.2. The unexpired balance of the original 120-day reservation runs in favor of the transferee — the transfer does NOT extend the original 120-day window (page-0 footnote: 'This transfer of reserved name will expire 120 days from the date of filing the original application.'). Records the reserved name (top), original applicant (transferor) name, transferee name and address, signature date, and the transferor's printed name and capacity. Filing fee is $5 per the page-0 header. 2 pages, 20 widgets. Nonprofit analogue of CORP_MBCA-1A.

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
- Open question: Form has no widget for the actual signature line — only the typed-name-and-capacity widget. Wet-ink only (same convention as NP_MNPCA-1, CORP_MBCA-1A, and other reservation/Shape-D forms).
- Open question: Drafter initially proposed entity.reserved_name + a top-level transfer.* namespace (transfer.original_applicant_name, transfer.transferee_name, transfer.transferee_address) and filing.signer.printed_name_and_capacity; corrected during review to keep the entire reservation lifecycle under name_reservation.* per NP_MNPCA-1 / CORP_MBCA-1A precedent (name_to_reserve, applicant.name, applicant.address, applicant.printed_name_and_capacity, transferee.name, transferee.address).
- Open question: filing.entities[1].name on the cover letter is unlikely to be populated for a name-transfer filing (the form is not bundled with another filing).
- Open question: Statutory citation 13-B MRSA §302-A.2 is the nonprofit equivalent of 13-C §402.2 (used by CORP_MBCA-1A). Schema keys are shared across both Title 13-B and Title 13-C reservation transfers — only the rubric statute citations differ.
