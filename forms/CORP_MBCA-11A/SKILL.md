# SKILL: Filling CORP_MBCA-11A

**Form:** Articles of Revocation of Dissolution  
**Entity type:** Business Corporation  
**When to use:** Revoke a previously filed dissolution of a Maine domestic business corporation under 13-C MRSA §1405. Records the effective date of the original dissolution being revoked, the date the revocation was authorized, the body that authorized the revocation (incorporators / board / board with prior shareholder authorization / shareholders), and the signature of any duly authorized officer or clerk.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity(s) on the submitted filings [2] |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name matches the corporation's name of record at the SOS (the entity must currently exist in dissolved status). (depends on `entity.name`)
- revocation.authorization_date is within 120 days after revocation.original_dissolution_date (per 13-C MRSA §1405.1). (depends on `revocation.authorization_date`, `revocation.original_dissolution_date`)
- revocation.original_dissolution_date is on or before filing.date_signed (cannot revoke a dissolution that has not yet occurred). (depends on `revocation.original_dissolution_date`, `filing.date_signed`)
- revocation.authorization_date is on or before filing.date_signed. (depends on `revocation.authorization_date`, `filing.date_signed`)
- Exactly one of the four THIRD checkboxes is selected (revocation.authority_type resolves to a single enum value). (depends on `revocation.authority_type`)
- filing.signer.printed_name_and_capacity includes both a name and a capacity (officer title or 'Clerk') — 13-C MRSA §121.5 limits signing authority. (depends on `filing.signer.printed_name_and_capacity`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name on the cover letter matches entity.name on the body. (depends on `filing.entities[0].name`, `entity.name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "revocation": {
    "original_dissolution_date": "2026-01-15",
    "authorization_date": "2026-01-15",
    "authority_type": "incorporators"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
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
