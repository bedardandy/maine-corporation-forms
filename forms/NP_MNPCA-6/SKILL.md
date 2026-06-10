# SKILL: Filling NP_MNPCA-6

**Form:** Articles of Incorporation (Nonprofit)  
**Entity type:** Nonprofit Corporation  
**When to use:** Form a Maine domestic nonprofit corporation under 13-B MRSA §403, designating public-benefit vs mutual-benefit purpose, registered agent, board structure, member structure, optional 501(c) provisions, and incorporator signatures (individual or corporate).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.501c_exhibit_letter` | text | high | EIGHTH: ...are set out in Exhibit ___ attached hereto and made a part hereof |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.directors_max_count` | text | high | and the maximum number of directors shall be ___ |
| `entity.directors_min_count` | text | high | FIFTH: The minimum number of directors (not less than 3) shall be ___ |
| `entity.initial_directors_count` | text | high | FIFTH: ...the initial board of directors of the corporation, if the number has been determined ... is ___ |
| `entity.mutual_benefit_purpose` | text | high | (mutual benefit purposes description) |
| `entity.name` | text | high | FIRST: The name of the corporation is |
| `entity.public_benefit_purpose` | text | high | (public benefit purposes description) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

_Showing 12 of 48 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of SECOND public_benefit/mutual_benefit options is selected. (depends on `entity.nonprofit_type`)
- If nonprofit_type = 'public_benefit', entity.public_benefit_purpose must be non-empty. If nonprofit_type = 'mutual_benefit' AND not 'all purposes permitted', entity.mutual_benefit_purpose must be non-empty. (depends on `entity.nonprofit_type`, `entity.public_benefit_purpose`, `entity.mutual_benefit_purpose`)
- Exactly one of THIRD commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If entity.initial_directors_count is set, it must be ≥3. If min/max are set, both must be ≥3 and min ≤ max. (depends on `entity.initial_directors_count`, `entity.directors_min_count`, `entity.directors_max_count`)
- Exactly one of SIXTH no-members/has-members options is selected. (depends on `entity.has_members`)
- If entity.has_501c_exhibit is true, entity.501c_exhibit_letter must be set. (depends on `entity.has_501c_exhibit`, `entity.501c_exhibit_letter`)
- At least one of incorporator_1, incorporator_2, incorporator_3, incorporator_entity_1, or incorporator_entity_2 is fully populated. (depends on `incorporator_1.printed_name`, `incorporator_entity_1.name`)
- If any incorporator_entity_N is set, the filing must be accompanied by an officer's certificate confirming signing authority (per 13-B MRSA §401 footnote on page 3 of the form). (depends on `incorporator_entity_1.name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "nonprofit_type": "Sample Value",
    "public_benefit_purpose": "Sample Value",
    "mutual_benefit_purpose": "Sample Value"
  },
  "registered_agent": {
    "type": "Sample Value",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value"
  }
}
```
