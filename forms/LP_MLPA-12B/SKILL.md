# SKILL: Filling LP_MLPA-12B

**Form:** Notice of Cancellation of Certificate of Authority to Transact Business (Foreign Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Cancel a foreign limited partnership's certificate of authority to transact business in Maine under 31 MRSA §1417. Captures the LP's home-jurisdiction name, optional Maine fictitious name (per §1508), home jurisdiction and date of organization, original Maine authorization date, and current principal-office and (optional) required-office addresses. Pursuant to SEVENTH, the SOS is automatically appointed as agent for service of process for residual rights of action arising from the LP's prior Maine activities.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.formation_date_in_home_jurisdiction` | text | high | SECOND: The date of organization is |
| `entity.home_jurisdiction` | text | high | SECOND: The jurisdiction of its organization is |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Partnership in Jurisdiction of Organization) |
| `entity.maine_authorization_date` | text | high | THIRD: The date on which it was authorized to transact business in the State of Maine is |
| `entity.maine_fictitious_name` | text | high | FIRST: The fictitious name, if any, of the limited partnership under which the limited partnership applied for authority to transact business in this State because its real name was not available is |
| `entity.principal_office.mailing_address` | text | high | (mailing address if different from above) [principal office] |
| `entity.principal_office.physical_address` | text | high | FOURTH: The street and mailing address of the foreign limited partnership's principal office is: (physical location - street (not P.O. Box), city, state and zip code) |
| `entity.required_office.mailing_address` | text | high | (mailing address if different from above) [required office] |
| `entity.required_office.physical_address` | text | high | FIFTH: The street and mailing address of the foreign limited partnership's required* office is: (physical location - street (not P.O. Box), city, state and zip code) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |

_Showing 12 of 27 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty. (depends on `entity.home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is non-empty. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.maine_authorization_date is non-empty and on or before filing.date_signed (cannot cancel before initial authorization). (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- entity.principal_office.physical_address is non-empty and not a P.O. Box. (depends on `entity.principal_office.physical_address`)
- If entity.required_office.physical_address is set, it is not a P.O. Box. (FIFTH is conditional on home-jurisdiction law per the * footnote.) (depends on `entity.required_office.physical_address`)
- At least one signer present: general_partner_1.printed_name OR (general_partner_entity_1.name + general_partner_entity_1.signer_printed_name_and_capacity). §1324.1.M only requires one GP signature. (depends on `general_partner_1.printed_name`, `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- If general_partner_entity_1.name is set, general_partner_entity_1.signer_printed_name_and_capacity must also be set. (depends on `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "maine_authorization_date": "2026-01-15",
    "principal_office": {
      "physical_address": "Sample Value",
      "mailing_address": "Sample Value"
    },
    "required_office": {
      "physical_address": "Sample Value"
    }
  }
}
```
