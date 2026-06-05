# SKILL: Filling CORP_MBCA-1

**Form:** Application for Reservation of Name  
**Entity type:** Business Corporation  
**When to use:** Reserve a corporate name for 120 days under 13-C MRSA §402.1 prior to incorporating; reservation cannot be renewed.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

## Conditional logic

- name_reservation.name_to_reserve is non-empty. (depends on `name_reservation.name_to_reserve`)
- name_reservation.applicant.name and name_reservation.applicant.address are both non-empty. (depends on `name_reservation.applicant.name`, `name_reservation.applicant.address`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "name_reservation": {
    "name_to_reserve": "Sample Value",
    "applicant": {
      "name": "Sample Value",
      "address": "Sample Value",
      "printed_name_and_capacity": "Sample Value"
    }
  },
  "filing": {
    "date_signed": "2026-01-15",
    "entities[0]": {
      "name": "Sample Value"
    },
    "entities[1]": {
      "name": "Sample Value"
    },
    "expedited_service": "Sample Value"
  }
}
```
