# SKILL: Filling NP_MNPCA-1

**Form:** Application for Reservation of Name (Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Reserve a corporate name for a prospective Maine nonprofit corporation for 120 days under 13-B MRSA §302-A.1. The reservation does not form the entity; it only secures availability of the name. The reservation is non-renewable.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `applicant.address` | text | high | Address of applicant |
| `applicant.name` | text | high | Name of applicant |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name to be reserved) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED |

_Showing 12 of 19 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the name to be reserved) is non-empty. (depends on `entity.name`)
- applicant.name is non-empty. (depends on `applicant.name`)
- applicant.address is non-empty. (depends on `applicant.address`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name equals entity.name (the name being reserved appears on the cover letter). (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "applicant": {
    "name": "Sample Value",
    "address": "Sample Value"
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
    },
    "expedited_service": {}
  }
}
```
