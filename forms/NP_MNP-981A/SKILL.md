# SKILL: Filling NP_MNP-981A

**Form:** Certificate of Organization (Domestic Nonprofit Corporation, 13 MRSA §981-A)  
**Entity type:** Nonprofit Corporation  
**When to use:** File a Certificate of Organization for an existing Maine domestic nonprofit corporation under 13 MRSA §981-A. The undersigned officers recite the corporation's original organization details (place, date, original name), historical name changes (up to 5 inline rows), original purposes, current public/mutual benefit classification, current management structure (directors vs members), current located-at address, and full officer roster. Unlike a NPCA-6 formation filing, the corporation already exists; this is a §981-A re-recital filing. Distinct from the modern NPCA-6 incorporator pattern — signers are sitting officers (President and Secretary/Clerk).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.current_address.city` | text | high | EIGHTH: ...in the town of [town] |
| `entity.current_address.county` | text | high | EIGHTH: ...County of [county] |
| `entity.current_address.street` | text | high | EIGHTH: Said corporation is now located at [street] |
| `entity.management_structure` | text | high | SEVENTH: [ ] Directors (including trustees, governors, managers, etc.), or if no Directors, (fills multiple widgets) |
| `entity.mutual_benefit_purpose` | text | high | SIXTH (mutual benefit): purpose description |
| `entity.name` | text | high | SECOND: The name of said corporation is now |
| `entity.name_history[0].date` | text | high | THIRD: row 1 — Date of Change |
| `entity.name_history[0].name` | text | high | THIRD: row 1 — New Name |
| `entity.name_history[1].date` | text | high | THIRD: row 2 — Date of Change |
| `entity.name_history[1].name` | text | high | THIRD: row 2 — New Name |
| `entity.name_history[2].date` | text | high | THIRD: row 3 — Date of Change |

_Showing 12 of 47 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty (SECOND recital). (depends on `entity.name`)
- entity.original_name is non-empty (FOURTH recital). (depends on `entity.original_name`)
- entity.original_organization_address.street and .city are both non-empty. (depends on `entity.original_organization_address.street`, `entity.original_organization_address.city`)
- entity.original_organization_date.{day,month,year} are all non-empty (FIRST recital sentence cannot be completed otherwise). (depends on `entity.original_organization_date.day`, `entity.original_organization_date.month`, `entity.original_organization_date.year`)
- entity.nonprofit_type is exactly one of 'public_benefit' or 'mutual_benefit' (SIXTH header reads '"X" one box only'). (depends on `entity.nonprofit_type`)
- If entity.nonprofit_type='public_benefit', entity.public_benefit_purpose must be non-empty. If entity.nonprofit_type='mutual_benefit' and the corporation is NOT organized for all purposes permitted under 13-B, entity.mutual_benefit_purpose must be non-empty (otherwise it may be empty). (depends on `entity.nonprofit_type`, `entity.public_benefit_purpose`, `entity.mutual_benefit_purpose`)
- entity.management_structure is exactly one of 'directors' or 'members' (SEVENTH header reads '"X" one box only'). (depends on `entity.management_structure`)
- entity.current_address.{street,city,county} are all non-empty (EIGHTH recital). (depends on `entity.current_address.street`, `entity.current_address.city`, `entity.current_address.county`)
- entity.officer_count equals the number of populated officer_<role>.name slots among {president, vice_president, secretary, treasurer}. (depends on `entity.officer_count`, `officer_president.name`, `officer_vice_president.name`, `officer_secretary.name`, `officer_treasurer.name`)
- officer_president.name and officer_secretary.name are non-empty at minimum (these are also the two signers of the filing per the page-2 signature block). (depends on `officer_president.name`, `officer_secretary.name`)
- filing.signer_president.printed_name and filing.signer_secretary.printed_name are both non-empty. (depends on `filing.signer_president.printed_name`, `filing.signer_secretary.printed_name`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- For every populated entity.name_history[N].name there is a corresponding non-empty entity.name_history[N].date (and vice versa). (depends on `entity.name_history`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- At most one of the three expedite checkboxes is selected (or zero, defaulting to standard processing). (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "original_organization_address": {
      "street": "Sample Value",
      "city": "Sample Value"
    },
    "original_organization_date": {
      "day": "Sample Value",
      "month": "Sample Value",
      "year": "Sample Value"
    },
    "name": "Wabanaki Widgets, Inc.",
    "name_history": [
      {
        "name": "Wabanaki Widgets, Inc.",
        "date": "2026-01-15"
      }
    ]
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
