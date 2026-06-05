# SKILL: Filling NP_MNPCA-14

**Form:** Application for Excuse (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Apply for excuse from filing further annual reports for a Maine domestic nonprofit corporation that has ceased to carry on activities, pursuant to 13-B MRSA §1301.5. The signer (President, Treasurer, or Clerk/Secretary — circled on the form) certifies the cessation date and that all required prior annual reports have been filed. The excuse is effective upon acceptance by the Secretary of State; if the corporation later resumes activities, annual-report filing duties resume. Filing fee is $5.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.cessation_date` | text | high | ceased to carry on activities on (date) ___ |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- filing.signer.printed_name is non-empty (the 'I, ___' widget at the start of the certification paragraph). (depends on `filing.signer.printed_name`)
- entity.cessation_date is non-empty (the §1301.5 excuse is unavailable without a stated cessation date). (depends on `entity.cessation_date`)
- entity.cessation_date should be on or before filing.date_signed (the corporation must have already ceased activities). (depends on `entity.cessation_date`, `filing.date_signed`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "cessation_date": "2026-01-15"
  },
  "filing": {
    "signer": {
      "printed_name": "Sample Value"
    },
    "date_signed": "2026-01-15",
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    },
    "expedited_service": "Sample Value",
    "total_fees_dollars": "Sample Value"
  }
}
```
