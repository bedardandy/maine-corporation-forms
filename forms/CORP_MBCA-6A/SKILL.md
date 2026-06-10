# SKILL: Filling CORP_MBCA-6A

**Form:** Restated Articles of Incorporation  
**Entity type:** Business Corporation  
**When to use:** File Restated Articles of Incorporation for a Maine domestic business corporation under 13-C MRSA §1007. The restatement consolidates all prior amendments into a single document, optionally adding a new amendment. The full restated text MUST be attached as an exhibit (typically the contents of MBCA-6-1).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.adoption_date` | text | high | The text of the new amendment was adopted on (date) ___ |
| `amendment.approval_method` | text | high | by the incorporators – shareholder approval was not required (fills multiple widgets) |
| `amendment.share_exchange_exhibit_letter` | text | high | THIRD: ...are set forth in Exhibit ___ or as follows |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

_Showing 12 of 23 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- restatement.text_exhibit_letter is non-empty (the full restated text MUST be attached as an exhibit per the form footnote). (depends on `restatement.text_exhibit_letter`)
- Exactly one of Check Box8 or Check Box9 is selected (restatement.type set to a single enum value). (depends on `restatement.type`)
- If restatement.type = 'includes_new_amendment', then amendment.adoption_date and amendment.approval_method must both be populated. (depends on `restatement.type`, `amendment.adoption_date`, `amendment.approval_method`)
- When restatement.type = 'includes_new_amendment', exactly one of Check Box10/11/13 is selected. (depends on `restatement.type`, `amendment.approval_method`)
- If amendment.adoption_date is set, it is not in the future relative to filing.date_signed. (depends on `amendment.adoption_date`, `filing.date_signed`)
- If restatement.future_effective_date is set, it is on or after filing.date_signed. (depends on `restatement.future_effective_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "restatement": {
    "text_exhibit_letter": "Sample Value",
    "type": "consolidation_only",
    "future_effective_date": "2026-01-15"
  },
  "amendment": {
    "adoption_date": "2026-01-15",
    "approval_method": "Sample Value",
    "share_exchange_exhibit_letter": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
