# SKILL: Filling CORP_SOPAPPT

**Form:** Statement of Appointment of Agent for Service of Process for a Nonfiling Domestic Entity or a Nonqualified Foreign Entity  
**Entity type:** Business Corporation  
**When to use:** Appoint an agent for service of process for a nonfiling domestic entity (e.g., general partnership, sole proprietorship, trust, unincorporated association — entities not required to file formation documents with SOS) or a nonqualified foreign entity transacting business in Maine, under 5 MRSA §112. The appointment is effective for 5 years from filing. Captures the entity's legal name and free-text type, jurisdiction of organization, and the agent's name and physical address (P.O. Box explicitly prohibited). Filing fee $100. Distinct from the registered_agent.* and clerk.* patterns used by formation/qualification forms — this form has neither because the appointing entity is neither registered nor qualified.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `agent.name` | text | high | THIRD: The name and address of the Agent for Service of Process is — (name of agent) |
| `agent.physical_address` | text | high | (physical address – street, city, state and zip code – No P.O. Box) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | SECOND: Jurisdiction of organization |
| `entity.name` | text | high | FIRST: The name and entity type of the domestic nonfiling or foreign nonqualified entity is — (entity name) |
| `entity.type` | text | high | (type of entity) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.type is non-empty. (depends on `entity.type`)
- entity.home_jurisdiction is non-empty. (depends on `entity.home_jurisdiction`)
- agent.name is non-empty. (depends on `agent.name`)
- agent.physical_address is non-empty and does not contain 'P.O. Box', 'PO Box', 'P.O.Box', or 'Post Office Box' (case-insensitive). Form explicitly prohibits P.O. Box. (depends on `agent.physical_address`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D signer per the * footnote). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "type": "Sample Value",
    "home_jurisdiction": "Sample Value"
  },
  "agent": {
    "name": "Sample Value",
    "physical_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
