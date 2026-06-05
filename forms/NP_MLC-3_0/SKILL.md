# SKILL: Filling NP_MLC-3_0

**Form:** Change of Clerk and/or Address (Domestic Nonprofit Corporation / Independent Local Church)  
**Entity type:** Nonprofit Corporation  
**When to use:** Update the registered clerk and/or address of record for a Maine domestic nonprofit corporation or independent local church under 13 MRSA §3025. The FIRST election picks among four mutually-exclusive change types (A: change of address only; B: change of clerk and address; C: change of clerk only; D: change in name of current clerk). SECOND recites the clerk currently on record (name + address). THIRD captures the new information per the FIRST election. Filing fee is $5.00 per the page-0 header — markedly cheaper than CLKRA-3 ($35) because §3025 governs church/nonprofit clerk changes specifically. 3 pages, 28 widgets. Sister-form NP_CLKRA-3 (multi-entity Statement of Appointment or Change of Clerk/RA) covers the broader §1604 case; MLC-3 is the §3025 narrow case for churches and small nonprofits.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `clerk_change.change_type` | text | high | FIRST A. [ ] change of address (fills multiple widgets) |
| `clerk_change.current_clerk_or_agent_address` | text | high | SECOND: (street, city, state and zip code) of current clerk |
| `clerk_change.current_clerk_or_agent_name` | text | high | SECOND: (name of current clerk) |
| `clerk_change.new_noncommercial_mailing_address` | text | high | THIRD: (mailing address if different from above) |
| `clerk_change.new_noncommercial_name` | text | high | THIRD: (name of new clerk or new name of current clerk) |
| `clerk_change.new_noncommercial_physical_address` | text | high | THIRD: (physical location, not P.O. Box - street, city, state and zip code) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.name` | text | high | (Name of Corporation) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of the FIRST checkboxes (A/B/C/D) is selected, populating clerk_change.change_type. (depends on `clerk_change.change_type`)
- clerk_change.current_clerk_or_agent_name and clerk_change.current_clerk_or_agent_address are both non-empty (SECOND mandates a full recital of the existing record). (depends on `clerk_change.current_clerk_or_agent_name`, `clerk_change.current_clerk_or_agent_address`)
- If clerk_change.change_type ∈ {'clerk', 'clerk_and_address', 'clerk_name'}, clerk_change.new_noncommercial_name must be non-empty (THIRD captures the new name). (depends on `clerk_change.change_type`, `clerk_change.new_noncommercial_name`)
- If clerk_change.change_type ∈ {'address', 'clerk_and_address'}, clerk_change.new_noncommercial_physical_address must be non-empty. (depends on `clerk_change.change_type`, `clerk_change.new_noncommercial_physical_address`)
- If clerk_change.new_noncommercial_physical_address is set, it must not be a P.O. Box (per THIRD parenthetical 'physical location, not P.O. Box'). (depends on `clerk_change.new_noncommercial_physical_address`)
- filing.signer_1.printed_name_and_capacity is non-empty (the clerk or another duly authorized officer per the page-1 footnote). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "clerk_change": {
    "change_type": "Sample Value",
    "current_clerk_or_agent_name": "Sample Value",
    "current_clerk_or_agent_address": "Sample Value",
    "new_noncommercial_name": "Sample Value",
    "new_noncommercial_physical_address": "Sample Value",
    "new_noncommercial_mailing_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
