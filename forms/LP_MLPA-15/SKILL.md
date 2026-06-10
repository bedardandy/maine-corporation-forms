# SKILL: Filling LP_MLPA-15

**Form:** Application for the Use of an Indistinguishable Name  
**Entity type:** Limited Partnership  
**When to use:** A Maine limited partnership consents to another entity's use of an indistinguishable name pursuant to 31 MRSA §1308.D.1. The consenting LP undertakes to change its own name to one that is distinguishable on SOS records, and the application MUST be accompanied by the corresponding name-change filing (e.g., LP_MLPA-9 Certificate of Amendment).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Limited Partnership Allowing Indistinguishable Name) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | Dated |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |

_Showing 12 of 20 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the consenting LP) is non-empty. (depends on `entity.name`)
- name_consent.indistinguishable_name is non-empty. (depends on `name_consent.indistinguishable_name`)
- name_consent.requestor.name is non-empty. (depends on `name_consent.requestor.name`)
- name_consent.indistinguishable_name differs from entity.name (case-sensitive — 'indistinguishable' means differing only on insubstantial grounds, not literally identical). (depends on `name_consent.indistinguishable_name`, `entity.name`)
- name_consent.replacement_name is non-empty (the consenting LP commits to renaming itself). (depends on `name_consent.replacement_name`)
- name_consent.replacement_name differs from both entity.name (the old name) and name_consent.indistinguishable_name (the granted name). (depends on `name_consent.replacement_name`, `entity.name`, `name_consent.indistinguishable_name`)
- name_consent.replacement_name contains a valid LP suffix per 31 MRSA §1308 (e.g., 'L.P.', 'LP', 'Limited Partnership'). (depends on `name_consent.replacement_name`)
- filing.signer.printed_name_and_capacity is non-empty (must be a general partner per footnote **). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "name_consent": {
    "indistinguishable_name": "Sample Value",
    "requestor": {
      "name": "Sample Value"
    },
    "replacement_name": "Sample Value"
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
