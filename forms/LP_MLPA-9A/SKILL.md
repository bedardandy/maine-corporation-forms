# SKILL: Filling LP_MLPA-9A

**Form:** Statement of Withdrawal of a Limited Partner  
**Entity type:** Limited Partnership  
**When to use:** Record the withdrawal of a limited partner from a Maine limited partnership pursuant to 31 MRSA §1346.1.B. The form captures the partnership name, the withdrawing limited partner's name, and a signature block with two parallel paths: an individual-limited-partner block (printed name) and an entity-limited-partner block (entity name + signer printed-name-and-capacity for the natural person signing on the entity's behalf).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Limited Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | Dated ____ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the limited partnership) is non-empty. (depends on `entity.name`)
- withdrawing_limited_partner.name (the recital identifying who is withdrawing) is non-empty. (depends on `withdrawing_limited_partner.name`)
- Exactly one of the two signer blocks is populated: either withdrawing_limited_partner.printed_name (individual) OR withdrawing_limited_partner_entity.name + withdrawing_limited_partner_entity.signer_printed_name_and_capacity (entity). Filling both is structurally inconsistent. (depends on `withdrawing_limited_partner.printed_name`, `withdrawing_limited_partner_entity.name`, `withdrawing_limited_partner_entity.signer_printed_name_and_capacity`)
- If withdrawing_limited_partner_entity.name is set, withdrawing_limited_partner_entity.signer_printed_name_and_capacity must also be set (an entity cannot sign without identifying the natural person signing for it). (depends on `withdrawing_limited_partner_entity.name`, `withdrawing_limited_partner_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name equals entity.name (the partnership). (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "withdrawing_limited_partner": {
    "name": "Sample Value",
    "printed_name": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "entities": [
      {
        "name": "Sample Value"
      },
      {
        "name": "Sample Value"
      }
    ]
  },
  "withdrawing_limited_partner_entity": {
    "name": "Sample Value",
    "signer_printed_name_and_capacity": "Sample Value"
  }
}
```
