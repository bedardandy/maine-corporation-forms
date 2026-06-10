# SKILL: Filling NP_MNP-3

**Form:** Change of Contact Person and/or Address (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Update the contact person and/or address for an existing Maine domestic nonprofit corporation pursuant to 13-B MRSA §910. Captures (FIRST) one of four mutually exclusive change types (A: address only; B: contact person + address; C: contact person only; D: name change of current contact person), (SECOND) the current contact person on record, (THIRD) the new contact person and/or address per the FIRST selection, and the signer block (Shape A: name + title).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `contact_change.action_type` | text | high | FIRST: A. [ ] change of address (fills multiple widgets) |
| `contact_change.current_address` | text | high | SECOND: (street, city, state and zip code) |
| `contact_change.current_name` | text | high | SECOND: (name of current contact person) |
| `contact_change.new_mailing_address` | text | high | THIRD: (mailing address if different from above) |
| `contact_change.new_name` | text | high | THIRD: (name of new contact person or new name of current contact person) |
| `contact_change.new_physical_address` | text | high | THIRD: (physical location, not P.O. Box – street, city, state and zip code) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

_Showing 12 of 24 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of FIRST A/B/C/D options is selected (form instructs 'X all boxes that apply' but the four options are semantically mutually exclusive — only one type of change per filing). (depends on `contact_change.action_type`)
- contact_change.current_name and contact_change.current_address are non-empty (SECOND block — always required to identify which record is being changed). (depends on `contact_change.current_name`, `contact_change.current_address`)
- If contact_change.action_type ∈ {'change_of_contact_person_and_address', 'change_of_contact_person', 'change_in_name_of_current_contact_person'}, contact_change.new_name must be non-empty. (depends on `contact_change.action_type`, `contact_change.new_name`)
- If contact_change.action_type ∈ {'change_of_address', 'change_of_contact_person_and_address'}, contact_change.new_physical_address must be non-empty. (depends on `contact_change.action_type`, `contact_change.new_physical_address`)
- filing.signer.printed_name and filing.signer.title are non-empty (Shape A). (depends on `filing.signer.printed_name`, `filing.signer.title`)
- Per page-1 footnote: if contact_change.action_type ∈ {'change_of_address', 'change_in_name_of_current_contact_person'} (A or D), filing.signer.title must indicate 'Contact Person'; if action_type ∈ {'change_of_contact_person_and_address', 'change_of_contact_person'} (B or C), filing.signer.title must be 'Secretary' or 'Clerk'. (depends on `contact_change.action_type`, `filing.signer.title`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "contact_change": {
    "action_type": "Sample Value",
    "current_name": "Sample Value",
    "current_address": "Sample Value",
    "new_name": "Sample Value",
    "new_physical_address": "Sample Value",
    "new_mailing_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
