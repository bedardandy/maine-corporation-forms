# SKILL: Filling LLC_MLLC-6

**Form:** Certificate of Formation (LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Form a Maine domestic limited liability company under 31 MRSA §1531, including LLC name, effective date, optional low-profit (L3C) or professional designations, registered-agent designation, and an optional initial statement of authority.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_effective_date` | text | high | Later effective date (specified here): ___ |
| `entity.formation_effective_date_choice` | text | high | SECOND: [ ] Date of this filing (fills multiple widgets) |
| `entity.is_low_profit_llc` | checkbox | high | THIRD: [ ] This is a low-profit limited liability company pursuant to 31 MRSA §1611 |
| `entity.is_professional_llc` | checkbox | high | FOURTH: [ ] This is a professional limited liability company* formed pursuant to 13 MRSA Chapter 22-A |
| `entity.name` | text | high | FIRST: The name of the limited liability company is |
| `entity.professional_services_description` | text | high | (Type of professional services) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |

_Showing 12 of 28 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name ends with one of the statutory suffixes: 'Limited Liability Company', 'Limited Company', 'L.L.C.', 'LLC', 'L.C.', 'LC', or (if low-profit) 'L3C' or 'l3c' (case-insensitive substring match per 31 MRSA §1508). (depends on `entity.name`, `entity.is_low_profit_llc`)
- Exactly one of the SECOND options is selected. (depends on `entity.formation_effective_date_choice`)
- If entity.formation_effective_date_choice = 'later_specified', entity.formation_effective_date must be set and on or after filing.date_signed. (depends on `entity.formation_effective_date_choice`, `entity.formation_effective_date`, `filing.date_signed`)
- If entity.is_professional_llc is true, entity.professional_services_description must be non-empty. (depends on `entity.is_professional_llc`, `entity.professional_services_description`)
- Exactly one of FIFTH commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type = 'commercial', registered_agent.cra_public_number must be set; if 'noncommercial', it must be absent. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.name is non-empty (regardless of type). (depends on `registered_agent.name`)
- registered_agent.physical_address must not be a P.O. Box. (depends on `registered_agent.physical_address`)
- entity.is_low_profit_llc and entity.is_professional_llc cannot both be true. (depends on `entity.is_low_profit_llc`, `entity.is_professional_llc`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "formation_effective_date_choice": "2026-01-15",
    "formation_effective_date": "2026-01-15",
    "is_low_profit_llc": true,
    "is_professional_llc": true,
    "professional_services_description": "Sample Value"
  },
  "registered_agent": {
    "type": "Sample Value",
    "cra_public_number": "P99999"
  }
}
```
