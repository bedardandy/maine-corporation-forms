# SKILL: Filling LLC_MLLC-9

**Form:** Certificate of Amendment (Maine Limited Liability Company)  
**Entity type:** Limited Liability Company  
**When to use:** Amend the certificate of formation of a Maine domestic limited liability company under 31 MRSA §1532 (Filing fee $50). Captures the LLC's current legal name (top), an optional new name (FIRST), the date of the original certificate of formation (SECOND), low-profit LLC designation (THIRD per 31 MRSA §1611), professional LLC designation with services description (FOURTH per 13 MRSA Chapter 22-A), an optional registered-agent change (FIFTH/SIXTH — commercial XOR noncommercial; 'Complete only if there is a change to the registered agent information'), and other amendments via exhibit (SEVENTH). Page 2 has a dual-signer block ('Authorized person(s)') — per **31 MRSA §1676.1, the certificate must be signed by a person authorized by the LLC; the form provides 2 inline slots so either one or two authorized persons may sign. Page 3 carries the standard cover-letter primitive.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.new_name` | text | high | FIRST: The name of the limited liability company has been changed to (if no change, so indicate) |
| `amendment.other_changes_exhibit_letter` | text | high | SEVENTH: Other changes …are set forth in Exhibit ____ attached and made a part hereof. |
| `authorized_person_1.printed_name_and_capacity` | text | high | **Authorized person(s) — (Type or print name and capacity) [signer slot 1] |
| `authorized_person_2.printed_name_and_capacity` | text | high | **Authorized person(s) — (Type or print name and capacity) [signer slot 2] |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.initial_filing_date` | text | high | SECOND: The date of filing of the initial certificate of formation: |
| `entity.is_low_profit_llc` | checkbox | high | THIRD: Designation as a low profit LLC — This is a low-profit limited liability company pursuant to 31 MRSA §1611 |
| `entity.is_professional_llc` | checkbox | high | FOURTH: Designation as a professional limited liability company — This is a professional limited liability company* formed pursuant to 13 MRSA Chapter 22-A |
| `entity.name` | text | high | (Name of Limited Liability Company) |
| `entity.professional_services_description.line1` | text | high | FOURTH: (type of professional services) line 1 |
| `entity.professional_services_description.line2` | text | high | FOURTH: (type of professional services) line 2 |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |

_Showing 12 of 30 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- If amendment.new_name is set and is not literally 'no change', it must contain a valid LLC suffix per 31 MRSA §1508 (e.g., 'L.L.C.', 'LLC', 'Limited Liability Company', 'L.C.'). (depends on `amendment.new_name`)
- entity.initial_filing_date is non-empty and is on or before filing.date_signed (initial filing must precede the amendment). (depends on `entity.initial_filing_date`, `filing.date_signed`)
- If entity.is_professional_llc is true, at least entity.professional_services_description.line1 must be non-empty (FOURTH). (depends on `entity.is_professional_llc`, `entity.professional_services_description.line1`)
- If any FIFTH widget is populated (registered_agent.name / .physical_address / .cra_public_number), exactly one of registered_agent.type values must be selected (commercial XOR noncommercial). FIFTH is optional — when not populated, no agent change is being made. (depends on `registered_agent.type`, `registered_agent.name`, `registered_agent.physical_address`, `registered_agent.cra_public_number`)
- If registered_agent.type = 'commercial', registered_agent.cra_public_number must be non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- If registered_agent.physical_address is non-empty, it must not be a P.O. Box. (depends on `registered_agent.physical_address`)
- At least authorized_person_1.printed_name_and_capacity is non-empty (per 31 MRSA §1676.1, the certificate must be signed by a person authorized by the LLC). (depends on `authorized_person_1.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (cover-letter primitive). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.entities[0].name is non-empty (cover-letter primitive). (depends on `filing.entities[0].name`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC",
    "initial_filing_date": "2026-01-15",
    "is_low_profit_llc": true,
    "is_professional_llc": true,
    "professional_services_description": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    }
  },
  "amendment": {
    "new_name": "Sample Value"
  },
  "registered_agent": {
    "type": "Sample Value"
  },
  "authorized_person_1": {},
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
