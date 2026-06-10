# SKILL: Filling LLP_MLLP-15

**Form:** Application for the Use of an Indistinguishable Name (LLP)  
**Entity type:** Limited Liability Partnership  
**When to use:** An existing Maine LLP that holds a name now wanted by another applicant uses this form (per 31 MRSA §803-A.4 / §860.1) to (a) consent to the requestor's use of the indistinguishable name and (b) commit to changing its own name to a new, distinguishable name. The form must be accompanied by the applicable name-change form for the existing LLP (FIRST/THIRD references item Third).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Limited Liability Partnership Allowing Indistinguishable Name) |
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

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the consenting LLP) is non-empty. (depends on `entity.name`)
- name_change.indistinguishable_name is non-empty. (depends on `name_change.indistinguishable_name`)
- name_change.requestor_name is non-empty. (depends on `name_change.requestor_name`)
- name_change.new_name is non-empty (the existing LLP must commit to a new distinguishable name). (depends on `name_change.new_name`)
- filing.signer.printed_name_and_capacity is non-empty (must be at least one partner per the page-0 footnote and 31 MRSA §826.1.B / §860.1). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "name_change": {
    "indistinguishable_name": "Sample Value",
    "requestor_name": "Sample Value",
    "new_name": "Sample Value"
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
