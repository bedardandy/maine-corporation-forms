# SKILL: Filling LLP_MLLP-12B

**Form:** Cancellation of Authority to Do Business (Foreign Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Cancel a foreign LLP's authority to do business in Maine under 31 MRSA §857. Captures the LLP's home-jurisdiction name, the Maine name (if different) used at qualification, the home jurisdiction, the original Maine authorization date, and the principal/registered office address. Signed by at least one partner OR any duly authorized person per the page-1 footnote.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | SECOND: The jurisdiction of its organization is |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Liability Partnership in Jurisdiction of Organization) |
| `entity.maine_authorization_date` | text | high | THIRD: The date on which it was authorized to do business in the State of Maine is |
| `entity.principal_office.physical_address` | text | high | SIXTH: The address of the principal or registered office of the limited liability partnership, wherever located, is (street, city, state and zip) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and not 'Maine'/'ME' (foreign cancellation implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is non-empty and on or before filing.date_signed (cannot cancel before initial authorization). (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- entity.principal_office.physical_address is non-empty. (depends on `entity.principal_office.physical_address`)
- Either (a) filing.signer.printed_name_and_capacity (individual path) is non-empty, or (b) filing.signer.entity_name AND filing.signer.entity_signer_printed_name_and_capacity (entity path) are both non-empty. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer.entity_name`, `filing.signer.entity_signer_printed_name_and_capacity`)
- If filing.signer.entity_name is set, filing.signer.entity_signer_printed_name_and_capacity must also be set, and vice versa. (depends on `filing.signer.entity_name`, `filing.signer.entity_signer_printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15",
    "principal_office": {
      "physical_address": "Sample Value"
    }
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value",
      "entity_name": "Sample Value"
    }
  }
}
```
