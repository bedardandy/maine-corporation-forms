# SKILL: Filling NP_CLKRA-3

**Form:** Statement of Appointment or Change of Clerk or Registered Agent  
**Entity type:** Nonprofit Corporation  
**When to use:** File a statement appointing a new clerk/registered agent or changing existing clerk/RA information (address, name) for a Maine domestic or foreign nonprofit corporation. The form template is shared with CORP_CLKRA-3 (multi-entity version) — the NP_ namespace tracks usage by the nonprofit category specifically; the form itself supports BC, NP, LLC, LP, LLP, and foreign variants.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `clerk_change.action_type` | text | high | FIRST: [ ] A new clerk or registered agent (fills multiple widgets) |
| `clerk_change.bc_authorization` | text | high | SIXTH (DOMESTIC BUSINESS CORPORATIONS ONLY): [ ] The change ... was duly authorized by the board of directors (fills multiple widgets) |
| `clerk_change.current_clerk_or_agent_name` | text | high | SECOND: (name of current clerk or registered agent) |
| `clerk_change.modify_subtype` | text | high | FIRST sub: [ ] Change of address (fills multiple widgets) |
| `clerk_change.new_commercial_cra_public_number` | text | high | FOURTH: The new CRA Public number is |
| `clerk_change.new_commercial_name` | text | high | FOURTH: The name of the new CRA is |
| `clerk_change.new_noncommercial_mailing_address` | text | high | (mailing address if different from above) |
| `clerk_change.new_noncommercial_name` | text | high | THIRD: (name of noncommercial clerk or registered agent) |
| `clerk_change.new_noncommercial_physical_address` | text | high | (physical street address, not P.O. Box - city, state and zip code) |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | SEVENTH (Foreign Entities Only): Jurisdiction of incorporation or organization |
| `entity.maine_authorization_date` | text | high | Date authorized to transact business in the State of Maine |

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of FIRST 'new' / 'modify' options is selected, populating clerk_change.action_type. (depends on `clerk_change.action_type`)
- If clerk_change.action_type = 'modify_existing', exactly one of clerk_change.modify_subtype options is selected. (depends on `clerk_change.action_type`, `clerk_change.modify_subtype`)
- If clerk_change.action_type = 'modify_existing', clerk_change.current_clerk_or_agent_name must be non-empty. (depends on `clerk_change.action_type`, `clerk_change.current_clerk_or_agent_name`)
- Either the noncommercial fields (THIRD: name + physical address) or the commercial fields (FOURTH: CRA Public Number + name) must be populated, but not both — depending on which type of clerk/RA is being appointed. (depends on `clerk_change.new_noncommercial_name`, `clerk_change.new_commercial_name`)
- If clerk_change.new_noncommercial_physical_address is set, it must not be a P.O. Box (per FOURTH parenthetical). (depends on `clerk_change.new_noncommercial_physical_address`)
- If the entity is foreign, entity.home_jurisdiction and entity.maine_authorization_date must both be populated; if domestic, both should be empty. (depends on `entity.home_jurisdiction`, `entity.maine_authorization_date`)
- filing.signer.printed_name and filing.signer.title are both non-empty (Shape A — split name/title widgets). (depends on `filing.signer.printed_name`, `filing.signer.title`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "clerk_change": {
    "action_type": "Sample Value",
    "modify_subtype": "Sample Value",
    "current_clerk_or_agent_name": "Sample Value",
    "new_noncommercial_name": "Sample Value",
    "new_noncommercial_physical_address": "Sample Value",
    "new_noncommercial_mailing_address": "Sample Value",
    "new_commercial_cra_public_number": "P99999"
  }
}
```
