# SKILL: Filling CORP_REVIVAL

**Form:** Application for Certificate of Revival  
**Entity type:** Business Corporation  
**When to use:** Apply for a Certificate of Revival to restore a dissolved domestic Maine entity (Nonprofit Corporation, Business Corporation, LLC, or Limited Partnership) to active status. The applicant identifies the entity, the original filing date, the entity type, the clerk/registered agent on record at dissolution, the purposes for revival, the time period needed, and the parties requesting revival.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | FIRST: Name of entity applying for revival is |
| `entity.original_filing_date` | text | high | SECOND: Original date of filing with Secretary of States Office |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 32 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.original_filing_date is non-empty and not in the future. (depends on `entity.original_filing_date`)
- Exactly one of THIRD A/B/C/D is selected (revival.entity_type set to a single enum value). (depends on `revival.entity_type`)
- revival.clerk_at_dissolution.name and revival.clerk_at_dissolution.address are both non-empty. (depends on `revival.clerk_at_dissolution.name`, `revival.clerk_at_dissolution.address`)
- revival.purpose is non-empty (concatenation of all four FIFTH lines). (depends on `revival.purpose`)
- revival.time_period_needed is non-empty. (depends on `revival.time_period_needed`)
- At least one of requesting_party_{1,2,3}.printed_name is non-empty along with the corresponding address rows. (depends on `requesting_party_1.printed_name`, `requesting_party_2.printed_name`, `requesting_party_3.printed_name`)
- filing.signer.printed_name is non-empty. (depends on `filing.signer.printed_name`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "original_filing_date": "2026-01-15"
  },
  "revival": {
    "entity_type": "Sample Value",
    "clerk_at_dissolution": {
      "name": "Sample Value",
      "address": "Sample Value"
    },
    "purpose": "Sample Value",
    "time_period_needed": "Sample Value"
  },
  "requesting_party_1": {
    "printed_name": "Sample Value"
  }
}
```
