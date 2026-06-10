# SKILL: Filling CORP_MBCA-9A

**Form:** Articles of Amendment (Reorganization ordered or decreed by a court)  
**Entity type:** Business Corporation  
**When to use:** File Articles of Amendment for a Maine domestic business corporation when the amendment is ordered or decreed by a court (typically a Chapter 11 bankruptcy reorganization) under 13-C MRSA §1008. The signer is an individual designated by the court — not a corporate officer — and shareholder approval is not required because the court's order substitutes for the usual approval mechanism. The form supports up to two parallel court-designated signers.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.court_order_date` | text | high | FIRST: ...the date of the court's order or decree approving these Articles of Amendment is ___ |
| `amendment.exhibit_letter` | text | high | FIRST: The text of each amendment approved by the court is set forth in Exhibit ___ attached and made a part hereof. |
| `amendment.reorganization_proceeding_title` | text | high | SECOND: The title of the reorganization proceeding in which the order or decree was entered: |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- amendment.exhibit_letter is non-empty (the text of each amendment must be attached as an exhibit per FIRST). (depends on `amendment.exhibit_letter`)
- amendment.court_order_date is non-empty and not in the future. (depends on `amendment.court_order_date`)
- amendment.court_order_date is on or before filing.date_signed (the court order must exist before the filing is executed). (depends on `amendment.court_order_date`, `filing.date_signed`)
- amendment.reorganization_proceeding_title is non-empty. (depends on `amendment.reorganization_proceeding_title`)
- At least one of filing.signer.printed_name_and_capacity or filing.signer_2.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.expedited_service is exactly one of hold_for_pickup | 24h_next_business_day | immediate_same_day. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "amendment": {
    "exhibit_letter": "Sample Value",
    "court_order_date": "2026-01-15",
    "reorganization_proceeding_title": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_2": {
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
