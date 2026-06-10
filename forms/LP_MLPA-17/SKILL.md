# SKILL: Filling LP_MLPA-17

**Form:** Statement of Correction (Limited Partnership — Maine or Foreign)  
**Entity type:** Limited Partnership  
**When to use:** Correct false or erroneous information or a defectively-signed record previously filed with the Maine Secretary of State by a Maine domestic or foreign limited partnership under 31 MRSA §1327. Identifies the original record name and filing date, describes the error (FOURTH), provides the corrected text (FIFTH), and — for foreign LPs only — recites the home jurisdiction and Maine authorization date (SEVENTH). The correction is effective retroactively to the original filing date except for purposes of 31 MRSA §1303.3 and 4 (third-party reliance). Filing fee $50.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `correction.corrected_information` | text | high | FIFTH: The portion of the said record is corrected to read in its entirety as follows (Attach separate document if more space is needed.) |
| `correction.error_description` | text | high | FOURTH: The incorrect information and the reason it is incorrect or the manner in which the signing was defective is (Attach separate document if more space is needed.) |
| `correction.original_document_name` | text | high | FIRST: Name of record requiring correction |
| `correction.original_filing_date` | text | high | SECOND: Date on which the record was filed by Secretary of State |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | SEVENTH: (Foreign Limited Partnership Only) Jurisdiction of organization |
| `entity.maine_authorization_date` | text | high | SEVENTH: ...and the date on which the limited partnership was authorized to do business in Maine |
| `entity.name` | text | high | (Name of Limited Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

_Showing 12 of 25 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- correction.original_document_name is non-empty. (depends on `correction.original_document_name`)
- correction.original_filing_date is non-empty and on or before filing.date_signed (cannot correct a future record). (depends on `correction.original_filing_date`, `filing.date_signed`)
- correction.error_description is non-empty. (depends on `correction.error_description`)
- correction.corrected_information is non-empty. (depends on `correction.corrected_information`)
- If either entity.home_jurisdiction or entity.maine_authorization_date is set, both must be set (SEVENTH applies to foreign LPs only and the two fields must travel together). (depends on `entity.home_jurisdiction`, `entity.maine_authorization_date`)
- At least one signer present: general_partner_1.printed_name OR (general_partner_entity_1.name + general_partner_entity_1.signer_printed_name_and_capacity). §1324.1.J only requires one GP signature. (depends on `general_partner_1.printed_name`, `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- If general_partner_entity_1.name is set, general_partner_entity_1.signer_printed_name_and_capacity must also be set. (depends on `general_partner_entity_1.name`, `general_partner_entity_1.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

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
