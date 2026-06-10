# SKILL: Filling CORP_MBCA-19A

**Form:** Articles of Charter Surrender (Upon Domestication)  
**Entity type:** Business Corporation  
**When to use:** Surrender the Maine charter of a domestic business corporation in connection with its domestication into a foreign jurisdiction under 13-C MRSA §§924–925. Records the effective date of domestication, the new home jurisdiction, the corporation's appointment of the Secretary of State as agent for service of process for shareholder-appraisal-rights enforcement, and a mailing address to which the SOS will forward such process. Filing fee $90 (per page 0 header).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `domestication.effective_date` | text | high | FIRST: ...the effective date of the domestication is (date) |
| `domestication.new_jurisdiction` | text | high | THIRD: The corporation's new jurisdiction of incorporation is |
| `domestication.service_of_process_mailing_address` | text | high | FOURTH: ...mailing address to which the Secretary of State may mail a copy of any process served on the Secretary of State. (mailing address) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- domestication.effective_date is non-empty. (depends on `domestication.effective_date`)
- domestication.effective_date is on or after filing.date_signed (effective date can be the filing date or a later specified date, but cannot precede the filing). (depends on `domestication.effective_date`, `filing.date_signed`)
- domestication.new_jurisdiction is non-empty. (depends on `domestication.new_jurisdiction`)
- domestication.new_jurisdiction is not 'Maine' or 'ME' (a domestication into Maine would not require an outbound charter surrender). (depends on `domestication.new_jurisdiction`)
- domestication.service_of_process_mailing_address is non-empty (mandatory under §924.4 for SOS process forwarding). (depends on `domestication.service_of_process_mailing_address`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D); the signer must be an officer or duly authorized representative per 13-C §924.1. (depends on `filing.signer.printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "domestication": {
    "effective_date": "2026-01-15",
    "new_jurisdiction": "Sample Value",
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
      },
      {
        "name": "Sample Value"
      }
    ]
  }
}
```
