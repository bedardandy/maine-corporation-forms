# SKILL: Filling NP_MNPCA-5A

**Form:** Termination of Statement of Intention to Carry on Activities Under an Assumed or Fictitious Name (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Terminate a previously filed Statement of Intention to Carry on Activities Under an Assumed or Fictitious Name (NP_MNPCA-5) for a Maine domestic nonprofit corporation under 13-B MRSA §308-A.8. Records the corporation's real (legal) name, the specific assumed/fictitious name being terminated, the Maine registered office address, and dual signatures by authorized officers. Filing fee is $5.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `assumed_name.name` | text | high | SECOND: The corporation intends to terminate the assumed or fictitious name of ___ |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Real Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ___ (left side, y≈320-341) |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

## Conditional logic

- entity.name (real corporate name) is non-empty. (depends on `entity.name`)
- assumed_name.name (the assumed/fictitious name being terminated) is non-empty. (depends on `assumed_name.name`)
- assumed_name.name should differ from entity.name (an assumed name that matches the legal name is meaningless). (depends on `assumed_name.name`, `entity.name`)
- registered_office.address_line2 (the wide labeled street/city/state/zip line) is non-empty. (depends on `registered_office.address_line2`)
- filing.signer_1.printed_name_and_capacity is non-empty (at least one duly authorized officer must sign per 13-B MRSA §104.1.B). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "assumed_name": {
    "name": "Sample Value"
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
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
