# SKILL: Filling LP_MLPA-9

**Form:** Certificate of Amendment (Domestic Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Amend the certificate of a domestic limited partnership under 31 MRSA §1322. Covers name changes, LLLP status elections, professional LLLP elections, changes to general partners (additions, dissociations, replacements, address/name changes), dissolution, and other amendments.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.other_exhibit_letter` | text | high | TWELFTH: Exhibit ___ |
| `dissociated_general_partner.additional_attached` | text | high | SIXTH: Names of additional dissociated person as a general partners are attached as Exhibit ___ |
| `dissociated_general_partner.additional_exhibit_letter` | text | high | SIXTH: Exhibit ___ |
| `dissociated_general_partner_1.address` | text | high | SIXTH: Address (row 1) |
| `dissociated_general_partner_1.name` | text | high | SIXTH: Name (row 1) |
| `dissociated_general_partner_2.address` | text | high | SIXTH: Address (row 2) |
| `dissociated_general_partner_2.name` | text | high | SIXTH: Name (row 2) |
| `dissociated_general_partner_3.address` | text | high | SIXTH: Address (row 3) |
| `dissociated_general_partner_3.name` | text | high | SIXTH: Name (row 3) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.initial_certificate_filing_date` | text | high | FIRST: The date of filing of the limited partnership's initial certificate is ___ (date) |
| `entity.is_dissolved` | checkbox | high | NINTH: The limited partnership is dissolved. |

_Showing 12 of 69 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.initial_certificate_filing_date is non-empty. (depends on `entity.initial_certificate_filing_date`)
- If entity.is_lllp is true, entity.name must contain 'LLLP', 'L.L.L.P.', or 'Limited Liability Limited Partnership'. If false, it must contain 'LP', 'L.P.', or 'Limited Partnership'. (depends on `entity.is_lllp`, `entity.name`)
- If entity.is_professional_lllp is true, entity.professional_services_description must be non-empty. (depends on `entity.is_professional_lllp`, `entity.professional_services_description`)
- If new_general_partner.additional_attached is true, new_general_partner.additional_exhibit_letter must be set. (depends on `new_general_partner.additional_attached`, `new_general_partner.additional_exhibit_letter`)
- If dissociated_general_partner.additional_attached is true, dissociated_general_partner.additional_exhibit_letter must be set. (depends on `dissociated_general_partner.additional_attached`, `dissociated_general_partner.additional_exhibit_letter`)
- If general_partner_address_change.additional_attached is true, general_partner_address_change.additional_exhibit_letter must be set. (depends on `general_partner_address_change.additional_attached`, `general_partner_address_change.additional_exhibit_letter`)
- If general_partner_name_change.additional_attached is true, general_partner_name_change.additional_exhibit_letter must be set. (depends on `general_partner_name_change.additional_attached`, `general_partner_name_change.additional_exhibit_letter`)
- If TWELFTH is used (implied by amendment.other_exhibit_letter being set), the exhibit letter must be present. (depends on `amendment.other_exhibit_letter`)
- At least one signatory (individual or entity) is populated. (depends on `general_partner_1.printed_name`, `general_partner_entity_1.name`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "initial_certificate_filing_date": "2026-01-15",
    "is_lllp": true,
    "is_professional_lllp": true,
    "professional_services_description": "Sample Value"
  },
  "new_general_partner_1": {
    "name": "Sample Value",
    "address": "Sample Value"
  },
  "new_general_partner_2": {
    "name": "Sample Value"
  }
}
```
