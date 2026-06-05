# SKILL: Filling NP_MNPCA-13A

**Form:** Amended Annual Report (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** File an amended annual report for a Maine nonprofit corporation under 13-B MRSA §1301-C, correcting or updating information previously reported. Recites the home jurisdiction, the date the original annual report was filed, the substantive changes (free-text, up to 7 inline lines), and the effective date of those changes. The amendment window runs from the original filing date through December 31 of the same filing year.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.changes_description.line1` | text | high | THIRD: The information has changed as follows (attach additional pages, if necessary): (line 1) |
| `amendment.changes_description.line2` | text | high | THIRD: ... (line 2) |
| `amendment.changes_description.line3` | text | high | THIRD: ... (line 3) |
| `amendment.changes_description.line4` | text | high | THIRD: ... (line 4) |
| `amendment.changes_description.line5` | text | high | THIRD: ... (line 5) |
| `amendment.changes_description.line6` | text | high | THIRD: ... (line 6) |
| `amendment.changes_description.line7` | text | high | THIRD: ... (line 7) |
| `amendment.effective_date` | text | high | FOURTH: This information changed on (date) ___ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | FIRST: The jurisdiction of its incorporation is ___ |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.home_jurisdiction is non-empty (typically 'Maine' or 'ME' for domestic nonprofits). (depends on `entity.home_jurisdiction`)
- filing.original_annual_report_date is non-empty and on or before filing.date_signed. (depends on `filing.original_annual_report_date`, `filing.date_signed`)
- At least one of amendment.changes_description.line1..line7 is non-empty (the THIRD block carries the substantive amendment). (depends on `amendment.changes_description.line1`, `amendment.changes_description.line2`, `amendment.changes_description.line3`, `amendment.changes_description.line4`, `amendment.changes_description.line5`, `amendment.changes_description.line6`, `amendment.changes_description.line7`)
- amendment.effective_date is non-empty and on or before filing.date_signed. (depends on `amendment.effective_date`, `filing.date_signed`)
- filing.date_signed is no later than December 31 of the calendar year of filing.original_annual_report_date (per 13-B MRSA §1301-C amendment window). Cannot file an amended annual report after that year ends. (depends on `filing.original_annual_report_date`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (must be a duly authorized officer per 13-B MRSA §104.1.B). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value"
  },
  "filing": {
    "original_annual_report_date": "2026-01-15"
  },
  "amendment": {
    "changes_description": {
      "line1": "Sample Value",
      "line2": "Sample Value",
      "line3": "Sample Value",
      "line4": "Sample Value",
      "line5": "Sample Value"
    }
  }
}
```
