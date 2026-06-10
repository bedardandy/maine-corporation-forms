# SKILL: Filling CORP_CLKRA-3

**Form:** Statement of Appointment or Change of Clerk or Registered Agent  
**Entity type:** Business Corporation  
**When to use:** File a statement appointing a new clerk/registered agent or changing existing clerk/RA information (address, name) for any Maine-domestic or foreign entity (corporations, LLCs, LPs, LLPs, nonprofits). Used across all entity categories.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `clerk_change.action_type` | text | high | FIRST: [ ] A new clerk or registered agent (fills multiple widgets) |
| `clerk_change.bc_authorization` | text | high | SIXTH (DOMESTIC BUSINESS CORPORATIONS ONLY): [ ] The change ... was duly authorized by the board of directors of the corporation and the power to appoint ... is not reserved to the shareholders (fills multiple widgets) |
| `clerk_change.current_clerk_or_agent_name` | text | high | SECOND: (name of current clerk or registered agent) |
| `clerk_change.modify_subtype` | text | high | FIRST sub: [ ] Change of address (fills multiple widgets) |
| `clerk_change.new_commercial_cra_public_number` | text | high | FOURTH: The new CRA's CRA Public number is |
| `clerk_change.new_commercial_name` | text | high | (name of new CRA) |
| `clerk_change.new_noncommercial_mailing_address` | text | high | (mailing address if different from above) |
| `clerk_change.new_noncommercial_name` | text | high | THIRD: (name of noncommercial clerk or registered agent) |
| `clerk_change.new_noncommercial_physical_address` | text | high | (physical street address, not P.O. Box - city, state and zip code) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | SEVENTH (Foreign Entities Only): Jurisdiction of incorporation or organization |
| `entity.maine_authorization_date` | text | high | Date authorized to transact business in the State of Maine |

_Showing 12 of 30 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of FIRST 'new' / 'modify' options is selected. (depends on `clerk_change.action_type`)
- If clerk_change.action_type = 'modify_existing', exactly one of clerk_change.modify_subtype options is selected. (depends on `clerk_change.action_type`, `clerk_change.modify_subtype`)
- If clerk_change.action_type = 'modify_existing', clerk_change.current_clerk_or_agent_name must be non-empty. (depends on `clerk_change.action_type`, `clerk_change.current_clerk_or_agent_name`)
- Either the noncommercial fields (THIRD) or the commercial fields (FOURTH) must be populated, but not both — depending on which type of clerk/RA is being appointed. (depends on `clerk_change.new_noncommercial_name`, `clerk_change.new_commercial_name`)
- If clerk_change.new_noncommercial_physical_address is set, it must not be a P.O. Box. (depends on `clerk_change.new_noncommercial_physical_address`)
- If the entity type is Maine domestic Business Corporation, exactly one of SIXTH bc_authorization options must be selected. (Determined externally — entity-type isn't on this form.) (depends on `clerk_change.bc_authorization`)
- If the entity is foreign, entity.home_jurisdiction and entity.maine_authorization_date must both be populated; if domestic, both should be empty. (depends on `entity.home_jurisdiction`, `entity.maine_authorization_date`)
- filing.signer.title is non-empty (the form's footnote restricts who may sign per entity type). (depends on `filing.signer.title`)

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
