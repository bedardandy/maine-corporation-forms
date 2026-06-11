# SKILL: Filling LLP_MLLP-12-1

**Form:** Application for Authority to do Business (Foreign Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Qualify a foreign Limited Liability Partnership (LLP) to transact business in Maine under 31 MRSA §852.3 (the '-1' variant of MLLP-12, which carries the body but does NOT include the standard signature block or cover letter — those are bundled when this form accompanies a primary filing). Captures home-jurisdiction name, optional professional-LLP election with services description, fictitious Maine name (with FICT-4 bundle indicator), home-jurisdiction date and place of organization, principal-office address, nature of Maine business, registered-agent appointment (commercial vs noncommercial), contact partner, and Maine-activities commencement date.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `contact_partner.address` | text | high | NINTH: ADDRESS (contact partner) |
| `contact_partner.name` | text | high | NINTH: NAME (contact partner) |
| `entity.formation_date_in_home_jurisdiction` | text | high | FIFTH: Date of organization |
| `entity.home_jurisdiction` | text | high | FIFTH: Jurisdiction of organization |
| `entity.home_jurisdiction_name` | text | high | FIRST: The name of the limited liability partnership* (in its home jurisdiction) |
| `entity.is_professional_llp` | checkbox | high | SECOND: (Check box only if applicable) This is a professional limited liability partnership** qualified pursuant to 13 MRSA Chapter 22-A |
| `entity.maine_activities_start_date` | text | high | TENTH: The date on which the foreign limited liability partnership first did, or intends to do, business in the State of Maine is |
| `entity.maine_business_purpose` | text | high | SIXTH: The nature of the business or purposes to be conducted or promoted in the State of Maine is |
| `entity.maine_fictitious_name` | text | high | THIRD: …the fictitious name under which it proposes to apply for authority to do business in the State of Maine is |
| `entity.principal_office.mailing_address` | text | high | (mailing address if different from above) [principal office] |
| `entity.principal_office.physical_address` | text | high | FIFTH: Address of the registered or principal office, wherever located, is: (physical location - street (not P.O. Box), city, state and zip code) |
| `entity.professional_services_description` | checkbox | high | SECOND: (used only when checkbox 18 is set) provide the following professional services: |

_Showing 12 of 19 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and not 'Maine'/'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- If entity.is_professional_llp is true, entity.professional_services_description must be non-empty AND entity.professional_partners_licensed_statement should be non-empty. (depends on `entity.is_professional_llp`, `entity.professional_services_description`, `entity.professional_partners_licensed_statement`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true (a fictitious-name election requires a bundled FICT-4). (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- entity.formation_date_in_home_jurisdiction is on or before today. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is on or before entity.maine_activities_start_date (cannot conduct Maine activities before existing). (depends on `entity.formation_date_in_home_jurisdiction`, `entity.maine_activities_start_date`)
- entity.principal_office.physical_address is non-empty. (depends on `entity.principal_office.physical_address`)
- Exactly one of SEVENTH commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number is non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- If registered_agent.type='noncommercial', registered_agent.physical_address is non-empty and not a P.O. Box. (depends on `registered_agent.type`, `registered_agent.physical_address`)
- contact_partner.name and contact_partner.address are non-empty. (depends on `contact_partner.name`, `contact_partner.address`)
- entity.maine_business_purpose is non-empty. (depends on `entity.maine_business_purpose`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "is_professional_llp": true,
    "professional_services_description": "Sample Value",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "professional_partners_licensed_statement": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "home_jurisdiction": "Sample Value"
  },
  "filing": {
    "fict4_accompanies": "Sample Value"
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999"
  }
}
```
