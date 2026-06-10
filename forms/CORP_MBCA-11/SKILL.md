# SKILL: Filling CORP_MBCA-11

**Form:** Articles of Dissolution  
**Entity type:** Business Corporation  
**When to use:** Dissolve a Maine domestic business corporation under 13-C MRSA §1404, recording the original-filing date, dissolution-authorization date, optional future effective date, and (when applicable) shareholder approval.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `dissolution.authorization_date` | text | high | SECOND: The date on which the dissolution was authorized is |
| `dissolution.effective_date` | text | high | THIRD: The future effective date of the articles of dissolution (if other than the date of filing) is |
| `dissolution.shareholder_approval_obtained` | checkbox | high | FOURTH: [Check if applicable] The proposal to dissolve was duly approved by the shareholders in the manner required by this Act and by the corporation's articles of incorporation. |
| `entity.name` | text | high | (Name of Corporation) |
| `entity.original_articles_filing_date` | text | high | FIRST: The date the original articles of incorporation were filed |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name matches the corporation's name of record at the SOS. (depends on `entity.name`)
- entity.original_articles_filing_date is strictly before dissolution.authorization_date. (depends on `entity.original_articles_filing_date`, `dissolution.authorization_date`)
- dissolution.authorization_date is not in the future relative to filing.date_signed. (depends on `dissolution.authorization_date`, `filing.date_signed`)
- If dissolution.effective_date is set, it is on or after dissolution.authorization_date. (depends on `dissolution.effective_date`, `dissolution.authorization_date`)
- filing.signer.printed_name_and_capacity includes a capacity (officer title or 'Clerk') — required because 13-C MRSA §121.5 limits signing authority. (depends on `filing.signer.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "original_articles_filing_date": "2026-01-15"
  },
  "dissolution": {
    "authorization_date": "2026-01-15",
    "effective_date": "2026-01-15",
    "shareholder_approval_obtained": true
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities": [
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
