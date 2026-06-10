# SKILL: Filling LLC_MLLC-1

**Form:** Application for Reservation of Name (Limited Liability Company)  
**Entity type:** Limited Liability Company  
**When to use:** Reserve a name for a Maine limited liability company (domestic or foreign) for 120 days under 31 MRSA §1509.1 prior to filing a formation or qualification document. Optional election to reserve the name as an assumed/fictitious name (exempt from the LLC suffix requirement per 31 MRSA §1508).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `applicant.address` | text | high | Address of applicant ___ |
| `applicant.name` | text | high | Name of applicant ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | [full-width line above the '(Name to be reserved must contain...)' footnote] |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ___ |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the name being reserved) is non-empty. (depends on `entity.name`)
- If filing.is_assumed_name_reservation is false, entity.name must contain a statutory LLC suffix (case-insensitive substring): 'Limited Liability Company', 'Limited Company', 'L.L.C.', 'LLC', 'L.C.', 'LC', 'L3C', or 'l3c' (per 31 MRSA §1508). If true, no suffix required. (depends on `entity.name`, `filing.is_assumed_name_reservation`)
- applicant.name is non-empty. (depends on `applicant.name`)
- applicant.address is non-empty. (depends on `applicant.address`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future relative to the submission date. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (per cover-letter NOTE). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "filing": {
    "is_assumed_name_reservation": true,
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
  },
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "applicant": {
    "name": "Sample Value",
    "address": "Sample Value"
  }
}
```
