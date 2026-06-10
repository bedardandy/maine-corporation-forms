# SKILL: Filling LLC_MLLC-12

**Form:** Statement of Foreign Qualification (Foreign LLC Authority to Conduct Activities)  
**Entity type:** Limited Liability Company  
**When to use:** Qualify a foreign limited liability company to conduct activities in Maine under 31 MRSA §1622, providing home-jurisdiction info, alternate/fictitious Maine name (if needed), Maine registered agent, manager list, commencement date, optional professional/series-LLC elections, and a certificate of existence.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: Date of formation |
| `entity.home_jurisdiction` | text | high | Jurisdiction where formed |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Liability Company in Jurisdiction of Organization) |
| `entity.is_professional_llc` | checkbox | high | TENTH: [ ] This is a professional limited liability company qualified pursuant to 13 MRSA Chapter 22-A |
| `entity.is_series_llc` | checkbox | high | ELEVENTH: (Check if applicable) [ ] The foreign limited liability company is governed by an agreement that establishes ... designated series ... |
| `entity.maine_assumed_name_for_suffix` | text | high | FIRST: ...the proposed name to be used in this State in compliance with this requirement is |
| `entity.maine_business_purpose` | text | high | FIFTH: The nature of the business or purpose(s) to be conducted or promoted in the State of Maine is |
| `entity.maine_fictitious_name` | text | high | SECOND: ...the fictitious name under which it seeks authority to conduct activities in the State of Maine is |
| `entity.principal_office.mailing_address` | text | high | (mailing address if different from above) |
| `entity.principal_office.physical_address` | text | high | Address of the principal office, wherever located: (physical location - street, city, state, zip and country) |
| `entity.professional_services_description` | text | high | (type of professional services) |

_Showing 12 of 42 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- If entity.home_jurisdiction_name does not include an LLC-style suffix (per §1508.1), entity.maine_assumed_name_for_suffix must be set and must include a valid suffix. (depends on `entity.home_jurisdiction_name`, `entity.maine_assumed_name_for_suffix`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true. (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- entity.formation_date_in_home_jurisdiction is on or before entity.maine_activities_start_date. (depends on `entity.formation_date_in_home_jurisdiction`, `entity.maine_activities_start_date`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- Exactly one of SIXTH commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- registered_agent.physical_address is not a P.O. Box. (depends on `registered_agent.physical_address`)
- If manager.additional_attached is false, all manager_N entries (1-3) that are populated must have both name and address; if true, an exhibit letter must be present. (depends on `manager.additional_attached`, `manager_1.name`, `manager_1.address`, `manager_2.name`, `manager_2.address`, `manager_3.name`, `manager_3.address`)
- If entity.is_professional_llc is true, entity.professional_services_description must be non-empty. (depends on `entity.is_professional_llc`, `entity.professional_services_description`)
- If entity.is_series_llc is true, entity.series_llc_exhibit_letter must be set. (depends on `entity.is_series_llc`, `entity.series_llc_exhibit_letter`)
- TWELFTH paragraph requires that an attached certificate of existence (or equivalent) is dated within 90 days before delivery; tracked manually in filing.notes since the COE is a separate attachment, not a form field. (depends on )

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_assumed_name_for_suffix": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "home_jurisdiction": "Sample Value",
    "principal_office": {
      "physical_address": "Sample Value",
      "mailing_address": "Sample Value"
    }
  },
  "filing": {
    "fict4_accompanies": true
  },
  "registered_agent": {}
}
```
