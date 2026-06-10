# SKILL: Filling LLP_MLLP-17

**Form:** Certificate of Correction (Domestic Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Correct an inaccurate or defectively-executed previously-filed document for a Maine domestic Limited Liability Partnership under 31 MRSA §824. Identifies the original filing date, describes the inaccuracy/defect, and supplies the corrected text. Per 31 MRSA §826.1.B/2 the certificate must be signed by at least one partner OR by a duly authorized person; an entity-partner alternative signature block is provided.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `correction.corrected_text` | text | high | FOURTH: The portion of the said document to be corrected is corrected to read in its entirety as follows: |
| `correction.defect_description` | text | high | THIRD: The inaccuracy or defect to be corrected is described as follows: |
| `correction.original_filing_date` | text | high | FIRST: On ___ (date) the Secretary of State filed a document delivered for filing by the undersigned limited liability partnership entitled: ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Limited Liability Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

_Showing 12 of 22 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- correction.original_filing_date is non-empty. (depends on `correction.original_filing_date`)
- correction.original_filing_date is on or before filing.date_signed (cannot correct a document that hasn't been filed yet). (depends on `correction.original_filing_date`, `filing.date_signed`)
- correction.defect_description is non-empty. (depends on `correction.defect_description`)
- correction.corrected_text is non-empty. (depends on `correction.corrected_text`)
- Either (filing.signer.printed_name_and_capacity) is non-empty for an individual-partner signer, OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) are both non-empty for an entity-partner signer. At least one path must be populated per 31 MRSA §826.1.B/2. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "correction": {
    "original_filing_date": "2026-01-15",
    "defect_description": "Sample Value",
    "corrected_text": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_entity": {
      "name": "Sample Value",
      "signer_printed_name_and_capacity": "Sample Value"
    }
  }
}
```
