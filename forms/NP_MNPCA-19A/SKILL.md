# SKILL: Filling NP_MNPCA-19A

**Form:** Statement of Abandonment of Domestication and Conversion (Foreign Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Abandon a previously-filed domestication and conversion of a foreign nonprofit corporation in Maine. The corporation recites (FIRST) that the abandonment was effected in accordance with the laws of its foreign jurisdiction after the original articles of domestication and conversion were filed with the Maine SOS, and (SECOND) that this statement takes effect upon filing such that the domestication and conversion is considered abandoned and does not become effective. Only 3 body widgets: entity name, dated, signer. Filing fee $35 per page-0 header.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ____ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |

_Showing 12 of 17 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty (this is a foreign-only form per the FOREIGN NONPROFIT CORPORATION page-0 heading). (depends on `entity.home_jurisdiction_name`)
- filing.date_signed is non-empty (statement takes effect upon filing per SECOND). (depends on `filing.date_signed`)
- filing.date_signed is not in the future (the statement takes effect upon filing — a future-dated statement cannot already be filed). (depends on `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D); the form footer requires signature by 'an officer or other duly authorized representative'. (depends on `filing.signer.printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc."
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    },
    "expedited_service": "Sample Value",
    "total_fees_dollars": "Sample Value",
    "contact": {
      "name": "Sample Value"
    }
  }
}
```
