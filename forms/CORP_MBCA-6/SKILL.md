# SKILL: Filling CORP_MBCA-6

**Form:** Articles of Incorporation  
**Entity type:** Business Corporation  
**When to use:** Form articles of incorporation to create a Maine domestic business corporation under 13-C MRSA, including clerk designation, share structure, board structure, optional liability/indemnification provisions, and incorporator signature.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `clerk.cra_public_number` | text | high | FOURTH: Commercial Clerk — CRA Public Number |
| `clerk.mailing_address` | text | high | (mailing address if different from above) |
| `clerk.physical_address` | text | high | (physical location, not P.O. Box - street, city, state and zip code) |
| `entity.additional_incorporators_exhibit_letter` | text | high | ELEVENTH: ...set forth on Exhibit __ attached hereto |
| `entity.additional_provisions_exhibit_letter` | text | high | Exhibit __ attached hereto and made a part hereof (TENTH) |
| `entity.additional_provisions_present` | checkbox | high | TENTH: [X] Additional provisions of these Articles of Incorporation are set forth in Exhibit __ |
| `entity.annual_report_reminder_email` | text | high | (Email address to use for annual report reminders) |
| `entity.authorized_shares_total` | text | high | SIXTH: There shall only be one class of shares. The number of authorized shares is ___ |
| `entity.director_liability_limited` | checkbox | high | EIGHTH: [X] To the fullest extent permitted by 13-C MRSA §202.2.D, a director shall have no liability |
| `entity.directors_count_limited` | checkbox | high | EIGHTH: [X] The number of directors is limited as follows |
| `entity.directors_max_count` | text | high | nor more than __ directors |
| `entity.directors_min_count` | text | high | not fewer than __ nor more than |

_Showing 12 of 36 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty and matches the printed name on the form. (depends on `entity.name`)
- If entity.is_professional_corporation is true, entity.professional_services_description must be non-empty; if false, the description must be empty. (depends on `entity.is_professional_corporation`, `entity.professional_services_description`)
- If clerk.type = 'commercial', clerk.cra_public_number must be present; if 'noncommercial', it must be absent. (depends on `clerk.type`, `clerk.cra_public_number`)
- clerk.physical_address must not begin with 'P.O.', 'PO Box', or 'Post Office Box' (form explicitly forbids P.O. Box for physical location). (depends on `clerk.physical_address`)
- Exactly one of the SIXTH options is selected (single_class XOR multi_class). (depends on `entity.share_structure`)
- If entity.share_structure = 'single_class', entity.authorized_shares_total must be a positive integer. (depends on `entity.share_structure`, `entity.authorized_shares_total`)
- If entity.share_structure = 'multi_class', entity.multi_class_exhibit_letter must be set. (depends on `entity.share_structure`, `entity.multi_class_exhibit_letter`)
- Exactly one of the SEVENTH options is selected (board XOR no-board). (depends on `entity.has_board_of_directors`)
- If entity.directors_count_limited is true, entity.directors_min_count <= entity.directors_max_count and both are positive integers. (depends on `entity.directors_count_limited`, `entity.directors_min_count`, `entity.directors_max_count`)
- If entity.additional_provisions_present is true, entity.additional_provisions_exhibit_letter must be set. (depends on `entity.additional_provisions_present`, `entity.additional_provisions_exhibit_letter`)
- When any expedited option requires a return copy, all attested_copy_recipient address fields (name, mailing_address.*) are populated. (depends on `filing.attested_copy_recipient.name`, `filing.attested_copy_recipient.mailing_address.street`, `filing.attested_copy_recipient.mailing_address.city_state_zip`)
- filing.date_signed is not in the future relative to the submission date. (depends on `filing.date_signed`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "is_professional_corporation": true,
    "professional_services_description": "Sample Value",
    "is_close_corporation": true
  },
  "clerk": {
    "cra_public_number": "P99999",
    "name": "Sample Value",
    "physical_address": "Sample Value",
    "mailing_address": "Sample Value"
  }
}
```
