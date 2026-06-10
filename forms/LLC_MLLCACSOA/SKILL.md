# SKILL: Filling LLC_MLLCACSOA

**Form:** Amendment or Cancellation of Statement of Authority (Maine LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Amend or cancel a previously filed Statement of Authority for a Maine LLC under 31 MRSA §1542.2. Captures the LLC's name, the original Statement-of-Authority filing date, a SECOND-recital radio that selects either an amendment or a cancellation, the affected person/position, up to 4 description lines for the chosen action, an optional additional-information exhibit letter, and up to 2 authorized-person signer blocks.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.affected_person_or_position` | text | high | Person or position the amendment affects: |
| `amendment.description_1` | text | high | Description of amendment: (line 1) |
| `amendment.description_2` | text | high | Description of amendment: (line 2) |
| `amendment.description_3` | text | high | Description of amendment: (line 3) |
| `amendment.description_4` | text | high | Description of amendment: (line 4) |
| `authority.original_filing_date` | text | high | FIRST: The Statement of Authority was originally filed on: |
| `cancellation.affected_person_or_position` | text | high | Person or position the cancellation affects: |
| `cancellation.description_1` | text | high | Description of authority that is being cancelled: (line 1) |
| `cancellation.description_2` | text | high | Description of authority that is being cancelled: (line 2) |
| `cancellation.description_3` | text | high | Description of authority that is being cancelled: (line 3) |
| `cancellation.description_4` | text | high | Description of authority that is being cancelled: (line 4) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |

_Showing 12 of 31 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- authority.original_filing_date is non-empty and is on or before filing.date_signed (you can't amend a Statement of Authority filed in the future). (depends on `authority.original_filing_date`, `filing.date_signed`)
- Exactly one of the SECOND-recital checkboxes is checked, populating filing.action_type with 'amendment' or 'cancellation' (XOR). (depends on `filing.action_type`)
- If filing.action_type='amendment': amendment.affected_person_or_position is non-empty AND at least amendment.description_1 is non-empty. Cancellation.* fields must be empty. (depends on `filing.action_type`, `amendment.affected_person_or_position`, `amendment.description_1`, `cancellation.affected_person_or_position`, `cancellation.description_1`)
- If filing.action_type='cancellation': cancellation.affected_person_or_position is non-empty AND at least cancellation.description_1 is non-empty. amendment.* fields must be empty. (depends on `filing.action_type`, `cancellation.affected_person_or_position`, `cancellation.description_1`, `amendment.affected_person_or_position`, `amendment.description_1`)
- If filing.additional_information_exhibit_letter is populated, it must be a single uppercase letter A-Z. (depends on `filing.additional_information_exhibit_letter`)
- At least one of {filing.signer_1.printed_name_and_capacity, filing.signer_2.printed_name_and_capacity} is non-empty. (depends on `filing.signer_1.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "authority": {
    "original_filing_date": "2026-01-15"
  },
  "filing": {
    "action_type": "Sample Value"
  },
  "amendment": {
    "affected_person_or_position": "Sample Value",
    "description_1": "Sample Value",
    "description_2": "Sample Value",
    "description_3": "Sample Value",
    "description_4": "Sample Value"
  }
}
```
