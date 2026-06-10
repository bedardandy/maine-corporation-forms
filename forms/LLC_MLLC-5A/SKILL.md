# SKILL: Filling LLC_MLLC-5A

**Form:** Termination of Statement of Intention to Transact Business Under an Assumed or Fictitious Name (Maine or Foreign LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Terminate a previously filed Statement of Intention to Transact Business Under an Assumed or Fictitious Name for a Maine or Foreign LLC under 31 MRSA §1510.7 (and §1676.1B for the signature requirement). Captures the LLC's legal name, the assumed/fictitious name being terminated, and up to two parallel 'Authorized Person' signer blocks.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
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
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |

_Showing 12 of 19 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- filing.terminated_fictitious_name is non-empty (the SECOND recital identifies which name is being terminated). (depends on `filing.terminated_fictitious_name`)
- filing.terminated_fictitious_name is different from entity.name (a fictitious-name termination is meaningless if the names match). (depends on `filing.terminated_fictitious_name`, `entity.name`)
- At least one of {filing.signer_1.printed_name_and_capacity, filing.signer_2.printed_name_and_capacity} is non-empty (per page-0 footnote requiring a person authorized by the LLC to sign). (depends on `filing.signer_1.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC"
  },
  "filing": {
    "terminated_fictitious_name": "Sample Value",
    "date_signed": "2026-01-15",
    "signer_1": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_2": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    },
    "expedited_service": {}
  }
}
```
