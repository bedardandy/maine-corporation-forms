# SKILL: Filling CORP_MBCA-17

**Form:** Articles of Correction (Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Correct an inaccurate or defectively executed corporate filing previously delivered to the Maine Secretary of State under 13-C MRSA §126. Identifies the original filing (document name + filing date), describes the inaccuracy or defect, and supplies the corrected text. Applies to both domestic and foreign business corporations (SEVENTH captures the foreign-corp jurisdiction + Maine-authorization-date when applicable). Filing fee $50. Per SIXTH, the correction is effective retroactively to the original document's effective date except as to persons who relied on the uncorrected document and were adversely affected.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `correction.corrected_information` | text | high | FIFTH: The portion of the said document to be corrected is corrected to read in its entirety as follows: |
| `correction.error_description` | text | high | FOURTH: The inaccuracy or defect to be corrected is described as follows: |
| `correction.original_document_name` | text | high | FIRST: Name of document requiring correction: (i.e. Articles of Incorporation, Articles of Amendment, etc.) |
| `correction.original_filing_date` | text | high | SECOND: Date on which document was filed by Secretary of State: |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | SEVENTH (Foreign Corporation Only): Jurisdiction of incorporation ___ and the date on which the corporation was authorized to transact business in Maine ___ |
| `entity.maine_authorization_date` | text | high | SEVENTH (Foreign Corporation Only): …and the date on which the corporation was authorized to transact business in Maine ___ |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- correction.original_document_name is non-empty. (depends on `correction.original_document_name`)
- correction.original_filing_date is non-empty and parses as a valid date in the past relative to filing.date_signed. (depends on `correction.original_filing_date`, `filing.date_signed`)
- correction.error_description is non-empty. (depends on `correction.error_description`)
- correction.corrected_information is non-empty. (depends on `correction.corrected_information`)
- If the corporation is foreign (entity.home_jurisdiction is set and != 'Maine'/'ME'), entity.maine_authorization_date must also be set. If domestic, both fields should be empty. SEVENTH header explicitly says '(Foreign Corporation Only)'. (depends on `entity.home_jurisdiction`, `entity.maine_authorization_date`)
- filing.signer.printed_name_and_capacity is non-empty and capacity reflects an authorized officer or the corporation's clerk (per 13-C MRSA §121.5). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name, phone, email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15"
  },
  "correction": {
    "original_document_name": "Sample Value",
    "original_filing_date": "2026-01-15",
    "error_description": "Sample Value",
    "corrected_information": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
