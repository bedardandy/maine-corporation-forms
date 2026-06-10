# SKILL: Filling LLC_MLLC-14A

**Form:** Certificate of Resumption (for a Maine LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Resume the transaction of business for a Maine domestic limited liability company that has previously suspended operations, pursuant to 31 MRSA §1665.6. Body has only three fillable widgets (entity name, dated, signer name+capacity); FIRST and SECOND are declarative-only paragraphs with no widgets. Page 1 is the standard cover-letter primitive.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of the Maine Limited Liability Company) |
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

_Showing 12 of 17 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- filing.signer.printed_name_and_capacity is non-empty (signer must be a person authorized by the LLC per 31 MRSA §1676.1.B). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty (per cover-letter NOTE: omission causes return.). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- At most one of the three expedite checkboxes is selected (or zero, defaulting to standard processing). (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "expedited_service": {},
    "total_fees_dollars": "Sample Value",
    "contact": {
      "name": "Sample Value"
    },
    "entities": [
      {
        "name": "Sample Value"
      },
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
