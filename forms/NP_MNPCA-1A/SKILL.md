# SKILL: Filling NP_MNPCA-1A

**Form:** Transfer of Reserved Name (Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Transfer a corporate name previously reserved under 13-B MRSA §302-A.1 to a new transferee, per 13-B MRSA §302-A.2. The unexpired balance of the original 120-day reservation runs in favor of the transferee — the transfer does NOT extend the original 120-day window (page-0 footnote: 'This transfer of reserved name will expire 120 days from the date of filing the original application.'). Records the reserved name (top), original applicant (transferor) name, transferee name and address, signature date, and the transferor's printed name and capacity. Filing fee is $5 per the page-0 header. 2 pages, 20 widgets. Nonprofit analogue of CORP_MBCA-1A.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- name_reservation.name_to_reserve is non-empty. (depends on `name_reservation.name_to_reserve`)
- name_reservation.applicant.name is non-empty (transferor identity). (depends on `name_reservation.applicant.name`)
- name_reservation.transferee.name is non-empty. (depends on `name_reservation.transferee.name`)
- name_reservation.transferee.address is non-empty. (depends on `name_reservation.transferee.address`)
- name_reservation.applicant.printed_name_and_capacity is non-empty (the transferor or any duly authorized person must sign per the page-0 'ORIGINAL APPLICANT (Transferor)' label). (depends on `name_reservation.applicant.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "name_reservation": {
    "name_to_reserve": "Sample Value",
    "applicant": {
      "name": "Sample Value",
      "printed_name_and_capacity": "Sample Value"
    },
    "transferee": {
      "name": "Sample Value",
      "address": "Sample Value"
    }
  },
  "filing": {
    "date_signed": "2026-01-15",
    "entities": [
      {
        "name": "Sample Value"
      },
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
