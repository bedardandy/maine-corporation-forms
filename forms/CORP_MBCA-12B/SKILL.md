# SKILL: Filling CORP_MBCA-12B

**Form:** Application of Withdrawal (Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Withdraw a foreign business corporation's authority to transact business in Maine under 13-C MRSA §1521 or §1523. The form recites the foreign corporation's home jurisdiction, the date Maine authority was granted, an optional FOURTH block for withdrawal upon conversion to a nonfiling entity (entity type + governing jurisdiction), and a FIFTH block providing a mailing address for service of process during the withdrawal period. Signed by a duly authorized officer.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | FIRST: The jurisdiction of its incorporation is |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation) |
| `entity.maine_authorization_date` | text | high | SECOND: The date on which it was authorized to do business in the State of Maine is |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ____ |

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and is not 'Maine' or 'ME' (foreign withdrawal implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is non-empty and on or before filing.date_signed. (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- FOURTH is an optional all-or-nothing block: either both withdrawal.conversion.new_entity_type AND withdrawal.conversion.governing_jurisdiction are set, or both are empty. (depends on `withdrawal.conversion.new_entity_type`, `withdrawal.conversion.governing_jurisdiction`)
- withdrawal.service_of_process_mailing_address is non-empty (FIFTH requires a mailing address for service of process). (depends on `withdrawal.service_of_process_mailing_address`)
- filing.signer.printed_name_and_capacity is non-empty (must be signed by a duly authorized officer per 13-C MRSA §121.5). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15"
  },
  "withdrawal": {
    "conversion": {
      "new_entity_type": "Sample Value",
      "governing_jurisdiction": "Sample Value"
    },
    "service_of_process_mailing_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
