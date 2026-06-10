# SKILL: Filling LLC_MLLC-17

**Form:** Statement of Correction (Limited Liability Company — Maine or Foreign)  
**Entity type:** Limited Liability Company  
**When to use:** Correct an incorrect or inaccurate record previously filed with the Maine Secretary of State by a Maine or foreign LLC under 31 MRSA §1675. Identifies the original filing date and document name, describes the error and the corrected information, and is signed by up to two authorized persons (per 31 MRSA §1676.1B). Filing fee $50. The correction is effective retroactively to the original filing's effective date except as to third parties that previously relied on the uncorrected record (FIFTH).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `correction.corrected_information` | text | high | FOURTH: The correction of the incorrect or inaccurate information or the correction to the manner in which the signing was defective is described as follows |
| `correction.error_description` | text | high | THIRD: The incorrect or inaccurate information to be corrected and the reason it is incorrect or inaccurate or the manner in which the signing was defective is described as follows |
| `correction.original_document_name` | text | high | limited liability company entitled: ___ (i.e. Application for Authority to do Business, Assumed Name, etc.) |
| `correction.original_filing_date` | text | high | FIRST: On ___ (filing date) the Secretary of State filed a document delivered for filing by the undersigned limited liability company entitled |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Maine or Foreign Limited Liability Company) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |

_Showing 12 of 22 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- correction.original_filing_date is non-empty and parses as a valid date in the past relative to filing.date_signed. (depends on `correction.original_filing_date`, `filing.date_signed`)
- correction.original_document_name is non-empty. (depends on `correction.original_document_name`)
- correction.error_description is non-empty. (depends on `correction.error_description`)
- correction.corrected_information is non-empty. (depends on `correction.corrected_information`)
- filing.signer.printed_name_and_capacity is non-empty (primary authorized signer per 31 MRSA §1676.1B). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC"
  },
  "correction": {
    "original_filing_date": "2026-01-15",
    "original_document_name": "Sample Value",
    "error_description": "Sample Value",
    "corrected_information": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_2": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
