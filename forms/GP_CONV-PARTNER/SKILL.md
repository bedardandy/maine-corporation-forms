# SKILL: Filling GP_CONV-PARTNER

**Form:** Articles of Conversion of Partnership  
**Entity type:** General Partnership  
**When to use:** Convert a Maine partnership (general partnership; LP filers use the Limited-Partnership-specific conversion form) into another entity type — Limited Partnership, Limited Liability Limited Partnership, Corporation, or Limited Liability Company — under 31 MRSA §1093. Records the converting partnership's name, the resulting entity's type and name, an exhibit of the new entity's organizing-document provisions, and an optional future effective date capped at 90 days. The corresponding formation form (MLPA-6-1, MLLC-6, or MBCA-6-1) must be attached.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.future_effective_date` | text | high | FOURTH: The future effective date of the conversion (if other than date of filing of the Articles) is — (Not to exceed 90 days from date of filing of the Articles) |
| `conversion.new_entity.name` | text | high | THIRD: The name of the resulting entity is (the name must satisfy the organic law of the surviving entity) |
| `conversion.new_entity_provisions_exhibit_letter` | text | high | FIFTH: All of the statements required to be set forth in the organizing documents for the resulting entity are attached as Exhibit ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | FIRST: The name of the converting partnership immediately before the conversion is |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

## Conditional logic

- entity.name (pre-conversion partnership name) is non-empty. (depends on `entity.name`)
- Exactly one of the SECOND checkboxes is selected, populating conversion.new_entity.type with a valid enum value. (depends on `conversion.new_entity.type`)
- conversion.new_entity.name is non-empty. (depends on `conversion.new_entity.name`)
- conversion.new_entity.name contains a statutory suffix appropriate for conversion.new_entity.type — 'LP'/'L.P.'/'Limited Partnership' for limited_partnership, 'LLLP'/'L.L.L.P.' for limited_liability_limited_partnership, 'LLC'/'L.L.C.'/'Limited Liability Company' for limited_liability_company, 'Corp'/'Inc'/'Incorporated'/'Corporation' for corporation. (depends on `conversion.new_entity.name`, `conversion.new_entity.type`)
- conversion.new_entity_provisions_exhibit_letter is non-empty (organizing documents must be attached as the corresponding formation form: MLPA-6-1, MLLC-6, or MBCA-6-1). (depends on `conversion.new_entity_provisions_exhibit_letter`)
- If conversion.future_effective_date is set, it must be on or after filing.date_signed and not exceed 90 days from filing.date_signed (per page-0 form text 'Not to exceed 90 days'). (depends on `conversion.future_effective_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (must be at least one partner OR a duly authorized representative per page-1 footnote). (depends on `filing.signer.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "conversion": {
    "new_entity": {
      "name": "Sample Value"
    },
    "future_effective_date": "2026-01-15",
    "new_entity_provisions_exhibit_letter": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    }
  }
}
```
