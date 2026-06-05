# SKILL: Filling CORP_MBCA-21

**Form:** Articles of Entity Conversion by Domestic Business Corporation  
**Entity type:** Business Corporation  
**When to use:** Convert a Maine domestic business corporation into another type of entity (typically an LLC or LP) under 13-C MRSA §955.1, recording the corporation's pre-conversion name, the surviving entity's name and type, an exhibit of provisions required for the new public organic document, and an optional future effective date. A separate filing entity-formation form (e.g., MLLC-6 or MLPA-6) must accompany this filing.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.future_effective_date` | text | high | FIFTH: The effective date of the articles of entity conversion (if other than the date of filing) is |
| `conversion.new_entity.name` | text | high | FIRST: The name of the corporation is changed as follows (the same must satisfy the organic law of the surviving entity) |
| `conversion.new_entity.type` | text | high | SECOND: The type of unincorporated entity that the surviving entity will be |
| `conversion.new_entity_provisions_exhibit_letter` | text | high | FOURTH: If the surviving entity is a filing entity, attached is Exhibit ___ which contains all the provisions required to be set forth in its public organic document... |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation Prior to Conversion) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |

## Conditional logic

- entity.name (pre-conversion corporate name) is non-empty. (depends on `entity.name`)
- conversion.new_entity.name is non-empty. (depends on `conversion.new_entity.name`)
- conversion.new_entity.type is non-empty. (depends on `conversion.new_entity.type`)
- conversion.new_entity.name contains a statutory suffix appropriate for conversion.new_entity.type (e.g., 'LLC' / 'L.L.C.' / 'Limited Liability Company' for LLC per 31 MRSA §1508; 'LP' / 'L.P.' / 'Limited Partnership' for LP per 31 MRSA §1308). (depends on `conversion.new_entity.name`, `conversion.new_entity.type`)
- If conversion.new_entity.type implies a filing entity (LLC, LP, LLLP, etc.), conversion.new_entity_provisions_exhibit_letter must be set and the corresponding formation form (MLLC-6 / MLPA-6) must be bundled. (depends on `conversion.new_entity.type`, `conversion.new_entity_provisions_exhibit_letter`)
- If conversion.future_effective_date is set, it must be on or after filing.date_signed. (depends on `conversion.future_effective_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (signer must be 'an officer or other duly authorized representative' per §955.1; cannot be auto-validated from form alone). (depends on `filing.signer.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "conversion": {
    "new_entity": {
      "name": "Sample Value",
      "type": "Sample Value"
    },
    "new_entity_provisions_exhibit_letter": "Sample Value",
    "future_effective_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
