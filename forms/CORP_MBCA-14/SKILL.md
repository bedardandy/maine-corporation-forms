# SKILL: Filling CORP_MBCA-14

**Form:** Certificate of Excuse (for a Maine Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** File a Certificate of Excuse for a Maine domestic business corporation pursuant to 13-C MRSA §1621.4 — the simplified end-of-life procedure used when a corporation has ceased to transact business and is not indebted to the State for annual reports or fees. The body has only one substantive election (THIRD: optional non-default effective date); the FIRST and SECOND paragraphs are declarative recitals (no checkboxes), so the act of filing constitutes the certification.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `excuse.future_effective_date` | text | high | THIRD: The effective date of the certificate of excuse (if other than the date of filing of the certificate of excuse): |
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
- filing.signer.printed_name_and_capacity is non-empty (signer must be a duly authorized officer or the clerk per 13-C MRSA §121.5; cannot be auto-validated from form alone). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- If excuse.future_effective_date is set, it must be on or after filing.date_signed (the certificate cannot take effect before it is filed). (depends on `excuse.future_effective_date`, `filing.date_signed`)
- filing.contact.{name,phone,email} are all non-empty (per cover-letter NOTE). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (the cover letter must identify at least one filing). (depends on `filing.entities[0].name`)
- At most one of the three expedited-service tiers is selected (hold_for_pickup | 24h_next_business_day | immediate_same_day). Zero is also valid (standard processing). (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "excuse": {
    "future_effective_date": "2026-01-15"
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
    "total_fees_dollars": "Sample Value"
  }
}
```
