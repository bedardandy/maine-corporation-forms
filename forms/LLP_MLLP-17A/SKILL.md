# SKILL: Filling LLP_MLLP-17A

**Form:** Certificate of Correction (Foreign Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Correct an inaccurate or defectively-executed previously-filed document for a foreign Limited Liability Partnership authorized to do business in Maine, pursuant to 31 MRSA §856. The form identifies the foreign LLP, its home jurisdiction, the date and title of the original document, the inaccuracy or defect, and the corrected text. Two parallel signature blocks are provided on page 1 — one for an individual partner / duly authorized person and one for an entity-partner with its natural-person signer.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `correction.corrected_text` | text | high | FOURTH: The portion of the said document to be corrected is corrected to read in its entirety as follows: |
| `correction.defect_description` | text | high | THIRD: The inaccuracy or defect to be corrected is described as follows: |
| `correction.original_document_type` | text | high | partnership entitled: ____ (i.e. Application for Authority to do Business, Assumed Name, etc.) |
| `correction.original_filing_date` | text | high | FIRST: On ____ (date) the Secretary of State filed a document delivered for filing by the undersigned foreign limited liability partnership entitled: |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | a partnership organized under the laws of the jurisdiction of ____, and authorized to do business in Maine |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Liability Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- correction.original_filing_date is non-empty. (depends on `correction.original_filing_date`)
- correction.original_filing_date is on or before filing.date_signed (cannot correct a document that hasn't been filed yet). (depends on `correction.original_filing_date`, `filing.date_signed`)
- correction.original_document_type is non-empty. (depends on `correction.original_document_type`)
- correction.defect_description is non-empty. (depends on `correction.defect_description`)
- correction.corrected_text is non-empty. (depends on `correction.corrected_text`)
- Either filing.signer.printed_name_and_capacity is non-empty (individual-partner signer) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) are both non-empty (entity-partner signer). At least one path must be populated. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value"
  },
  "correction": {
    "original_filing_date": "2026-01-15",
    "original_document_type": "Sample Value",
    "defect_description": "Sample Value",
    "corrected_text": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
