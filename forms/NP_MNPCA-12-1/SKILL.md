# SKILL: Filling NP_MNPCA-12-1

**Form:** Application for Authority to Carry on Activities (Foreign Nonprofit Corporation, sub-form to accompany Application for Transfer of Authority)  
**Entity type:** Nonprofit Corporation  
**When to use:** Page-by-page foreign-qualification disclosure block bundled with NP_MNPCA-12 (Application for Transfer of Authority) per 13-B MRSA §1202 / §1301-A. Captures the foreign nonprofit's home-jurisdiction identity, optional fictitious Maine name, jurisdiction and date of incorporation, scope of activities, and Maine registered agent. SEVENTH (registered-agent consent per 5 MRSA §108.3) and EIGHTH (certificate-of-existence within 90 days) are declarative paragraphs without widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.formation_date_in_home_jurisdiction` | text | high | THIRD: ...and the date of incorporation is |
| `entity.home_jurisdiction` | text | high | THIRD: Its jurisdiction of incorporation is |
| `entity.home_jurisdiction_name` | text | high | FIRST: The name of the corporation is: |
| `entity.home_purpose.line1` | text | high | FOURTH: Purpose(s) it is authorized to do under the laws of its jurisdiction of incorporation: (inline blank) |
| `entity.home_purpose.line2` | text | high | FOURTH: ...continuation line below the purpose statement |
| `entity.maine_fictitious_name` | text | high | SECOND: ...the fictitious name under which it proposes to apply for authority to carry on activities in the State of Maine is: |
| `entity.maine_limited_activities.line1` | text | high | FIFTH: If no, specify activity (activities) for which authority is sought. (inline blank) |
| `entity.maine_limited_activities.line2` | text | high | FIFTH: ...continuation line below |
| `filing.fict4_accompanies` | checkbox | high | Form FICT-4 accompanies this application. |
| `filing.seeks_full_authority` | text | high | FIFTH: Does it seek authority to engage in all activities authorized in its jurisdiction and allowed by Maine Law? Yes (fills multiple widgets) |
| `registered_agent.cra_public_number` | text | high | SIXTH: CRA Public Number: |
| `registered_agent.mailing_address` | text | high | SIXTH: (mailing address if different from above) |

_Showing 12 of 15 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true. (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- entity.formation_date_in_home_jurisdiction is non-empty and parses as a date on or before today. (depends on `entity.formation_date_in_home_jurisdiction`)
- At least entity.home_purpose.line1 is non-empty. (depends on `entity.home_purpose.line1`)
- Exactly one of SIXTH commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- registered_agent.physical_address is not a P.O. Box. (depends on `registered_agent.physical_address`)
- If registered_agent.type='commercial', registered_agent.cra_public_number is non-empty. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- If filing.seeks_full_authority is false, entity.maine_limited_activities.line1 must be non-empty. (depends on `filing.seeks_full_authority`, `entity.maine_limited_activities.line1`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "home_purpose": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    }
  },
  "filing": {
    "fict4_accompanies": true,
    "seeks_full_authority": true
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999"
  }
}
```
