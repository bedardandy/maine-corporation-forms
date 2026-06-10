# SKILL: Filling CORP_MBCA-5A

**Form:** Termination of Statement of Intention to Do Business Under an Assumed or Fictitious Name (Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Terminate a previously filed Statement of Intention to do business under an assumed or fictitious name for a Maine domestic business corporation pursuant to 13-C MRSA §404.8. Records the corporation's real name, the assumed/fictitious name being terminated, the signing date, and the signer (any duly authorized officer or the clerk).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.assumed_or_fictitious_name` | text | high | SECOND: The corporation intends to terminate the assumed or fictitious name of ___ |
| `entity.name` | text | high | (Real Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 18 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (real name of corporation) is non-empty. (depends on `entity.name`)
- entity.assumed_or_fictitious_name is non-empty (SECOND identifies which assumed/fictitious name is being terminated). (depends on `entity.assumed_or_fictitious_name`)
- entity.assumed_or_fictitious_name differs from entity.name (case-insensitive); a corporation cannot terminate its own legal name as a fictitious name. (depends on `entity.name`, `entity.assumed_or_fictitious_name`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future relative to the submission date. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (per cover-letter NOTE). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "assumed_or_fictitious_name": "Wabanaki Widgets, Inc."
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
