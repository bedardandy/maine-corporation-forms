# SKILL: Filling NP_MNPCA-12B

**Form:** Application for Surrender of Authority to Carry on Activities (Foreign Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Surrender a foreign nonprofit corporation's authority to carry on activities in Maine under 13-B MRSA §1208. Recites the foreign corporation's home jurisdiction, the date Maine authority was granted, the surrender of registered-agent authority, a post-surrender mailing address for service of process via the Secretary of State, and the principal/registered office address.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | FIRST: The jurisdiction of its incorporation is ___ |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation) |
| `entity.maine_authorization_date` | text | high | SECOND: The date on which it was authorized to carry on activities in the State of Maine is ___ |
| `entity.principal_office.physical_address` | text | high | SIXTH: The address of the principal or registered office of the corporation, wherever located, is ___ (street, city, state and zip code) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and is not 'Maine' or 'ME' (foreign-surrender implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is non-empty and on or before filing.date_signed (cannot surrender authority before it was granted). (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- withdrawal.service_of_process_mailing_address is non-empty (FIFTH requires a mailing address for SOS to forward post-surrender process). (depends on `withdrawal.service_of_process_mailing_address`)
- entity.principal_office.physical_address is non-empty (SIXTH). (depends on `entity.principal_office.physical_address`)
- filing.signer.printed_name_and_capacity is non-empty (form footnote: must be 'any duly authorized individual' per 13-B MRSA §104.1.B). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15",
    "principal_office": {
      "physical_address": "Sample Value"
    }
  },
  "withdrawal": {
    "service_of_process_mailing_address": "Sample Value"
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
