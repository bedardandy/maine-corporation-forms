# SKILL: Filling LLC_MLLC-12A

**Form:** Statement of Change of Foreign Qualification  
**Entity type:** Limited Liability Company  
**When to use:** Update the Secretary of State's records for a foreign limited liability company already authorized in Maine, per 31 MRSA §1622.3 / §1632. Captures changes to the entity's home-jurisdiction name (FIRST), Maine fictitious name (SECOND), original Maine qualification date (THIRD, recital-only), nature of business (FOURTH), principal-office address (FIFTH), registered agent (SIXTH), home jurisdiction (EIGHTH), and any other changes via an attached exhibit (NINTH). A certificate of existence (or equivalent), dated within 90 days of delivery, must accompany the filing. 3 pages, 33 widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | EIGHTH: The new state or other jurisdiction under whose law the foreign limited liability company is now formed |
| `entity.home_jurisdiction_name` | text | high | (Name of the Foreign Limited Liability Company in the Jurisdiction of Organization) |
| `entity.maine_authorization_date` | text | high | THIRD: The date on which the foreign limited liability company was qualified to conduct activities in the State of Maine: |
| `entity.maine_business_purpose` | text | high | FOURTH: The nature of the business or purpose(s) to be conducted or promoted in the State of Maine is |
| `entity.maine_fictitious_name` | text | high | SECOND: ...the fictitious name under which it seeks authority to conduct activities in the State of Maine is |
| `entity.principal_office.mailing_address` | text | high | (mailing address if different from above) |
| `entity.principal_office.physical_address` | text | high | FIFTH: The new address of the principal office, wherever located, is: (physical location - street (not P.O. Box), city, state and zip code) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |

_Showing 12 of 32 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty (header recital identifying the foreign LLC by its home-jurisdiction name). (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true (per MLLC-12 convention). (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- Exactly one of SIXTH commercial/noncommercial options is selected (when the registered agent is changing). (depends on `registered_agent.type`)
- If registered_agent.type is 'commercial', registered_agent.cra_public_number must be present. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- registered_agent.physical_address must not be a P.O. Box. (depends on `registered_agent.physical_address`)
- entity.maine_authorization_date is non-empty (THIRD recital is required regardless of which fields are changing — SOS uses it to locate the existing record). (depends on `entity.maine_authorization_date`)
- entity.maine_authorization_date is on or before filing.date_signed (a Statement of Change cannot pre-date the original qualification). (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- filing.signer.printed_name is non-empty (Shape B — name only, no title field). (depends on `filing.signer.printed_name`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.expedited_service is exactly one of hold_for_pickup | 24h_next_business_day | immediate_same_day. (depends on `filing.expedited_service`)
- A certificate of existence (or equivalent) must accompany the filing and must be dated within 90 days of delivery (page-1 SEVENTH recital). Tracked as an attachment, not a form field — rubric flags via filing.notes if the synth scenario does not include it. (depends on )

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_assumed_name_for_suffix": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "maine_authorization_date": "2026-01-15",
    "maine_business_purpose": "Sample Value",
    "principal_office": {
      "physical_address": "Sample Value",
      "mailing_address": "Sample Value"
    }
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
