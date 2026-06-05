# SKILL: Filling MARK_mark6

**Form:** Voluntary Cancellation of Registration of Mark  
**Entity type:** Trademark / Service Mark  
**When to use:** Voluntarily cancel an existing Maine trademark/service-mark registration under 10 MRSA §1527.1.B. Identifies the mark by charter number, text words, and design features, and is signed by the registrant or assignee of record.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

## Conditional logic

- At least one of mark.charter_number, mark.text_words.line1, or mark.design_features.line1 is non-empty (the mark must be identifiable for cancellation). (depends on `mark.charter_number`, `mark.text_words.line1`, `mark.design_features.line1`)
- mark.signer.printed_name_and_capacity is non-empty. (depends on `mark.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.expedited_service is exactly one of hold_for_pickup | 24h_next_business_day | immediate_same_day. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "mark": {
    "charter_number": "P99999",
    "text_words": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "design_features": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    }
  },
  "filing": {
    "date_signed": "2026-01-15",
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
