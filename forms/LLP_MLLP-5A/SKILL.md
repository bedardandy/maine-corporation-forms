# SKILL: Filling LLP_MLLP-5A

**Form:** Termination of Statement of Intention to Do Business Under an Assumed or Fictitious Name (LLP)  
**Entity type:** Limited Liability Partnership  
**When to use:** Terminate a previously filed Statement of Intention to do Business Under an Assumed or Fictitious Name for a Maine Limited Liability Partnership under 31 MRSA §805-A.8 and §860-A. Captures the LLP's real name, the assumed/fictitious name being terminated, and a single signer block (individual partner OR entity partner).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Real Name of Limited Liability Partnership) |
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

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the LLP's real name) is non-empty. (depends on `entity.name`)
- filing.terminated_fictitious_name is non-empty (the SECOND recital identifies which name is being terminated). (depends on `filing.terminated_fictitious_name`)
- filing.terminated_fictitious_name is different from entity.name (a fictitious-name termination is meaningless if the names match). (depends on `filing.terminated_fictitious_name`, `entity.name`)
- Exactly one signer block is populated: either filing.signer.printed_name_and_capacity (individual partner) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) (entity partner). Both blocks empty or both populated is a fill error. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- If filing.signer_entity.name is populated, filing.signer_entity.signer_printed_name_and_capacity must also be populated (and vice versa). (depends on `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "filing": {
    "terminated_fictitious_name": "Sample Value",
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
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
