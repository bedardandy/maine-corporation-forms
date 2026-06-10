# SKILL: Filling CORP_MBCA-12A

**Form:** Amended Application for Authority to Do Business (Foreign Business Corporation)  
**Entity type:** Business Corporation  
**When to use:** Amend a foreign business corporation's authority to do business in Maine under 13-C MRSA §1504. Records the entity's current name and current home jurisdiction (FIRST recital — used to identify the existing SOS record), the date the corporation was originally authorized in Maine (SECOND recital), then captures any of: a new corporate name (THIRD; with optional fictitious name + FICT-4 attachment), a new principal-office address (FOURTH), or a new home jurisdiction (FIFTH; requires an attached certificate of existence dated within 90 days). Filing fee $76 base, $35 if amending ONLY Item FOURTH (principal-office address). 3 pages, 28 widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.home_jurisdiction` | text | high | FIFTH: The new state or country under whose law the foreign corporation is now incorporated is ___ (if no change, so indicate) |
| `entity.home_jurisdiction_name` | text | high | THIRD: The name of the foreign corporation has been changed to ___ (if no change, so indicate) |
| `entity.home_jurisdiction_name_on_record` | text | high | (Name of Corporation) |
| `entity.home_jurisdiction_on_record` | text | high | FIRST: The jurisdiction currently appearing on the record is ___ |
| `entity.maine_authorization_date` | text | high | SECOND: The date on which it was authorized to do business in the State of Maine is ___ |
| `entity.maine_fictitious_name` | text | high | If the real corporate name is not available, the fictitious name under which it proposes to apply for authority to do business in the State of Maine is ___ |
| `entity.principal_office.mailing_address` | text | high | (mailing address if different from above) |
| `entity.principal_office.physical_address` | text | high | FOURTH: The new address of its principal office, wherever located, is ___ (if no change, so indicate) (street, city, state and zip code) |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |

_Showing 12 of 27 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.home_jurisdiction_name_on_record is non-empty (top-of-form recital used to identify the existing SOS record). (depends on `entity.home_jurisdiction_name_on_record`)
- entity.home_jurisdiction_on_record is non-empty (FIRST recital). (depends on `entity.home_jurisdiction_on_record`)
- entity.maine_authorization_date is non-empty and on or before filing.date_signed (SECOND recital — Maine-side anniversary). (depends on `entity.maine_authorization_date`, `filing.date_signed`)
- At least one of entity.home_jurisdiction_name (THIRD), entity.principal_office.physical_address (FOURTH), or entity.home_jurisdiction (FIFTH) differs from its on-record counterpart, or contains a non-'no change' value (an amendment that changes nothing is vacuous). (depends on `entity.home_jurisdiction_name`, `entity.home_jurisdiction_name_on_record`, `entity.principal_office.physical_address`, `entity.home_jurisdiction`, `entity.home_jurisdiction_on_record`)
- If entity.maine_fictitious_name is set, filing.fict4_accompanies must be true. (depends on `entity.maine_fictitious_name`, `filing.fict4_accompanies`)
- If entity.home_jurisdiction differs from entity.home_jurisdiction_on_record (Item FIFTH was amended), filing.certificate_of_existence_attached must be true (Check Box2 checked). (depends on `entity.home_jurisdiction`, `entity.home_jurisdiction_on_record`, `filing.certificate_of_existence_attached`)
- Both entity.home_jurisdiction and entity.home_jurisdiction_on_record are not 'Maine' or 'ME' (foreign-corp amendments only — domestic Maine corps amend differently). (depends on `entity.home_jurisdiction`, `entity.home_jurisdiction_on_record`)
- filing.signer.printed_name and filing.signer.title are both non-empty (Shape A — name and title in separate widgets). (depends on `filing.signer.printed_name`, `filing.signer.title`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)
- filing.expedited_service is exactly one of hold_for_pickup | 24h_next_business_day | immediate_same_day. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "entity": {
    "home_jurisdiction_name_on_record": "Wabanaki Widgets, Inc.",
    "home_jurisdiction_on_record": "Sample Value",
    "maine_authorization_date": "2026-01-15",
    "home_jurisdiction_name": "Wabanaki Widgets, Inc.",
    "maine_fictitious_name": "Wabanaki Widgets, Inc.",
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
