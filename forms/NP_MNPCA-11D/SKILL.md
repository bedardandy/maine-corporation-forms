# SKILL: Filling NP_MNPCA-11D

**Form:** Articles of Dissolution (Domestic Nonprofit Corporation, post-intent)  
**Entity type:** Nonprofit Corporation  
**When to use:** Dissolve a Maine domestic nonprofit corporation under 13-B MRSA §1104 by filing Articles of Dissolution following a previously-filed Statement of Intent to Dissolve. Recites the prior intent-filing date, attests via SECOND/THIRD/FOURTH/FIFTH that distribution of assets, satisfaction of liabilities, and any required vote conditions have been met, and provides the Maine registered-office address. Sister to NP_MNPCA-11 (intent), NP_MNPCA-11A, NP_MNPCA-11C, NP_MNPCA-11E in the dissolution family.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `dissolution.intent_filed_date` | text | high | FIRST: A statement of intent to dissolve the corporation was filed with the Secretary of State on ___ (date) |
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

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- dissolution.intent_filed_date is non-empty and on or before filing.date_signed (Articles of Dissolution must post-date the prior intent filing). (depends on `dissolution.intent_filed_date`, `filing.date_signed`)
- registered_office.address_line2 (the wide labeled street/city/state/zip line) is non-empty. (depends on `registered_office.address_line2`)
- filing.signer_1.printed_name_and_capacity is non-empty (13-B MRSA §104.1.B requires at least one authorized officer to sign). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "dissolution": {
    "intent_filed_date": "2026-01-15"
  },
  "registered_office": {
    "address_line1": "Sample Value",
    "address_line2": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer_1": {
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
