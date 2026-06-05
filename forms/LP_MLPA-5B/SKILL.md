# SKILL: Filling LP_MLPA-5B

**Form:** Statement to Add/Delete/Change Location Where an Assumed Name is Used in Maine (Limited Partnership)  
**Entity type:** Limited Partnership  
**When to use:** Update the location(s) where a Maine limited partnership uses a previously filed assumed name (DBA) under 31 MRSA §1308.2. The form (3 pages, 29 widgets, $35 base fee) captures the LP's real name, the assumed name affected (FIRST), the location currently associated with that assumed name (SECOND), and one or more elections — Change location(s) / Add additional location(s) / Delete location(s) — together with a 2-line free-text description of the change (THIRD). An optional exhibit may be attached if more locations are needed than fit inline. Sibling of LP_MLPA-5A (terminate an assumed name); same single-slot signer block (individual GP OR entity GP). Same body shape as the LLC_MLLC-* and LLP_MLLP-* assumed-name-modification forms in the family.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `assumed_name.current_location` | text | high | SECOND: The location where the assumed name is currently being used, if any |
| `assumed_name.name` | text | high | FIRST: The assumed name of the limited partnership affected by this change |
| `assumed_name_change.add_locations` | text | high | THIRD: Add additional location(s) |
| `assumed_name_change.additional_locations_attached` | text | high | Additional locations are attached as Exhibit ___, and made a part hereof |
| `assumed_name_change.additional_locations_exhibit_letter` | text | high | Exhibit ___ [additional locations] |
| `assumed_name_change.change_locations` | text | high | THIRD: Change location(s) |
| `assumed_name_change.delete_locations` | text | high | THIRD: Delete location(s) |
| `assumed_name_change.description.line1` | text | high | THIRD: (provide description of change/addition/deletion in the space provide below) — line 1 |
| `assumed_name_change.description.line2` | text | high | THIRD: change description — line 2 |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Real Name of Limited Partnership) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |

## Conditional logic

- entity.name (the LP's real name) is non-empty. (depends on `entity.name`)
- assumed_name.name (the DBA being modified) is non-empty. (depends on `assumed_name.name`)
- assumed_name.name is different from entity.name (an assumed-name modification is meaningless if the names match). (depends on `assumed_name.name`, `entity.name`)
- At least one of assumed_name_change.{change_locations, add_locations, delete_locations} is true (form text 'intends to:' implies at least one action). (depends on `assumed_name_change.change_locations`, `assumed_name_change.add_locations`, `assumed_name_change.delete_locations`)
- If any change action is selected, assumed_name_change.description (after concatenating line1+line2) must be non-empty. (depends on `assumed_name_change.change_locations`, `assumed_name_change.add_locations`, `assumed_name_change.delete_locations`, `assumed_name_change.description.line1`, `assumed_name_change.description.line2`)
- If assumed_name_change.additional_locations_attached is true, assumed_name_change.additional_locations_exhibit_letter must be non-empty. (depends on `assumed_name_change.additional_locations_attached`, `assumed_name_change.additional_locations_exhibit_letter`)
- Exactly one signer block is populated: either filing.signer.printed_name (individual GP) OR (filing.signer_entity.name AND filing.signer_entity.signer_printed_name_and_capacity) (entity GP). Both blocks empty or both populated is a fill error. (depends on `filing.signer.printed_name`, `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- If filing.signer_entity.name is populated, filing.signer_entity.signer_printed_name_and_capacity must also be populated (and vice versa). (depends on `filing.signer_entity.name`, `filing.signer_entity.signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.entities[0].name matches entity.name. (depends on `filing.entities[0].name`, `entity.name`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "assumed_name": {
    "name": "Sample Value",
    "current_location": "Sample Value"
  },
  "assumed_name_change": {
    "change_locations": "Sample Value",
    "add_locations": "Sample Value",
    "delete_locations": "Sample Value",
    "description": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    }
  }
}
```
