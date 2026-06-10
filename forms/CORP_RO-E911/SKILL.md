# SKILL: Filling CORP_RO-E911

**Form:** Notification of Change in Address by Municipality or U.S. Postal Service  
**Entity type:** Business Corporation  
**When to use:** Notify the Maine Secretary of State that the address of a registered entity's clerk or registered agent has been administratively changed by either the local municipality (e.g., E911 street-renumbering) or the U.S. Postal Service (e.g., zip-code reassignment). The entity itself does not initiate this filing — the municipal official or postmaster does. Records the entity name, the existing clerk/RA name on record, the old address, the new physical and (optionally) mailing address, and which authority authorized the change. No filing fee. 2 pages, 24 widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `clerk_change.address_change_authorized_by` | text | high | FOURTH: This change of address was duly authorized by (choose one): [ ] Town/Municipality (fills multiple widgets) |
| `clerk_change.current_clerk_or_agent_name` | text | high | FIRST: The name of the clerk/registered agent as it appears on the record in the Secretary of State's office: |
| `clerk_change.new_mailing_address` | text | high | (mailing address if different from above) |
| `clerk_change.new_physical_address` | text | high | THIRD: The new address of the clerk/registered agent: (physical location, not P.O. Box – street, city, state and zip code) |
| `clerk_change.old_address` | text | high | SECOND: The old address of the clerk/registered agent as it appears on the record in the Secretary of State's office: (street, city, state and zip code - old address) |
| `entity.name` | text | high | (Name of Entity) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |

_Showing 12 of 22 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- clerk_change.current_clerk_or_agent_name is non-empty (must match the SOS record exactly to identify the agent). (depends on `clerk_change.current_clerk_or_agent_name`)
- clerk_change.old_address is non-empty. (depends on `clerk_change.old_address`)
- clerk_change.new_physical_address is non-empty. (depends on `clerk_change.new_physical_address`)
- clerk_change.new_physical_address must not be a P.O. Box (page-0 THIRD parenthetical 'physical location, not P.O. Box'). (depends on `clerk_change.new_physical_address`)
- clerk_change.old_address differs from clerk_change.new_physical_address (an E911 / USPS notification with identical addresses is vacuous). (depends on `clerk_change.old_address`, `clerk_change.new_physical_address`)
- Exactly one of clerk_change.address_change_authorized_by ∈ {'town_municipality', 'us_postal_service'} is selected (FOURTH 'choose one'). (depends on `clerk_change.address_change_authorized_by`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D — must be signed by the municipal official or postmaster per page-0 footnote). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "clerk_change": {
    "current_clerk_or_agent_name": "Sample Value",
    "old_address": "Sample Value",
    "new_physical_address": "Sample Value",
    "new_mailing_address": "Sample Value",
    "address_change_authorized_by": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    }
  }
}
```
