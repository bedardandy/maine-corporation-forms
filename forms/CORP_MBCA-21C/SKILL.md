# SKILL: Filling CORP_MBCA-21C

**Form:** Statement of Abandonment of Entity Conversion  
**Entity type:** Business Corporation  
**When to use:** Abandon a previously filed Articles of Entity Conversion (Form MBCA-21) OR Articles of Charter Surrender (Form MBCA-20A) before the conversion becomes effective, pursuant to 13-C MRSA §958. Filed by a domestic business corporation to halt a pending entity conversion. The form (2 pages, 18 widgets) captures the entity name, the date the original conversion was scheduled to become effective (FIRST), the filing date (DATED), the signer's name and capacity (Shape D), plus the standard cover-letter primitive on page 2. Filing fee is $35 per the page-0 header. Direct sibling of MBCA-20B (which abandons the nonprofit-conversion form MBCA-20).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `conversion.future_effective_date` | text | high | FIRST: ...before the entity conversion has become effective on ___ |
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

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- conversion.future_effective_date is non-empty (FIRST — the date the original conversion was scheduled to become effective). (depends on `conversion.future_effective_date`)
- filing.date_signed is strictly before conversion.future_effective_date — per 13-C MRSA §958, abandonment must be filed before the entity conversion becomes effective. (depends on `filing.date_signed`, `conversion.future_effective_date`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D; signer must be 'officer or other duly authorized representative' per §958.2). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "conversion": {
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
