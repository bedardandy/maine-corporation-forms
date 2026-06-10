# SKILL: Filling CORP_MBCA-20

**Form:** Articles of Nonprofit Conversion  
**Entity type:** Business Corporation  
**When to use:** Convert a Maine domestic business corporation into a Maine nonprofit corporation under 13-C MRSA §933. Records the pre-conversion business-corporation name, the new nonprofit entity's name (which must satisfy 13-B MRSA naming requirements), an exhibit of the attached Articles of Incorporation (Form MNPCA-6-1), an optional future effective date, and an authorized signature.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.future_effective_date` | text | high | FOURTH: The effective date of the articles of nonprofit conversion (if other than the date of filing) is ___ |
| `conversion.new_entity.name` | text | high | FIRST: ... and the name it proposes to use in the State of Maine is |
| `conversion.new_entity_provisions_exhibit_letter` | text | high | THIRD: ... is attached as Exhibit ___ |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation Prior to Conversion) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (pre-conversion business-corporation name) is non-empty. (depends on `entity.name`)
- conversion.new_entity.name is non-empty. (depends on `conversion.new_entity.name`)
- conversion.new_entity_provisions_exhibit_letter must be set (Form MNPCA-6-1 must be attached as the public organic document for the new nonprofit). (depends on `conversion.new_entity_provisions_exhibit_letter`)
- If conversion.future_effective_date is set, it must be on or after filing.date_signed. (depends on `conversion.future_effective_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (signer must be 'an officer or other duly authorized representative' per 13-C MRSA §933.1; cannot be auto-validated from form alone). (depends on `filing.signer.printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

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
    },
    "entities[1]": {
      "name": "Sample Value"
    }
  }
}
```
