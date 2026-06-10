# SKILL: Filling LLC_MLLC-12B

**Form:** Statement of Cancellation of Foreign Qualification (Foreign LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Cancel a foreign limited liability company's authority to conduct activities in Maine under 31 MRSA §1665.7 (with §1662 SOS-as-agent appointment when no registered agent is maintained). Recites the entity's home name, fictitious Maine name (if any), home jurisdiction and date of organization, and date of original Maine qualification, then provides a post-cancellation service-of-process mailing address (FIFTH) and the entity's current principal office address (SIXTH). FOURTH and SEVENTH are declarative-only paragraphs with no widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.formation_date_in_home_jurisdiction` | text | high | SECOND: ...and the date of organization is ___ |
| `entity.home_jurisdiction` | text | high | SECOND: Its jurisdiction of organization is ___ (state or country) |
| `entity.home_jurisdiction_name` | text | high | (Name of Limited Liability Company in Jurisdiction of Organization) |
| `entity.maine_authorization_date` | text | high | THIRD: The date on which the foreign limited liability company was qualified to conduct activities in the State of Maine: |
| `entity.maine_fictitious_name` | text | high | FIRST: If different, the fictitious name under which the foreign limited liability company adopted to do business in the State of Maine pursuant to §1510-1.B is: |
| `entity.post_cancellation_service_address.line1` | text | high | FIFTH: ...the mailing address to which service of process may be mailed pursuant to §1662 is: (Principal office address) [line 1] |
| `entity.post_cancellation_service_address.line2` | text | high | FIFTH: (Principal office address) [line 2] |
| `entity.principal_office.physical_address` | text | high | SIXTH: The street and mailing address of the foreign limited liability company's principal office is: ___ (street, city, state and zip code) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |

_Showing 12 of 24 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty. (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is not 'Maine' or 'ME' (this form is foreign-only). (depends on `entity.home_jurisdiction`)
- If entity.maine_fictitious_name is non-empty, it differs from entity.home_jurisdiction_name (case-insensitive). (depends on `entity.maine_fictitious_name`, `entity.home_jurisdiction_name`)
- entity.formation_date_in_home_jurisdiction is on or before entity.maine_authorization_date (a foreign LLC must exist in its home jurisdiction before it can qualify in Maine). (depends on `entity.formation_date_in_home_jurisdiction`, `entity.maine_authorization_date`)
- entity.maine_authorization_date is not in the future and is on or before filing.date_signed. (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- entity.principal_office.physical_address is non-empty (SIXTH is unconditional). (depends on `entity.principal_office.physical_address`)
- If the entity is not maintaining a registered agent in Maine, entity.post_cancellation_service_address.line1 must be non-empty (FIFTH applies). At least line1 is required when FIFTH applies; line2 is optional. (depends on `entity.post_cancellation_service_address.line1`, `entity.post_cancellation_service_address.line2`)
- filing.signer.printed_name_and_capacity is non-empty (signer must be a person authorized by the LLC per 31 MRSA §1676.1.B). (depends on `filing.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- At most one of the three expedite checkboxes is selected. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "formation_date_in_home_jurisdiction": "2026-01-15",
    "maine_authorization_date": "2026-01-15",
    "post_cancellation_service_address": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "principal_office": {
      "physical_address": "Sample Value"
    }
  }
}
```
