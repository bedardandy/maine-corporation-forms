# SKILL: Filling NP_MNPCA-14A

**Form:** Certificate of Resumption (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Resume the carrying-on of activities for a Maine domestic nonprofit corporation that has previously suspended/forfeited its existence, pursuant to 13-B MRSA §1301.6. FIRST recites that the certificate was adopted by the corporation's members or directors on a stated date and location, either at a meeting legally called and held or by unanimous written consent. SECOND certifies that a majority of members or directors have voted to resume carrying on activities. THIRD records the (current) Maine registered office address. FOURTH classifies the corporation as a public-benefit or mutual-benefit corporation. After filing, the corporation is required to file annual reports beginning with the next reporting deadline.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation) |
| `entity.nonprofit_type` | text | high | FOURTH: ("X" one box only) [ ] public benefit corporation (fills multiple widgets) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 26 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of FIRST [members]/[directors] is selected (resumption.adopting_body set). (depends on `resumption.adopting_body`)
- Exactly one of FIRST [meeting]/[written consent] is selected (resumption.method set). (depends on `resumption.method`)
- Exactly one of SECOND [members]/[directors] is selected (resumption.voting_body set). (depends on `resumption.voting_body`)
- resumption.adoption_date is non-empty and parses as a date on or before filing.date_signed. (depends on `resumption.adoption_date`, `filing.date_signed`)
- If resumption.method='meeting', resumption.adoption_location is non-empty. (depends on `resumption.method`, `resumption.adoption_location`)
- registered_office.address.line2 is non-empty (the full-width continuation line is the canonical address line; line1 may be a leading fragment). (depends on `registered_office.address.line2`)
- Exactly one of FOURTH [public benefit]/[mutual benefit] is selected (entity.nonprofit_type set). (depends on `entity.nonprofit_type`)
- filing.signer.printed_name_and_capacity is non-empty (form footnote * requires signature by any authorized officer per 13-B MRSA §104.1.B). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "resumption": {
    "adopting_body": "Sample Value",
    "adoption_date": "2026-01-15",
    "adoption_location": "Sample Value",
    "method": "Sample Value",
    "voting_body": "Sample Value"
  },
  "registered_office": {
    "address": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    }
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
