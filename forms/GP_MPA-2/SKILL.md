# SKILL: Filling GP_MPA-2

**Form:** Statement of Dissolution (General Partnership)  
**Entity type:** General Partnership  
**When to use:** File a Statement of Dissolution under 31 MRSA §1085 declaring that a Maine general partnership has dissolved and is winding up its business. Recites the partnership name (FIRST), the dissolution-and-winding-up declaration (SECOND), and an under-penalty-of-perjury attestation (THIRD); signed on page 0 by an authorized partner per 31 MRSA §1005.3 (individual or entity-partner).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | FIRST: The name of the partnership is |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | Dated ____ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity(s) on the submitted filings [2] |

_Showing 12 of 19 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the partnership name) is non-empty. (depends on `entity.name`)
- Exactly one signer block is populated: either filing.signer.printed_name (individual partner) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) (entity partner). Both empty or both populated is a fill error. (depends on `filing.signer.printed_name`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- If filing.signer_entity.name is populated, filing.signer_entity.signer_printed_name_and_capacity must also be populated. (depends on `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name matches entity.name (the partnership being filed for). (depends on `filing.entities[0].name`, `entity.name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
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
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    },
    "expedited_service": "Sample Value"
  }
}
```
