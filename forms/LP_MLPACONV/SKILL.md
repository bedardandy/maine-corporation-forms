# SKILL: Filling LP_MLPACONV

**Form:** Articles of Conversion (Maine Limited Partnership → Other Type of Organization)  
**Entity type:** Limited Partnership  
**When to use:** Convert a Maine Limited Partnership into another type of organization under 31 MRSA §1324 and §1432 (per the recital text on page 1 referencing the Maine LP statute). Records the converting LP's name/form/jurisdiction/formation date, the resulting (post-conversion) organization's name/form/jurisdiction/formation date/principal-office address, the effective date of conversion, an optional foreign-survivor service-of-process address, an attached organizing-document exhibit (or election that no filing is required), and the signature of each general partner.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.effective_date` | text | high | THIRD: The date the conversion is effective under the governing statute of the converted organization: |
| `conversion.new_entity.foreign_service_of_process_mailing_address.line1` | text | high | SIXTH: (Foreign Converted Organization Not Authorized to Transact Business in this State Only) The street and mailing address of an office that may be used for service of process under §1435 is: |
| `conversion.new_entity.foreign_service_of_process_mailing_address.line2` | text | high | (continuation line) |
| `conversion.new_entity.formation_date` | text | high | The date of its organization (resulting org): |
| `conversion.new_entity.governing_statute_jurisdiction` | text | high | The jurisdiction of the converted (resulting) organization's governing statute: |
| `conversion.new_entity.name` | text | high | SECOND: The name of the converted (resulting) organization: |
| `conversion.new_entity.principal_office.physical_address` | text | high | The address of its principal office is: |
| `conversion.new_entity.type` | text | high | The form of the converted (resulting) organization: |
| `conversion.new_entity_organizing_document_exhibit_letter` | text | high | SEVENTH: The organizing document for the converted (resulting) organization is attached as Exhibit ___, and made a part hereof |
| `conversion.result_type` | text | high | SEVENTH: [ ] The organizing document for the converted (resulting) organization is attached as Exhibit ___, and made a part hereof (fills multiple widgets) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.formation_date` | text | high | The date of its organization: |

## Conditional logic

- entity.name (converting LP name) is non-empty. (depends on `entity.name`)
- entity.organization_type is non-empty (typically 'Limited Partnership' on this form). (depends on `entity.organization_type`)
- entity.formation_date is on or before filing.date_signed. (depends on `entity.formation_date`, `filing.date_signed`)
- conversion.new_entity.name is non-empty. (depends on `conversion.new_entity.name`)
- conversion.new_entity.name contains a statutory suffix appropriate for conversion.new_entity.type (e.g., 'LLC' for LLC per 31 MRSA §1508; 'Corp.'/'Inc.' for corporation per 13-C MRSA §401). (depends on `conversion.new_entity.name`, `conversion.new_entity.type`)
- conversion.effective_date is non-empty (THIRD recital is required). (depends on `conversion.effective_date`)
- conversion.effective_date is on or after filing.date_signed. (depends on `conversion.effective_date`, `filing.date_signed`)
- Exactly one SEVENTH option is selected (conversion.result_type ∈ {'filing_required', 'no_filing_required'}). (depends on `conversion.result_type`)
- If conversion.result_type = 'filing_required', conversion.new_entity_organizing_document_exhibit_letter must be set. (depends on `conversion.result_type`, `conversion.new_entity_organizing_document_exhibit_letter`)
- If conversion.new_entity.governing_statute_jurisdiction != 'Maine' AND the resulting entity is not authorized to transact business in Maine (SIXTH header), conversion.new_entity.foreign_service_of_process_mailing_address.line1 must be set. (depends on `conversion.new_entity.governing_statute_jurisdiction`, `conversion.new_entity.foreign_service_of_process_mailing_address.line1`)
- At least general_partner_1.printed_name_and_capacity must be populated; ALL GPs of the converting LP must sign per recital. If the LP has >2 GPs, overflow attaches on additional pages. (depends on `general_partner_1.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "organization_type": "Sample Value",
    "governing_statute_jurisdiction": "Sample Value",
    "formation_date": "2026-01-15"
  },
  "conversion": {
    "new_entity": {
      "name": "Sample Value",
      "type": "Sample Value",
      "governing_statute_jurisdiction": "Sample Value",
      "formation_date": "2026-01-15"
    }
  }
}
```
