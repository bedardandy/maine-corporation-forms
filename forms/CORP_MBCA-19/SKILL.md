# SKILL: Filling CORP_MBCA-19

**Form:** Articles of Domestication (Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Domesticate a foreign business corporation into a Maine domestic business corporation under 13-C MRSA §923. Records the corporation's foreign legal name, optional new Maine name (when the foreign name is unavailable or the corporation chooses to change), home jurisdiction and date of original incorporation, the attached Articles of Incorporation exhibit (Form MBCA-6-1), an optional future effective date, and the authorized signer.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `domestication.articles_exhibit_letter` | text | high | THIRD: All the statements required to be set forth in Articles of Incorporation (Form MBCA-6-1) are attached as Exhibit ___ |
| `domestication.future_effective_date` | text | high | FOURTH: The effective date of the articles of domestication (if other than the date of filing) |
| `domestication.maine_name` | text | high | FIRST: …the name it proposes to use in the State of Maine |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | and the original date of incorporation was ___ |
| `entity.home_jurisdiction` | text | high | SECOND: The corporation was originally incorporated in ___ (state or country) |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation in Jurisdiction of Incorporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty. (depends on `entity.home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is non-empty. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is on or before filing.date_signed (cannot domesticate before original incorporation). (depends on `entity.formation_date_in_home_jurisdiction`, `filing.date_signed`)
- domestication.articles_exhibit_letter is non-empty (Form MBCA-6-1 must be attached). (depends on `domestication.articles_exhibit_letter`)
- If domestication.future_effective_date is set, it must be on or after filing.date_signed. (depends on `domestication.future_effective_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (must be an officer or duly authorized representative per §923). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15"
  },
  "domestication": {
    "maine_name": "Sample Value",
    "articles_exhibit_letter": "Sample Value",
    "future_effective_date": "2026-01-15"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
