# SKILL: Filling NP_MNPCA-15

**Form:** Application for the Use of an Indistinguishable Name (Nonprofit)  
**Entity type:** Nonprofit Corporation  
**When to use:** Existing Maine nonprofit corporation consents to allow another entity (the 'requestor') to use a name that is indistinguishable from the consenting corporation's current name, pursuant to 13-B MRSA §301-A.4. The consenting corporation simultaneously commits to change its own name to a distinguishable name. Captures: consenting entity name, the indistinguishable name being consented to, the requestor entity name, the consenting entity's new (distinguishable) name, and the consenting entity's Maine registered office.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.name` | text | high | (Name of Corporation Allowing Indistinguishable Name) |
| `entity.new_name` | text | high | THIRD: The entity in possession of the name must change its name to:* ___ |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | DATED ___ |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |

_Showing 12 of 22 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (consenting corporation's current name) is non-empty. (depends on `entity.name`)
- indistinguishable_name.proposed_name is non-empty (FIRST line 1 — the name being consented to). (depends on `indistinguishable_name.proposed_name`)
- indistinguishable_name.requestor_name is non-empty (FIRST line 2 — the entity that will use the name). (depends on `indistinguishable_name.requestor_name`)
- entity.new_name is non-empty (THIRD — the consenting entity's new distinguishable name). (depends on `entity.new_name`)
- entity.new_name must differ from entity.name (the whole point of this filing is to change the name to something distinguishable). (depends on `entity.name`, `entity.new_name`)
- registered_agent.physical_address is non-empty (FOURTH). (depends on `registered_agent.physical_address`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- At least one of filing.signer or filing.signer_2 printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer_2.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "new_name": "Wabanaki Widgets, Inc."
  },
  "indistinguishable_name": {
    "proposed_name": "Sample Value",
    "requestor_name": "Sample Value"
  },
  "registered_agent": {
    "physical_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "signer_2": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
