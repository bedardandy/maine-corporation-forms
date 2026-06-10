# SKILL: Filling NP_MNPCA-12A

**Form:** Amended Application for Authority to Carry on Activities (Foreign Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Amend an existing foreign nonprofit corporation's authority to carry on activities in Maine under 13-B MRSA §1207. Captures the home-jurisdiction name, original Maine authorization date, the proposed amendment text, optional name-change information (new home-jurisdiction name + date + fictitious-name election), updated activities/business purpose, and updated principal-office and Maine-registered-office addresses. Signed by any duly authorized individual.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.description` | text | high | THIRD: The proposed amendment to its application of authority is ___ (line 1 inline) (fills multiple widgets) |
| `entity.annual_report_reminder_email` | text | high | Email address to use for annual report reminders |
| `entity.home_jurisdiction` | text | high | FIRST: The jurisdiction of its incorporation is |
| `entity.home_jurisdiction_name` | text | high | (Name of Corporation) |
| `entity.home_jurisdiction_name_new` | text | high | FOURTH: The corporate name of the corporation has been changed to (If no change, so indicate.) ___ (line 1 inline) (fills multiple widgets) |
| `entity.maine_authorization_date` | text | high | SECOND: The date on which it was authorized to carry on activities in the State of Maine is |
| `entity.maine_business_purpose` | text | high | SIXTH: The activity (activities) which it seeks to pursue in the State of Maine is (are) authorized by the laws of its jurisdiction of incorporation and consist(s) of (If no change, so indicate.) ___ (line 1 inline) (fills multiple widgets) |
| `entity.maine_fictitious_name` | text | high | FIFTH: If the real corporate name is not available, the fictitious name under which it proposes to apply for authority to carry on activities in the State of Maine is (If not applicable, so indicate.) ___ (full-width continuation) |
| `entity.name_change_date_in_home_jurisdiction` | text | high | FOURTH: incorporation on ___ (date) |
| `entity.principal_office.physical_address` | text | high | SEVENTH: The new address of its registered or principal office, wherever located, is (If no change, so indicate.) ___ (full-width line, with '(street, city, state and zip code)' caption) |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |

_Showing 12 of 27 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name is non-empty (the corporation's existing name in its home jurisdiction). (depends on `entity.home_jurisdiction_name`)
- entity.home_jurisdiction is non-empty (FIRST). (depends on `entity.home_jurisdiction`)
- entity.maine_authorization_date is non-empty — the original Maine authorization must exist in order to amend it (SECOND). (depends on `entity.maine_authorization_date`)
- amendment.description is non-empty (THIRD). (depends on `amendment.description`)
- If entity.home_jurisdiction_name_new is set, entity.name_change_date_in_home_jurisdiction must also be set (FOURTH pairs the new name with its effective date). (depends on `entity.home_jurisdiction_name_new`, `entity.name_change_date_in_home_jurisdiction`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true (FIFTH requires accompanying FICT-4 when a fictitious name is elected). (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- entity.maine_business_purpose is non-empty (SIXTH; or 'no change, so indicate' is permitted text). (depends on `entity.maine_business_purpose`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "home_jurisdiction": "Sample Value",
    "maine_authorization_date": "2026-01-15",
    "home_jurisdiction_name_new": "Wabanaki Widgets, Inc.",
    "name_change_date_in_home_jurisdiction": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc."
  },
  "amendment": {
    "description": "Sample Value"
  },
  "filing": {
    "fict4_accompanies": true
  }
}
```
