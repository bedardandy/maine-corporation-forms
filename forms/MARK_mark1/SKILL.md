# SKILL: Filling MARK_mark1

**Form:** Application for Registration of a Mark  
**Entity type:** Trademark / Service Mark  
**When to use:** Register a trademark, service mark, or collective mark with the Maine Secretary of State under 10 MRSA §1522. Captures dates of first use (anywhere and in Maine), the mark's text and design features, type and class number, descriptions of goods/services and usage, applicant identity, applicant entity-type classification, and jurisdiction of incorporation/organization.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `filing.attested_copy_recipient.firm` | text | high | Firm or Company |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | City, State & Zip |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | Mailing Address |
| `filing.attested_copy_recipient.name` | text | high | Name of attested copy recipient |
| `filing.contact.email` | text | high | Contact email address for this filing |
| `filing.contact.name` | text | high | Name of contact person |
| `filing.contact.phone` | text | high | Daytime telephone number |
| `filing.date_signed` | text | high | G: Date of this application |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up (fills multiple widgets) |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

_Showing 12 of 35 canonical keys — the full set is in mapping.json._

## Conditional logic

- mark.dates_of_first_use.anywhere is non-empty. (depends on `mark.dates_of_first_use.anywhere`)
- mark.dates_of_first_use.in_maine is non-empty. (depends on `mark.dates_of_first_use.in_maine`)
- mark.dates_of_first_use.anywhere is on or before mark.dates_of_first_use.in_maine (a mark must have been used 'anywhere' at least as early as it was first used in Maine). (depends on `mark.dates_of_first_use.anywhere`, `mark.dates_of_first_use.in_maine`)
- At least one of mark.text_words.line1 or mark.design_features.line1 is non-empty (a mark must have at least text words or design features; empty marks aren't registrable). (depends on `mark.text_words.line1`, `mark.design_features.line1`)
- mark.type_and_class_number is non-empty. (depends on `mark.type_and_class_number`)
- mark.goods_or_services_description.line1 is non-empty. (depends on `mark.goods_or_services_description.line1`)
- mark.usage_description.line1 is non-empty. (depends on `mark.usage_description.line1`)
- Exactly one mark.applicant.entity_type option is selected. (depends on `mark.applicant.entity_type`)
- If mark.applicant.entity_type='other', mark.applicant.entity_type_other_explanation must be non-empty. (depends on `mark.applicant.entity_type`, `mark.applicant.entity_type_other_explanation`)
- If mark.applicant.entity_type is one of {'corporation', 'limited_partnership', 'general_partnership', 'association', 'union'} (or 'other' with an entity-like explanation), mark.applicant.jurisdiction_of_organization and mark.applicant.date_of_organization must be set. (depends on `mark.applicant.entity_type`, `mark.applicant.jurisdiction_of_organization`, `mark.applicant.date_of_organization`)
- mark.signer.printed_name_and_capacity and mark.applicant.entity_name are both non-empty. (depends on `mark.signer.printed_name_and_capacity`, `mark.applicant.entity_name`)
- mark.applicant.mailing_address is non-empty. (depends on `mark.applicant.mailing_address`)

## Example case data

```json
{
  "mark": {
    "dates_of_first_use": {
      "anywhere": "Sample Value",
      "in_maine": "Sample Value"
    },
    "predecessor_name_and_address": "Sample Value",
    "text_words": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "design_features": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "type_and_class_number": 99999
  }
}
```
