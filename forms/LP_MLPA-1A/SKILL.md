# SKILL: Filling LP_MLPA-1A

**Form:** Notice of Transfer of Reserved Name (Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Transfer a previously reserved limited partnership name from the original applicant to a new transferee under 31 MRSA §1309.1.C. Captures the previously-reserved name, the original applicant (transferor), the transferee's name and address, and the transferor's signature/date. The 120-day reservation window runs from the original application date and is not renewed by this transfer.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `applicant.name` | text | high | Name of original applicant |
| `applicant.printed_name_and_capacity` | text | high | (type or print name and capacity) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name previously reserved pursuant to 31 MRSA §1309.1) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED |

## Conditional logic

- entity.name (the previously-reserved name being transferred) is non-empty. (depends on `entity.name`)
- applicant.name (the transferor / original applicant) is non-empty. (depends on `applicant.name`)
- transferee.name is non-empty. (depends on `transferee.name`)
- transferee.address is non-empty. (depends on `transferee.address`)
- applicant.printed_name_and_capacity (the transferor's printed name + capacity) is non-empty. (depends on `applicant.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name equals entity.name (the reserved string being transferred). (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "applicant": {
    "name": "Sample Value",
    "printed_name_and_capacity": "Sample Value"
  },
  "transferee": {
    "name": "Sample Value",
    "address": "Sample Value"
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
