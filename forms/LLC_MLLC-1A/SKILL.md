# SKILL: Filling LLC_MLLC-1A

**Form:** Transfer of Reserved Name (LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Transfer a previously reserved LLC name from the original applicant (transferor) to a new transferee under 31 MRSA §1509.2. Records the reserved name, the original applicant's name, the transferee's name and address, and the transferor's signature. Per the page-0 note, the transfer is valid only for the remaining 120-day reservation window from the original application's filing date.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.reserved_name` | text | high | (Name previously reserved pursuant to 31 MRSA §1509.1) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity(s) on the submitted filings [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.reserved_name is non-empty. (depends on `entity.reserved_name`)
- name_reservation.original_applicant.name is non-empty. (depends on `name_reservation.original_applicant.name`)
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
