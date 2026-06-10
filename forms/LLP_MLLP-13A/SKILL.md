# SKILL: Filling LLP_MLLP-13A

**Form:** Amended Annual Report (Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** File an amended annual report for a Maine LLP under 31 MRSA §873-A to correct or update information previously reported on a filed annual report. Identifies the LLP (header), its jurisdiction of organization (FIRST), the date the original annual report being amended was filed (SECOND), the substantive changes (THIRD, up to 5 inline lines plus attached pages), and the date on which the underlying information actually changed (FOURTH). Page-2 cover letter is the standard cover-letter primitive. Sibling of LLP_MLLP-13 (the original annual report) and analogous to MBCA-9 / MLLC-9 amended-annual-report patterns.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.changes_description.line1` | text | high | THIRD: The information has changed as follows (attach additional pages, if necessary): [line 1] |
| `amendment.changes_description.line2` | text | high | THIRD: ... [line 2] |
| `amendment.changes_description.line3` | text | high | THIRD: ... [line 3] |
| `amendment.changes_description.line4` | text | high | THIRD: ... [line 4] |
| `amendment.changes_description.line5` | text | high | THIRD: ... [line 5] |
| `amendment.effective_date` | text | high | FOURTH: This information changed on (date) |
| `amendment.original_filing_date` | text | high | SECOND: The date the current year's annual report was filed |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | FIRST: The jurisdiction of its organization is |
| `entity.name` | text | high | (Name of Limited Liability Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |

_Showing 12 of 27 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.home_jurisdiction is non-empty (FIRST recital). (depends on `entity.home_jurisdiction`)
- amendment.original_filing_date is non-empty and not in the future and not after filing.date_signed. (depends on `amendment.original_filing_date`, `filing.date_signed`)
- At least one of amendment.changes_description.line1..line5 is non-empty (otherwise the amendment describes no change). (depends on `amendment.changes_description.line1`, `amendment.changes_description.line2`, `amendment.changes_description.line3`, `amendment.changes_description.line4`, `amendment.changes_description.line5`)
- amendment.effective_date is non-empty and is on or after the entity's earliest known formation date and on or before filing.date_signed. (depends on `amendment.effective_date`, `filing.date_signed`)
- Exactly one signer block is populated: either filing.signer.printed_name_and_capacity (individual partner) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) (entity partner). Both empty or both populated is a fill error. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- If filing.signer_entity.name is populated, filing.signer_entity.signer_printed_name_and_capacity must also be populated. (depends on `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- At most one of the three expedite checkboxes is selected. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value"
  },
  "amendment": {
    "original_filing_date": "2026-01-15",
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
