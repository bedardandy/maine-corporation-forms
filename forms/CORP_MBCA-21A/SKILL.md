# SKILL: Filling CORP_MBCA-21A

**Form:** Articles of Entity Conversion (Domestic or Foreign Unincorporated Entity → Maine Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Convert a domestic or foreign unincorporated entity (LLC, LP, LLLP, GP, etc.) into a Maine business corporation under 13-C MRSA §955.2 (domestic unincorporated → corporation) or §955.3 (foreign unincorporated → corporation). Records the pre-conversion entity name, the new corporate name, foreign-origin info (if applicable), the source-organic-law approval recital, an attached Articles of Incorporation provisions exhibit (Form MBCA-6-1), an optional future effective date, and an authorized signature.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.approval_type` | text | high | THIRD: [ ] (Domestic Unincorporated Entity) The plan of entity conversion was duly approved by the unincorporated entity in accordance with the organic law of the unincorporated entity (fills multiple widgets) |
| `conversion.future_effective_date` | text | high | FIFTH: The effective date of the articles of entity conversion (if other than the date of filing of the articles of entity conversion) is |
| `conversion.new_entity.name` | text | high | FIRST: The name of the unincorporated entity is changed as follows (the same must satisfy the requirements of 13-C MRSA §401) |
| `conversion.new_entity_provisions_exhibit_letter` | text | high | FOURTH: All the statements required to be set forth in Articles of Incorporation (Form MBCA-6-1) are attached as Exhibit ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.formation_date_in_home_jurisdiction` | text | high | SECOND: ...and the date of organization was |
| `entity.home_jurisdiction` | text | high | SECOND: (Foreign Unincorporated Entity Only) The unincorporated entity was organized in (state or country) |
| `entity.name` | text | high | (Name of Unincorporated Entity Prior to Conversion) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

_Showing 12 of 23 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (pre-conversion unincorporated entity name) is non-empty. (depends on `entity.name`)
- conversion.new_entity.name is non-empty. (depends on `conversion.new_entity.name`)
- conversion.new_entity.name contains a statutory corporate suffix per 13-C MRSA §401: 'Corp.', 'Corporation', 'Co.', 'Company', 'Inc.', 'Incorporated', or 'Limited'. (depends on `conversion.new_entity.name`)
- Exactly one of the THIRD checkboxes is selected (conversion.approval_type ∈ {'domestic','foreign'}). (depends on `conversion.approval_type`)
- If conversion.approval_type = 'foreign', entity.home_jurisdiction and entity.formation_date_in_home_jurisdiction must be non-empty (SECOND is labeled 'Foreign Unincorporated Entity Only'). (depends on `conversion.approval_type`, `entity.home_jurisdiction`, `entity.formation_date_in_home_jurisdiction`)
- If conversion.approval_type = 'foreign', entity.home_jurisdiction must not equal 'Maine' or 'ME'. (depends on `conversion.approval_type`, `entity.home_jurisdiction`)
- conversion.new_entity_provisions_exhibit_letter is non-empty (FOURTH requires the attached Articles of Incorporation provisions exhibit, Form MBCA-6-1). (depends on `conversion.new_entity_provisions_exhibit_letter`)
- If conversion.future_effective_date is set, it must be on or after filing.date_signed. (depends on `conversion.future_effective_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15"
  },
  "conversion": {
    "new_entity": {
      "name": "Sample Value"
    },
    "approval_type": "Sample Value",
    "new_entity_provisions_exhibit_letter": "Sample Value",
    "future_effective_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
