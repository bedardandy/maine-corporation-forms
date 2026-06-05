# SKILL: Filling CORP_MBCA-9

**Form:** Articles of Amendment  
**Entity type:** Business Corporation  
**When to use:** Amend the articles of incorporation of an existing Maine domestic business corporation under 13-C MRSA §§1006, 1004, 1005, 1011, including approval method, optional benefit-corporation status changes, share-exchange provisions, and effective date.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.adoption_date` | text | high | FIRST: The amendment was adopted on (date) |
| `amendment.benefit_corp_public_benefit_exhibit_letter` | text | high | SECOND: ...specific public benefit ... as set forth in Exhibit __ |
| `amendment.effective_date` | text | high | FOURTH: The effective date of the amendment (if other than the date of filing) is ___ |
| `amendment.share_exchange_exhibit_letter` | text | high | THIRD: ...are set forth in Exhibit __, or as follows |
| `amendment.share_exchange_inline_text` | text | high | THIRD: ...or as follows: ___ |
| `amendment.text_exhibit_letter` | text | high | FIRST: ...as set forth in Exhibit __ |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

## Conditional logic

- entity.name on the form matches the corporation's existing name of record at the SOS (case-insensitive trim). (depends on `entity.name`)
- amendment.adoption_date is not in the future relative to filing.date_signed. (depends on `amendment.adoption_date`, `filing.date_signed`)
- Either amendment.text_exhibit_letter is set OR an inline text-of-amendment exhibit reference is present (form requires one). (depends on `amendment.text_exhibit_letter`)
- Exactly one of the FIRST options is selected. (depends on `amendment.approval_method`)
- If amendment.benefit_corp_change = 'modify_public_benefit', amendment.benefit_corp_public_benefit_exhibit_letter must be set. (depends on `amendment.benefit_corp_change`, `amendment.benefit_corp_public_benefit_exhibit_letter`)
- If amendment.effective_date is set, it is on or after amendment.adoption_date. (depends on `amendment.effective_date`, `amendment.adoption_date`)
- filing.signer.printed_name is non-empty (note: signer must be a duly authorized officer per 13-C MRSA §1011 — cannot be auto-validated from form alone). (depends on `filing.signer.printed_name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "amendment": {
    "adoption_date": "2026-01-15",
    "text_exhibit_letter": "Sample Value",
    "approval_method": "Sample Value",
    "benefit_corp_change": "Sample Value",
    "benefit_corp_public_benefit_exhibit_letter": "Sample Value",
    "share_exchange_exhibit_letter": "Sample Value",
    "share_exchange_inline_text": "Sample Value"
  }
}
```
