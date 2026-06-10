# SKILL: Filling LP_MLPA-12A

**Form:** Application for Amended Certificate of Authority to Transact Business (Foreign Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Amend the Certificate of Authority of a foreign limited partnership already authorized to transact business in Maine under 31 MRSA §1324. Captures changes to the entity's home-jurisdiction name (or adoption of a fictitious Maine name), additions/dissociations to the GP roster, address and name changes for current GPs, and updates to principal-office and required-office addresses.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `dissociated_general_partner.additional_attached` | text | high | Names of additional dissociated persons as general partners are attached hereto as Exhibit ___ |
| `dissociated_general_partner.additional_exhibit_letter` | text | high | Exhibit ___ (additional dissociated GPs) |
| `dissociated_general_partner_1.address` | text | high | FIFTH: Address (dissociated GP row 1) |
| `dissociated_general_partner_1.name` | text | high | FIFTH: Name (dissociated GP row 1) |
| `dissociated_general_partner_2.address` | text | high | FIFTH: Address (dissociated GP row 2) |
| `dissociated_general_partner_2.name` | text | high | FIFTH: Name (dissociated GP row 2) |
| `dissociated_general_partner_3.address` | text | high | FIFTH: Address (dissociated GP row 3) |
| `dissociated_general_partner_3.name` | text | high | FIFTH: Name (dissociated GP row 3) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | FIRST: Date of organization |
| `entity.home_jurisdiction` | text | high | Jurisdiction of organization |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Partnership in Jurisdiction of Organization) |

_Showing 12 of 62 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty (the LP's existing Maine record). (depends on `entity.home_jurisdiction_name`)
- entity.maine_authorization_date is on or before filing.date_signed (cannot amend before initial authorization). (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true. (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- If new_general_partner.additional_attached is true, new_general_partner.additional_exhibit_letter must be set. (depends on `new_general_partner.additional_attached`, `new_general_partner.additional_exhibit_letter`)
- If dissociated_general_partner.additional_attached is true, dissociated_general_partner.additional_exhibit_letter must be set. (depends on `dissociated_general_partner.additional_attached`, `dissociated_general_partner.additional_exhibit_letter`)
- If general_partner_address_change.additional_attached is true, general_partner_address_change.additional_exhibit_letter must be set. (depends on `general_partner_address_change.additional_attached`, `general_partner_address_change.additional_exhibit_letter`)
- If general_partner_name_change.additional_attached is true, general_partner_name_change.additional_exhibit_letter must be set. (depends on `general_partner_name_change.additional_attached`, `general_partner_name_change.additional_exhibit_letter`)
- If entity.principal_office.physical_address is set, it is not a P.O. Box. (depends on `entity.principal_office.physical_address`)
- At least one signer present: general_partner_1.printed_name OR (general_partner_entity_1.name + general_partner_entity_1.signer_printed_name_and_capacity). §1324.1.M only requires one GP signature. (depends on `general_partner_1.printed_name`, `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15",
    "home_jurisdiction_name_new": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc."
  },
  "filing": {
    "fict4_accompanies": true
  },
  "new_general_partner_1": {
    "name": "Sample Value"
  }
}
```
