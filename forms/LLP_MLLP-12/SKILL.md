# SKILL: Filling LLP_MLLP-12

**Form:** Application for Authority to Do Business (Foreign Limited Liability Partnership)  
**Entity type:** Limited Liability Partnership  
**When to use:** Qualify a foreign limited liability partnership to conduct activities in Maine under 31 MRSA §852.3, providing home-jurisdiction name, optional Maine assumed-name (when home name lacks the LLP suffix per §803-A) or fictitious Maine name (when home name is unavailable), Maine registered agent, contact partner, commencement date, optional professional-LLP election, and a certificate of existence (ELEVENTH paragraph). Body schema mirrors LLC_MLLC-12 (foreign-LLC authority) with LLP-specific role-name substitution (contact_partner instead of manager).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `contact_partner.additional_attached` | text | high | [ ] Names and addresses of additional contact partners are attached as Exhibit ___, and made a part hereof |
| `contact_partner_1.address` | text | high | EIGHTH: ADDRESS (contact partner row 1) |
| `contact_partner_1.name` | text | high | EIGHTH: NAME (contact partner row 1) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | FOURTH: Date of organization |
| `entity.home_jurisdiction` | text | high | FOURTH: Jurisdiction of organization |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Liability Partnership in Jurisdiction of Organization) |
| `entity.maine_activities_start_date` | text | high | NINTH: The date on which the foreign limited liability partnership first did, or intends to do, business in the State of Maine is |
| `entity.maine_assumed_name_for_suffix` | text | high | FIRST: The proposed limited liability partnership name* to be used in this State: |
| `entity.maine_business_purpose` | text | high | FIFTH: ...The nature of the business or purposes to be conducted or promoted in the State of Maine is |
| `entity.maine_fictitious_name` | text | high | SECOND: ...the fictitious name under which it proposes to apply for authority to do business in the State of Maine is |
| `entity.principal_office.mailing_address` | text | high | FOURTH: (mailing address if different from above) |

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- If entity.maine_fictitious_name is non-empty, filing.fict4_accompanies must be true (Form FICT-4 must accompany the application). (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- entity.formation_date_in_home_jurisdiction is not in the future. (depends on `entity.formation_date_in_home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is on or before entity.maine_activities_start_date (cannot start Maine activities before formation). (depends on `entity.formation_date_in_home_jurisdiction`, `entity.maine_activities_start_date`)
- entity.principal_office.physical_address is non-empty. (depends on `entity.principal_office.physical_address`)
- Exactly one of SIXTH commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be set. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address is not a P.O. Box. (depends on `registered_agent.physical_address`)
- contact_partner_1.name and contact_partner_1.address are both non-empty. (depends on `contact_partner_1.name`, `contact_partner_1.address`)
- If entity.is_professional_llp is true, at least entity.professional_services_description.line1 must be non-empty. (depends on `entity.is_professional_llp`, `entity.professional_services_description.line1`)
- Either (a) filing.signer.printed_name_and_capacity (individual path) is non-empty, or (b) filing.signer.entity_name AND filing.signer.entity_signer_printed_name_and_capacity (entity path) are both non-empty. (depends on `filing.signer.printed_name_and_capacity`, `filing.signer.entity_name`, `filing.signer.entity_signer_printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- ELEVENTH paragraph requires that an attached certificate of existence (or document of similar import) is dated within 90 days before delivery; tracked manually in filing.notes since the COE is a separate attachment, not a form field. (depends on )

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
    "fict4_accompanies": "Sample Value"
  }
}
```
