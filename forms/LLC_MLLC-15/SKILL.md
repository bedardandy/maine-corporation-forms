# SKILL: Filling LLC_MLLC-15

**Form:** Application for the Use of an Indistinguishable Name  
**Entity type:** Limited Liability Company  
**When to use:** A Maine LLC consents to another entity's use of an indistinguishable name pursuant to 31 MRSA §1508.4. The consenting LLC undertakes to change its own name to one that is distinguishable on SOS records, and the application MUST be accompanied by the corresponding name-change filing (e.g., MLLC-9 Articles of Amendment).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Limited Liability Company Allowing Indistinguishable Name) |
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

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the LLC granting consent) is non-empty. (depends on `entity.name`)
- name_consent.indistinguishable_name is non-empty. (depends on `name_consent.indistinguishable_name`)
- name_consent.requestor.name is non-empty. (depends on `name_consent.requestor.name`)
- name_consent.indistinguishable_name differs from entity.name (case-sensitive, since indistinguishable means differing on insubstantial grounds — e.g., punctuation or spacing — but not literally identical). (depends on `name_consent.indistinguishable_name`, `entity.name`)
- name_consent.replacement_name is non-empty (the consenting LLC commits to renaming itself). (depends on `name_consent.replacement_name`)
- name_consent.replacement_name differs from both entity.name (the old name) and name_consent.indistinguishable_name (the granted name) — i.e., the consenting LLC must pick a name truly distinguishable from the requestor's. (depends on `name_consent.replacement_name`, `entity.name`, `name_consent.indistinguishable_name`)
- name_consent.replacement_name contains a valid LLC suffix per 31 MRSA §1508 (e.g., 'L.L.C.', 'LLC', 'Limited Liability Company', 'L.C.'). (depends on `name_consent.replacement_name`)
- filing.signer_1.printed_name_and_capacity is non-empty (statute mandates at least one authorized-person signature). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC"
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
    "signer_1": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_2": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
