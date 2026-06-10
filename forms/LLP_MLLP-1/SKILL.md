# SKILL: Filling LLP_MLLP-1

**Form:** Application for Reservation of Name (Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Reserve a name for a Limited Liability Partnership (LLP) in Maine for 120 days under 31 MRSA §804-A.1, prior to filing the LLP's qualification statement. Optional election to reserve the name as an assumed/fictitious name (exempt from the LLP suffix requirement).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `applicant.address` | text | high | Address of applicant ___ |
| `applicant.name` | text | high | Name of applicant ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | [full-width line above the '(2003-A.1 - Name to be reserved must contain one of the following: "Limited Liability Partnership", "L.L.P." or "LLP" unless this name is being reserved for use only as an assumed name)' footnote] |
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

- entity.name (the LLP name being reserved) is non-empty. (depends on `entity.name`)
- If filing.is_assumed_name_reservation is false, entity.name must contain a statutory LLP suffix (case-insensitive substring): 'Limited Liability Partnership', 'L.L.P.', or 'LLP'. If true, no suffix required. (depends on `entity.name`, `filing.is_assumed_name_reservation`)
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
    "entities": [
      {
        "name": "Sample Value"
      },
      {
        "name": "Sample Value"
      }
    ]
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
