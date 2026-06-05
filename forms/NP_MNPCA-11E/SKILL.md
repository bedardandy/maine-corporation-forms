# SKILL: Filling NP_MNPCA-11E

**Form:** Voluntary Dissolution by Incorporators (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Dissolve a Maine domestic nonprofit corporation by incorporator consent under 13-B MRSA §1101-A. This dissolution path is available only when (per the form's recitals) the corporation has not carried on activities (SECOND), no debts remain unpaid (THIRD), a majority of incorporators consent to dissolve (FOURTH), and all required Annual Reports have been filed with the SOS (FIFTH). Captures the entity name, original articles filing date (FIRST), Maine registered office (SIXTH, two-line), and up to three incorporator signatures with name+capacity (page 1). Filing fee $10 per page-0 header.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `entity.original_articles_filing_date` | text | high | FIRST: The filing date of its articles of incorporation was ____ |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ____ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.original_articles_filing_date is non-empty and is on or before filing.date_signed. (depends on `entity.original_articles_filing_date`, `filing.date_signed`)
- registered_office.address_line2 (the wide labeled street/city/state/zip line) is non-empty. (depends on `registered_office.address_line2`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- At least one incorporator slot is signed; rubric cannot strictly verify 'majority' without knowing the total count of incorporators (which is not on this form). Page-1 footnote requires majority signatures — synth must populate at least the first slot, and ideally all three with consistent capacities. (depends on `incorporator_1.printed_name_and_capacity`, `incorporator_2.printed_name_and_capacity`, `incorporator_3.printed_name_and_capacity`)
- incorporator_1.printed_name_and_capacity is non-empty (at minimum, slot 1 must be filled). (depends on `incorporator_1.printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "original_articles_filing_date": "2026-01-15"
  },
  "registered_office": {
    "address_line1": "Sample Value",
    "address_line2": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  },
  "incorporator_1": {
    "printed_name_and_capacity": "Sample Value"
  },
  "incorporator_2": {
    "printed_name_and_capacity": "Sample Value"
  },
  "incorporator_3": {
    "printed_name_and_capacity": "Sample Value"
  }
}
```
