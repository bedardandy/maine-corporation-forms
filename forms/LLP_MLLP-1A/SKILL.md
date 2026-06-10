# SKILL: Filling LLP_MLLP-1A

**Form:** Transfer of Reserved Name (Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Transfer a previously reserved Limited Liability Partnership name from the original applicant (transferor) to a new transferee under 31 MRSA §804-A.2. Records the reserved name, the original applicant's name, the transferee's name and address, signature date, and the transferor's printed name and capacity. Filing fee is $20 per the page-0 header. Per the page-0 footnote, the transfer is valid only for the remaining 120-day window from the original reservation's filing date. 2 pages, 20 widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.reserved_name` | text | high | (Name previously reserved pursuant to §804-A.1) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity(s) on the submitted filings [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.reserved_name is non-empty. (depends on `entity.reserved_name`)
- name_reservation.original_applicant.name is non-empty (transferor identity). (depends on `name_reservation.original_applicant.name`)
- name_reservation.transferee.name is non-empty. (depends on `name_reservation.transferee.name`)
- name_reservation.transferee.address is non-empty. (depends on `name_reservation.transferee.address`)
- name_reservation.transferee.name differs from name_reservation.original_applicant.name (a transfer to oneself is vacuous). (depends on `name_reservation.original_applicant.name`, `name_reservation.transferee.name`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.expedited_service is exactly one of hold_for_pickup | 24h_next_business_day | immediate_same_day. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "reserved_name": "Wabanaki Widgets, Inc."
  },
  "name_reservation": {
    "original_applicant": {
      "name": "Sample Value"
    },
    "transferee": {
      "name": "Sample Value",
      "address": "Sample Value"
    }
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    }
  }
}
```
