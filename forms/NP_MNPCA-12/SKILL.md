# SKILL: Filling NP_MNPCA-12

**Form:** Application for Authority to Carry on Activities (Foreign Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Qualify a foreign nonprofit corporation to carry on activities in Maine under 13-B MRSA §1202. Recites the entity's home-jurisdiction name, optional Maine fictitious name (with bundled FICT-4 indicator) when the home name is unavailable per §301-A, jurisdiction and date of incorporation, authorized purposes in the home jurisdiction, scope of activities sought in Maine (all-authorized vs. specific-subset), principal/registered office address, Maine registered agent, registered-agent §1105.2 consent recital, and certificate-of-existence attachment. Sister to CORP_MBCA-12 (foreign business corporation) but without an officer roster.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.formation_date_in_home_jurisdiction` | text | high | SECOND: ...and the date of incorporation is ___ |
| `entity.home_jurisdiction` | text | high | SECOND: Its jurisdiction of incorporation is ___ and the date of incorporation is |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation in Jurisdiction of Incorporation) |
| `entity.home_purpose_description_line1` | text | high | THIRD: Purpose(s) it is authorized to do under the laws of its jurisdiction of incorporation: ___ (line 1) |
| `entity.home_purpose_description_line2` | text | high | THIRD: ___ (line 2) |
| `entity.maine_activities_scope` | text | high | FOURTH: Does it seek authority to engage in all activities authorized in its jurisdiction and allowed by Maine Law? [X] Yes (fills multiple widgets) |
| `entity.maine_fictitious_name` | text | high | FIRST: ...the fictitious name under which it proposes to apply for authority to carry on activities in the State of Maine is ___ |
| `entity.maine_specific_activities_line1` | text | high | FOURTH: If no, specify activity (activities) for which authority is sought. ___ (inline trailing blank, line 1) |
| `entity.maine_specific_activities_line2` | text | high | FOURTH: ___ (line 2 — wide) |
| `entity.principal_office.physical_address_line1` | text | high | FIFTH: Address of the registered or principal office, wherever located, is ___ (inline trailing blank, line 1) |
| `entity.principal_office.physical_address_line2` | text | high | FIFTH: ___ (street, city, state and zip code) — wide labeled line |

_Showing 12 of 33 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty and is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true (Form FICT-4 must accompany the application when a fictitious name is used). (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- entity.formation_date_in_home_jurisdiction is not in the future. (depends on `entity.formation_date_in_home_jurisdiction`)
- filing.date_signed is on or after entity.formation_date_in_home_jurisdiction (cannot apply for Maine authority before being formed). (depends on `filing.date_signed`, `entity.formation_date_in_home_jurisdiction`)
- At least one of entity.home_purpose_description_line1 or _line2 is non-empty (THIRD recital). (depends on `entity.home_purpose_description_line1`, `entity.home_purpose_description_line2`)
- entity.maine_activities_scope is exactly one of 'all' | 'specific' (FOURTH Yes/No is mutually exclusive). (depends on `entity.maine_activities_scope`)
- If entity.maine_activities_scope='specific', at least one of entity.maine_specific_activities_line1 or _line2 must be non-empty. (depends on `entity.maine_activities_scope`, `entity.maine_specific_activities_line1`, `entity.maine_specific_activities_line2`)
- At least one of entity.principal_office.physical_address_line1 or _line2 is non-empty (FIFTH). (depends on `entity.principal_office.physical_address_line1`, `entity.principal_office.physical_address_line2`)
- Exactly one of SIXTH commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be set. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address is not a P.O. Box (per SIXTH parenthetical). (depends on `registered_agent.physical_address`)
- filing.signer.printed_name_and_capacity is non-empty (must be 'any duly authorized individual' per 13-B MRSA §104.1.B). (depends on `filing.signer.printed_name_and_capacity`)
- EIGHTH paragraph requires that an attached certificate of existence (or document of similar import) is dated no more than 90 days prior to delivery of this application; tracked manually since the COE is a separate attachment, not a form field. (depends on )

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "home_purpose_description_line1": "Sample Value",
    "home_purpose_description_line2": "Sample Value",
    "maine_activities_scope": "all"
  },
  "filing": {
    "fict4_accompanies": true
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999"
  }
}
```
