# SKILL: Filling LP_MLPA-9B

**Form:** Statement of Dissociation (Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** File a standalone Statement of Dissociation by a general partner of a Maine limited partnership pursuant to 31 MRSA §1375.1.D. The form names the LP and the dissociating GP, and is signed by that GP (per footnote: 'Certificate MUST be signed by the person dissociated as a general partner. (31 MRSA §1324.1.G)'). The signer is therefore identical to the dissociated GP — individual or entity.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `dissociated_general_partner.name` | text | high | FIRST: The general partner named herein is dissociated... (Name of General Partner) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Limited Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | Dated ____ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- dissociated_general_partner.name is non-empty. (depends on `dissociated_general_partner.name`)
- Either `general_partner_1.printed_name` (individual GP signer) OR both `general_partner_entity_1.name` and `general_partner_entity_1.signer_printed_name_and_capacity` (entity GP signer) are populated. (depends on `general_partner_1.printed_name`, `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- Per the footnote (31 MRSA §1324.1.G), the signer must be the dissociated GP. If individual, `general_partner_1.printed_name` should equal `dissociated_general_partner.name`. If entity, `general_partner_entity_1.name` should equal `dissociated_general_partner.name`. (depends on `dissociated_general_partner.name`, `general_partner_1.printed_name`, `general_partner_entity_1.name`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- At most one of the three expedite checkboxes (Check Box14/15/16) is set; `filing.expedited_service` resolves to a single enum value. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "dissociated_general_partner": {
    "name": "Sample Value"
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
  "general_partner_1": {
    "printed_name": "Sample Value"
  },
  "general_partner_entity_1": {
    "name": "Sample Value",
    "signer_printed_name_and_capacity": "Sample Value"
  }
}
```
