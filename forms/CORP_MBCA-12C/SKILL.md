# SKILL: Filling CORP_MBCA-12C

**Form:** Application for Transfer of Authority (Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Transfer a foreign business corporation's existing Maine authority into a new authority for a different foreign entity type (nonprofit corporation, LP, LLC, or LLP) following an entity-type conversion in its home jurisdiction or a re-domestication, per 13-C MRSA §1524. The form recites the original home jurisdiction and Maine authorization date, identifies the new entity type and new governing jurisdiction, and bundles the corresponding new Application for Authority (MNPCA-12 / MLPA-12 / MLLC-12 / MLLP-12) per FOURTH.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | FIRST: The current jurisdiction of its incorporation is |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation) |
| `entity.maine_authorization_date` | text | high | and the date on which it was authorized to transact business in the State of Maine is |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty. (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is non-empty and on or before filing.date_signed (cannot transfer authority before being authorized). (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- Exactly one of Check Box1/2/3/4 is set; transfer.new_entity_type resolves to exactly one of the four enum values. (depends on `transfer.new_entity_type`)
- transfer.new_governing_jurisdiction is non-empty. (depends on `transfer.new_governing_jurisdiction`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15"
  },
  "transfer": {
    "new_entity_type": "foreign_limited_liability_company",
    "new_governing_jurisdiction": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities": [
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
