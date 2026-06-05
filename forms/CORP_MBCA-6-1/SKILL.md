# SKILL: Filling CORP_MBCA-6-1

**Form:** Articles of Incorporation (to accompany other filings)  
**Entity type:** Business Corporation  
**When to use:** Articles of Incorporation form designed to ACCOMPANY one of six other principal corporate filings (domestication, domestication+conversion, entity conversion, merger or share exchange, partnership conversion, or restated articles). Captures the kind of accompanying filing (mutually-exclusive enum at top of page 0), entity name, optional professional/benefit corporation elections, clerk designation, share structure, board structure, and optional liability/indemnification provisions. Filed under 13-C MRSA §202.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `clerk.cra_public_number` | text | high | SECOND: [ ] Commercial Clerk    CRA Public Number: ___ |
| `clerk.mailing_address` | text | high | (mailing address if different from above) |
| `clerk.name` | text | high | (name of commercial clerk) (fills multiple widgets) |
| `clerk.physical_address` | text | high | (physical location, not P.O. Box – street, city, state and zip code) |
| `clerk.type` | text | high | SECOND: [ ] Commercial Clerk (fills multiple widgets) |
| `entity.additional_provisions_exhibit_letter` | text | high | EIGHTH: ...set forth in Exhibit ___ attached hereto |
| `entity.additional_provisions_present` | checkbox | high | EIGHTH: (Check only if applicable) [ ] Additional provisions of these Articles of Incorporation are set forth in Exhibit ___ attached hereto and made a part hereof. (13-C MRSA §202) |
| `entity.authorized_shares_total` | text | high | FOURTH: ...The number of authorized shares is ___ |
| `entity.director_liability_limited` | checkbox | high | SIXTH: [ ] To the fullest extent permitted by 13-C MRSA §202.2.D, a director shall have no liability to the Corporation or its shareholders for money damages for an action taken or a failure to take action as a director. |
| `entity.directors_count_limited` | checkbox | high | SIXTH: [ ] The number of directors is limited as follows: not fewer than ___ nor more than ___ directors. (13-C MRSA §803) |
| `entity.directors_max_count` | text | high | nor more than ___ directors |
| `entity.directors_min_count` | text | high | not fewer than ___ |

## Conditional logic

- Exactly one of the six top-of-page filing-purpose checkboxes is selected (filing.accompanying_filing_type is one of the 6 enum values, not null and not multiple). (depends on `filing.accompanying_filing_type`)
- entity.name is non-empty. (depends on `entity.name`)
- If entity.is_professional_corporation is true, entity.professional_services_description must be non-empty; if false, it must be empty. (depends on `entity.is_professional_corporation`, `entity.professional_services_description`)
- Exactly one of the SECOND clerk-type options is selected (commercial XOR noncommercial). (depends on `clerk.type`)
- If clerk.type='commercial', clerk.cra_public_number must be present; if 'noncommercial', it must be absent. (depends on `clerk.type`, `clerk.cra_public_number`)
- clerk.physical_address must not begin with 'P.O.', 'PO Box', or 'Post Office Box' (form forbids P.O. Box for physical location). (depends on `clerk.physical_address`)
- Exactly one of the FOURTH share-structure options is selected (single_class XOR multi_class). (depends on `entity.share_structure`)
- If entity.share_structure='single_class', entity.authorized_shares_total must be a positive integer. (depends on `entity.share_structure`, `entity.authorized_shares_total`)
- If entity.share_structure='multi_class', entity.multi_class_exhibit_letter must be a single uppercase letter. (depends on `entity.share_structure`, `entity.multi_class_exhibit_letter`)
- Exactly one of the FIFTH board-structure options is selected (board XOR no-board). (depends on `entity.has_board_of_directors`)
- If entity.directors_count_limited is true, both entity.directors_min_count and entity.directors_max_count are positive integers and min <= max. (depends on `entity.directors_count_limited`, `entity.directors_min_count`, `entity.directors_max_count`)
- If entity.additional_provisions_present is true, entity.additional_provisions_exhibit_letter must be a single uppercase letter. (depends on `entity.additional_provisions_present`, `entity.additional_provisions_exhibit_letter`)

## Example case data

```json
{
  "filing": {
    "accompanying_filing_type": "Sample Value"
  },
  "entity": {
    "is_professional_corporation": true,
    "professional_services_description": "Sample Value",
    "is_benefit_corporation": true,
    "name": "Wabanaki Widgets, Inc."
  },
  "clerk": {
    "cra_public_number": "P99999",
    "type": "Sample Value",
    "name": "Sample Value"
  }
}
```
