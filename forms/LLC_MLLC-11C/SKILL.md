# SKILL: Filling LLC_MLLC-11C

**Form:** Certificate of Cancellation (Domestic LLC)  
**Entity type:** Limited Liability Company  
**When to use:** Cancel a Maine domestic limited liability company under 31 MRSA §1533.2 (and 31 MRSA §1676.1.B/C for the signer). Records (FIRST) the date the original certificate of formation was filed, (SECOND) the date the LLC was dissolved (if known), (THIRD) the cancellation effective-date election (date of filing OR a future date), (FOURTH) any additional information set forth in an exhibit, and a single signer block with date and printed-name-and-capacity. Filing fee is $75 per the page-0 header. 2 pages, 24 widgets — page 1 is the standard cover-letter primitive.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `cancellation.future_effective_date` | text | high | the future effective date as follows: ___ |
| `entity.dissolution_date` | text | high | SECOND: The limited liability company is dissolved and the date of dissolution (if known) is |
| `entity.formation_date` | text | high | FIRST: The date the limited liability company's original certificate of formation was filed |
| `entity.name` | text | high | (Name of Limited Liability Company) |
| `filing.additional_info_exhibit_letter` | text | high | FOURTH: ...set forth in Exhibit ___ attached and made a part hereof |
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |

_Showing 12 of 21 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name is non-empty. (depends on `entity.name`)
- entity.formation_date is non-empty. (depends on `entity.formation_date`)
- filing.date_signed is on or after entity.formation_date — cannot cancel before formation. (depends on `filing.date_signed`, `entity.formation_date`)
- Exactly one of the THIRD options is selected (cancellation.effective_date_type is one of 'date_of_filing' | 'future_date'). (depends on `cancellation.effective_date_type`)
- If cancellation.effective_date_type='future_date', cancellation.future_effective_date must be set and not in the past relative to filing.date_signed. (depends on `cancellation.effective_date_type`, `cancellation.future_effective_date`, `filing.date_signed`)
- filing.date_signed is non-empty and on or before today. (depends on `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty. (depends on `filing.signer.printed_name_and_capacity`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "formation_date": "2026-01-15",
    "dissolution_date": "2026-01-15"
  },
  "cancellation": {
    "future_effective_date": "2026-01-15"
  },
  "filing": {
    "additional_info_exhibit_letter": "Sample Value",
    "date_signed": "2026-01-15",
    "signer": {
      "printed_name_and_capacity": "Sample Value"
    },
    "entities[0]": {
      "name": "Sample Value"
    }
  }
}
```
