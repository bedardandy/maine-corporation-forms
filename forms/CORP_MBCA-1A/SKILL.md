# SKILL: Filling CORP_MBCA-1A

**Form:** Transfer of Reserved Name  
**Entity type:** Business Corporation  
**When to use:** Transfer a corporate name previously reserved under 13-C MRSA §402.1 to a new transferee, per 13-C MRSA §402.2. The unexpired balance of the original 120-day reservation runs in favor of the transferee. Records the reserved name (top), original applicant (transferor) name, transferee name and address, signature date, and the transferor's printed name and capacity. Filing fee is $20 per the page-0 header. 2 pages, 20 widgets.

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
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    }
  }
}
```
