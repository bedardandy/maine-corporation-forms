# SKILL: Filling LLC_MLLCCONV

**Form:** Statement of Conversion (Maine LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Record with the Maine SOS that an organization has converted into another organization under 31 MRSA §1647 (Maine LLC chapter conversion provisions). Captures parallel identification of the converting (predecessor) and converted/resulting organizations — name, form, jurisdiction, date of organization — plus the resulting entity's principal-office address, the conversion's effective date, a foreign-resulting-entity service-of-process address (when the resulting entity is foreign), and a SEVENTH-recital select-one indicating either the resulting entity's organizing document is attached as an exhibit OR the resulting entity is not a Maine SOS filer.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.effective_date` | text | high | THIRD: The date the conversion is effective under the governing statute of the converted organization: |
| `conversion.foreign_resulting_entity.principal_office_address.line1` | text | high | SIXTH: (Foreign Converted Organization Only) ... address of its principal office for the purposes of §1648.3 is: (line 1) |
| `conversion.foreign_resulting_entity.principal_office_address.line2` | text | high | SIXTH (continued): (Principal office address — line 2) |
| `conversion.new_entity.jurisdiction` | text | high | The jurisdiction of the converted (resulting) organization's governing statute: |
| `conversion.new_entity.name` | text | high | SECOND: Converted (Resulting) Organization — The name of the converted (resulting) organization: |
| `conversion.new_entity.principal_office_address` | text | high | SECOND (continued): The address of its principal office is: |
| `conversion.new_entity.type` | text | high | The form of the converted (resulting) organization: |
| `conversion.new_entity_provisions_exhibit_letter` | text | high | SEVENTH: Result of Conversion (Select One) — *The organizing document for the converted (resulting) organization is attached as Exhibit ___ |
| `conversion.organizing_document_disposition` | enum_select | high | SEVENTH (option 1): [ ] *The organizing document for the converted (resulting) organization is attached as Exhibit ___, and made a part hereof |
| `conversion.signature_block.converting_entity_name_and_form` | text | high | Must Be Completed by the Converting Organization — (name and form of converting organization) |
| `entity.form_type` | text | high | The form of the converting organization: |
| `entity.home_jurisdiction` | text | high | The jurisdiction of the converting organization prior to filing this certificate: |

_Showing 12 of 32 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the converting/predecessor organization's name) is non-empty. (depends on `entity.name`)
- entity.form_type is non-empty (the FIRST recital captures the converting entity's pre-conversion form). (depends on `entity.form_type`)
- entity.home_jurisdiction is non-empty. (depends on `entity.home_jurisdiction`)
- entity.original_articles_filing_date is non-empty and is on or before filing.date_signed. (depends on `entity.original_articles_filing_date`, `filing.date_signed`)
- conversion.new_entity.name is non-empty. (depends on `conversion.new_entity.name`)
- conversion.new_entity.type is non-empty. (depends on `conversion.new_entity.type`)
- conversion.new_entity.jurisdiction is non-empty. (depends on `conversion.new_entity.jurisdiction`)
- conversion.effective_date is non-empty. (depends on `conversion.effective_date`)
- If conversion.new_entity.jurisdiction is non-Maine, conversion.foreign_resulting_entity.principal_office_address.line1 must be non-empty (SIXTH recital required for foreign-resulting filings per §1648.3). (depends on `conversion.new_entity.jurisdiction`, `conversion.foreign_resulting_entity.principal_office_address.line1`)
- Exactly one SEVENTH-recital checkbox is selected, populating conversion.organizing_document_disposition with 'attached_as_exhibit' or 'not_filing_with_sos' (form text 'Select One'). (depends on `conversion.organizing_document_disposition`)
- If conversion.organizing_document_disposition='attached_as_exhibit', conversion.new_entity_provisions_exhibit_letter must be a single uppercase letter A-Z. (depends on `conversion.organizing_document_disposition`, `conversion.new_entity_provisions_exhibit_letter`)
- At least filing.signer_1.printed_name_and_capacity is non-empty. (depends on `filing.signer_1.printed_name_and_capacity`)
- conversion.signature_block.converting_entity_name_and_form is non-empty and includes both the entity name and form (e.g., 'Acme LLC, a Maine limited liability company'). (depends on `conversion.signature_block.converting_entity_name_and_form`, `entity.name`, `entity.form_type`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name (the converting/predecessor entity is the lead entity on the cover letter). (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC",
    "form_type": "Sample Value",
    "home_jurisdiction": "Sample Value",
    "original_articles_filing_date": "2026-01-15"
  },
  "conversion": {
    "new_entity": {
      "name": "Sample Value",
      "type": "Sample Value",
      "jurisdiction": "Sample Value",
      "formation_date": "2026-01-15"
    }
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
