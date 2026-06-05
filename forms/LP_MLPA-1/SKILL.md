# SKILL: Filling LP_MLPA-1

**Form:** Application for Reservation of Name (Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Reserve a name for a Limited Partnership in Maine for 120 days under 31 MRSA §1309.1. Captures the name being reserved, the applicant's name and address, the applicant's signature, and an opt-in checkbox indicating the name is being reserved as an assumed name (relaxes the entity-suffix requirement).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `applicant.address` | text | high | Address of applicant |
| `applicant.name` | text | high | Name of applicant |
| `applicant.printed_name_and_capacity` | text | high | (signature of applicant) / (type or print name and capacity) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name to be reserved must contain one of the following: 'Limited Partnership', 'L.P.' or 'LP' unless this name is being reserved for use only as an assumed name) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

## Conditional logic

- entity.name (the name being reserved) is non-empty. (depends on `entity.name`)
- If reservation.is_assumed_name is false, entity.name must contain one of: 'Limited Partnership', 'L.P.', 'LP' (case-insensitive). 31 MRSA §1305 entity-suffix requirement; relaxed when the name is reserved as assumed. (depends on `entity.name`, `reservation.is_assumed_name`)
- applicant.name is non-empty. (depends on `applicant.name`)
- applicant.address is non-empty. (depends on `applicant.address`)
- applicant.printed_name_and_capacity is non-empty. (depends on `applicant.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name equals entity.name (the reserved string). (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "applicant": {
    "name": "Sample Value",
    "address": "Sample Value",
    "printed_name_and_capacity": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    }
  },
  "reservation": {
    "is_assumed_name": true
  }
}
```
