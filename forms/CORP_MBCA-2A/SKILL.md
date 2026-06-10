# SKILL: Filling CORP_MBCA-2A

**Form:** Consent Terminating Name Registration (Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Terminate the registration of a foreign business corporation's name in Maine under 13-C MRSA §403.5, releasing the name so another corporation may use it. The form recites the foreign corporation's home jurisdiction, principal office address, and date of incorporation, and is signed by a duly authorized officer (per the page-1 footnote citing §1217.5).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.formation_date_in_home_jurisdiction` | text | high | SECOND: The date of its incorporation is |
| `entity.home_jurisdiction` | text | high | FIRST: The state or country under the laws of which it is incorporated is |
| `entity.home_jurisdiction_name` | text | high | (Foreign Registered Name) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |
| `filing.date_signed` | text | high | DATED |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and not 'Maine'/'ME' (foreign-name-registration termination implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- entity.principal_office.physical_address is non-empty (filled into Text3 and/or Text4). (depends on `entity.principal_office.physical_address`)
- entity.formation_date_in_home_jurisdiction is non-empty and on or before filing.date_signed. (depends on `entity.formation_date_in_home_jurisdiction`, `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "principal_office": {
      "physical_address": "Sample Value"
    },
    "formation_date_in_home_jurisdiction": "2026-01-15"
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
    }
  }
}
```
