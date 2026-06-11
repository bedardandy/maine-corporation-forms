# SKILL: Filling CORP_MBCA-12

**Form:** Application for Authority to do Business (Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Qualify a foreign business corporation to transact business in Maine under 13-C MRSA Chapter 15, providing home-jurisdiction name, optional fictitious-name election (when home name fails §401 / Chapter 22-A §736), Maine registered agent, jurisdiction and date of incorporation, principal-office address, list of current directors and officers, and a certificate of existence dated within 90 days of filing.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | FIFTH: ...and the date of incorporation is |
| `entity.home_jurisdiction` | text | high | FIFTH: Its jurisdiction of incorporation is ___ (state or country) |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation in Jurisdiction of Incorporation) |
| `entity.is_professional_corporation` | checkbox | high | (Check box only if applicable.) This is a professional corporation pursuant to 13 MRSA Chapter 22-A** |
| `entity.maine_fictitious_name` | text | high | FIRST: ...a fictitious name under which it proposes to apply for authority to do business in the State of Maine is |
| `entity.principal_office.mailing_address` | text | high | (mailing address if different from above) |
| `entity.principal_office.physical_address` | text | high | SIXTH: Address of the principal office, wherever located, is: ___ (street, city, state and zip code) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |

_Showing 12 of 37 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (foreign-qualification implies a non-Maine home). (depends on `entity.home_jurisdiction`)
- Exactly one of SECOND commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type='commercial', registered_agent.cra_public_number must be set. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- entity.formation_date_in_home_jurisdiction is not in the future. (depends on `entity.formation_date_in_home_jurisdiction`)
- filing.date_signed is on or after entity.formation_date_in_home_jurisdiction (cannot apply for Maine authority before being formed). (depends on `filing.date_signed`, `entity.formation_date_in_home_jurisdiction`)
- entity.principal_office.physical_address is non-empty. (depends on `entity.principal_office.physical_address`)
- At least one officer_N row is fully populated (printed_name_and_capacity + address.street + address.city_state_zip). (depends on `officer_1.printed_name_and_capacity`, `officer_1.address.street`, `officer_1.address.city_state_zip`)
- If entity.is_professional_corporation is true, entity.home_jurisdiction_name (or maine_fictitious_name when set) must contain one of: 'chartered', 'professional corporation', 'professional association', 'service corporation', 'P.C.', 'P.A.', or 'S.C.' (per page 2 footnote). (depends on `entity.is_professional_corporation`, `entity.home_jurisdiction_name`, `entity.maine_fictitious_name`)
- filing.signer.printed_name_and_capacity is non-empty (signer must be an officer per 13-C MRSA §1121.5; cannot be auto-validated from form alone). (depends on `filing.signer.printed_name_and_capacity`)
- EIGHTH paragraph requires that an attached certificate of existence (or document of similar import) is dated within 90 days before delivery; tracked manually in filing.notes since the COE is a separate attachment, not a form field. (depends on )

## Example case data

```json
{
  "entity": {
    "is_professional_corporation": true,
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc."
  },
  "registered_agent": {
    "type": "commercial",
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value",
    "mailing_address": "Sample Value"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
