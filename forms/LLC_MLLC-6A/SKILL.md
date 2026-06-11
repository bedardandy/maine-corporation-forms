# SKILL: Filling LLC_MLLC-6A

**Form:** Restated Certificate of Formation (Maine LLC)  
**Entity type:** Limited Liability Company  
**When to use:** File a Restated Certificate of Formation for an existing Maine LLC under 31 MRSA §1532, integrating prior amendments (and optional new amendments) into a single restated document. Records the LLC's current SOS-record name, the post-restatement name (or 'no change'), the original certificate-of-formation date, optional low-profit (L3C) and professional-LLC designations, the registered-agent block, an optional restatement-amendments exhibit, and per-officer signatures by up to three authorized persons.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `authorized_person_1.printed_name_and_capacity` | text | high | (type or print name and capacity) [signer slot 1, paired with first signature line] |
| `authorized_person_2.printed_name_and_capacity` | text | high | (type or print name and capacity) [signer slot 2] |
| `authorized_person_3.printed_name_and_capacity` | text | high | (type or print name and capacity) [signer slot 3] |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.initial_formation_date` | text | high | SECOND: The date of filing of the initial certificate of formation: ___ |
| `entity.is_low_profit_llc` | checkbox | high | THIRD: Designation as a low profit LLC (Check only if applicable): This is a low-profit limited liability company pursuant to 31 MRSA §1611... |
| `entity.is_professional_llc` | checkbox | high | FOURTH: Designation as a professional limited liability company (Check only if applicable): This is a professional limited liability company* formed pursuant to 13 MRSA Chapter 22-A... |
| `entity.name` | text | high | (Name of Limited Liability Company as it appears on the record of the Secretary of State) (fills multiple widgets) |
| `entity.professional_services_description` | text | high | (Type of professional services) |
| `entity.restatement_amendments_exhibit_letter` | text | high | SEVENTH: Other matters the members determine to include are set forth in the attached Exhibit ___, and made a part hereof. |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |

_Showing 12 of 29 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty (the LLC's current SOS-record name; for synth fills the same value goes into both 'name' and 'new name' widgets unless a name change is being effected). (depends on `entity.name`)
- entity.name ends with one of the statutory LLC suffixes: 'Limited Liability Company', 'Limited Company', 'L.L.C.', 'LLC', 'L.C.', 'LC', or (if low-profit) 'L3C'/'l3c' (case-insensitive substring match per 31 MRSA §1508). (depends on `entity.name`, `entity.is_low_profit_llc`)
- entity.initial_formation_date is non-empty (SECOND requires the original formation date to identify the LLC being restated). (depends on `entity.initial_formation_date`)
- If entity.is_professional_llc is true, entity.professional_services_description must be non-empty; if false, the description must be empty. (depends on `entity.is_professional_llc`, `entity.professional_services_description`)
- entity.is_low_profit_llc and entity.is_professional_llc cannot both be true. (depends on `entity.is_low_profit_llc`, `entity.is_professional_llc`)
- Exactly one of FIFTH commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type = 'commercial', registered_agent.cra_public_number must be set; if 'noncommercial', it must be absent. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.name is non-empty (regardless of type; one of 'agent' or 'noncommercial agent' must be filled). (depends on `registered_agent.name`)
- registered_agent.physical_address must not begin with 'P.O.', 'PO Box', or 'Post Office Box' (form explicitly forbids P.O. Box). (depends on `registered_agent.physical_address`)
- At least one of authorized_person_{1,2,3}.printed_name_and_capacity is non-empty. (depends on `authorized_person_1.printed_name_and_capacity`, `authorized_person_2.printed_name_and_capacity`, `authorized_person_3.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future relative to the submission date. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are non-empty (per cover-letter NOTE). (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, LLC",
    "initial_formation_date": "2026-01-15",
    "is_low_profit_llc": true,
    "is_professional_llc": true,
    "professional_services_description": "Sample Value"
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999",
    "name": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
