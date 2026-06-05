# SKILL: Filling CORP_MBCA-13A

**Form:** Amended Annual Report (Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** File an amended annual report for a Maine domestic or foreign business corporation under 13-C MRSA §1623 to correct or update information previously filed on the current year's annual report. Captures the corporation's jurisdiction of incorporation (FIRST), the date of the original annual report being amended (SECOND), the substantive changes (THIRD, 4 inline lines + attachable additional pages), and the date the changes occurred (FOURTH). Per the * footnote on page 1: 'An amended annual report may be filed by the corporation to change information currently on file. The time for filing an amended annual report is from the date of the original filing until December 31st of that filing year.' Filing fee is $85 domestic / $150 foreign per the page-0 header.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.changes_description.line1` | text | high | THIRD: The information has changed as follows (attach additional pages, if necessary): line 1 |
| `amendment.changes_description.line2` | text | high | THIRD: amendment text (line 2) |
| `amendment.changes_description.line3` | text | high | THIRD: amendment text (line 3) |
| `amendment.changes_description.line4` | text | high | THIRD: amendment text (line 4 — bottom) |
| `amendment.effective_date` | text | high | FOURTH: This information changed on (date) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | FIRST: The jurisdiction of its incorporation is |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.home_jurisdiction is non-empty (FIRST). (depends on `entity.home_jurisdiction`)
- filing.original_annual_report_date is non-empty and on or before filing.date_signed. (depends on `filing.original_annual_report_date`, `filing.date_signed`)
- filing.date_signed is on or before December 31 of the year of filing.original_annual_report_date (per the * footnote: amendment window is from original filing date until Dec 31 of that filing year). (depends on `filing.original_annual_report_date`, `filing.date_signed`)
- At least one of amendment.changes_description.line1–line4 is non-empty. (depends on `amendment.changes_description.line1`, `amendment.changes_description.line2`, `amendment.changes_description.line3`, `amendment.changes_description.line4`)
- amendment.effective_date is non-empty (FOURTH). (depends on `amendment.effective_date`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

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
      "line4": "Sample Value"
    },
    "effective_date": "2026-01-15"
  }
}
```
