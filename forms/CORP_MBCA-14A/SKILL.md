# SKILL: Filling CORP_MBCA-14A

**Form:** Certificate of Resumption (for a Maine Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Resume the transaction of business for a Maine domestic business corporation that has been suspended or forfeited, pursuant to 13-C MRSA §1621.5. The filer must certify that shareholders authorized the resumption — either (a) by majority vote at a meeting (with date and location recited) or (b) by written consent — and may optionally specify an effective date other than the date of filing (THIRD).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
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
| `filing.entities[1].name` | text | high | Name of entity [2] |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of the FIRST options is selected (resumption.method ∈ {'meeting', 'written_consent'}). (depends on `resumption.method`)
- If resumption.method='meeting', resumption.meeting_date and resumption.meeting_location must both be non-empty. (depends on `resumption.method`, `resumption.meeting_date`, `resumption.meeting_location`)
- If set, resumption.meeting_date is not in the future. (depends on `resumption.meeting_date`)
- filing.signer.printed_name_and_capacity is non-empty (signer must be a duly authorized officer per 13-C MRSA §121.5; cannot be auto-validated from form alone). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.{name,phone,email} are all non-empty (per cover-letter NOTE). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "resumption": {
    "method": "meeting",
    "meeting_date": "2026-01-15",
    "meeting_location": "Sample Value",
    "effective_date": "2026-01-15"
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
