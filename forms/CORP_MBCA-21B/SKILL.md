# SKILL: Filling CORP_MBCA-21B

**Form:** Articles of Charter Surrender (Upon Entity Conversion)  
**Entity type:** Business Corporation  
**When to use:** Surrender the charter of a Maine domestic business corporation that has converted into a foreign unincorporated entity (LLC, LP, GP, or other non-Maine non-corporate form) under 13-C MRSA §§956 and 957. Records the effective date of the conversion, the jurisdiction of the surviving entity, the address of the surviving entity's executive office (required only if the surviving entity is a nonfiling entity), and the mailing address at which the Secretary of State will be served any process relating to shareholder appraisal rights under chapter 13 of Title 13-C. Filing fee is $90.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.effective_date` | text | high | FIRST: ...the conversion of the corporation to a foreign unincorporated entity and the effective date of the conversion is (date) |
| `conversion.service_of_process_mailing_address` | text | high | FIFTH: ...provide a mailing address to which the Secretary of State may mail a copy of any process served on the Secretary of State. (mailing address) |
| `conversion.surviving_entity_executive_office_address` | text | high | FOURTH: If the surviving entity is a nonfiling entity, the address of its executive office immediately after the conversion. |
| `conversion.surviving_entity_jurisdiction` | text | high | THIRD: The jurisdiction under the laws of which the surviving entity is organized is |
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
- conversion.effective_date is non-empty (FIRST paragraph requires the effective date of the conversion). (depends on `conversion.effective_date`)
- conversion.surviving_entity_jurisdiction is non-empty (THIRD paragraph requires the home jurisdiction of the surviving entity). (depends on `conversion.surviving_entity_jurisdiction`)
- conversion.service_of_process_mailing_address is non-empty (FIFTH paragraph mandates SOS-as-agent appointment for appraisal-rights service). (depends on `conversion.service_of_process_mailing_address`)
- filing.signer.printed_name_and_capacity is non-empty (signer must be 'an officer or other duly authorized representative' per §956.1). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "conversion": {
    "effective_date": "2026-01-15",
    "surviving_entity_jurisdiction": "Sample Value",
    "surviving_entity_executive_office_address": "Sample Value",
    "service_of_process_mailing_address": "Sample Value"
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
