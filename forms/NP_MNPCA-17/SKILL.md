# SKILL: Filling NP_MNPCA-17

**Form:** Certificate of Correction (Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Correct an inaccuracy or defect in a previously filed document of a Maine nonprofit corporation (domestic or foreign) under 13-B MRSA §106.4. Identifies the original filing (date + document title), describes the error (THIRD), supplies the corrected text in its entirety (FOURTH), states the Maine registered office, and is signed by an authorized officer. The correction takes effect as of the original filing date except as to persons substantially and adversely affected.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `correction.corrected_text` | text | high | FOURTH: The portion of the said document to be corrected is corrected to read in its entirety as follows: |
| `correction.error_description` | text | high | THIRD: The inaccuracy or defect to be corrected is described as follows: |
| `correction.original_document_title` | text | high | FIRST: ...entitled: ___ (i.e. Articles of Incorporation, Articles of Amendment, etc.) |
| `correction.original_filing_date` | text | high | FIRST: On ___ (date) the Secretary of State filed a document... |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | incorporated under the laws of the State of ___, and authorized to carry on activities in Maine |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |

_Showing 12 of 24 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- correction.original_filing_date is non-empty (FIRST). (depends on `correction.original_filing_date`)
- correction.original_document_title is non-empty (FIRST). (depends on `correction.original_document_title`)
- correction.error_description is non-empty (THIRD). (depends on `correction.error_description`)
- correction.corrected_text is non-empty (FOURTH). (depends on `correction.corrected_text`)
- registered_agent.physical_address is non-empty (SIXTH). (depends on `registered_agent.physical_address`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- At least one of filing.signer or filing.signer_2 printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`)
- correction.original_filing_date must be on or before filing.date_signed (you can only correct documents that already exist). (depends on `correction.original_filing_date`, `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value"
  },
  "correction": {
    "original_filing_date": "2026-01-15",
    "original_document_title": "Sample Value",
    "error_description": "Sample Value",
    "corrected_text": "Sample Value"
  },
  "registered_agent": {
    "physical_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
