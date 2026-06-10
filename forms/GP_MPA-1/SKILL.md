# SKILL: Filling GP_MPA-1

**Form:** Statement of Dissociation (General Partnership)  
**Entity type:** General Partnership  
**When to use:** File a Statement of Dissociation under 31 MRSA §1074 recording that a named partner has dissociated from a general partnership. The statement is signed by a partner (individual or entity); signature authority is governed by 31 MRSA §1005.3.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `dissociating_partner.name` | text | high | FIRST: The partner named herein is dissociated from the above named partnership. (Name of Partner) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | Dated ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the partnership name) is non-empty. (depends on `entity.name`)
- dissociating_partner.name is non-empty (the FIRST recital is meaningless without it). (depends on `dissociating_partner.name`)
- Exactly one signer block is populated: either filing.signer.printed_name (individual partner) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) (entity partner). Both blocks empty or both populated is a fill error. (depends on `filing.signer.printed_name`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- If filing.signer_entity.name is populated, filing.signer_entity.signer_printed_name_and_capacity must also be populated. (depends on `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is on or before today. (depends on `filing.date_signed`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name matches entity.name (the partnership being filed for). (depends on `filing.entities[0].name`, `entity.name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "dissociating_partner": {
    "name": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name": "Sample Value"
    },
    "signer_entity": {
      "name": "Sample Value",
      "signer_printed_name_and_capacity": "Sample Value"
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
