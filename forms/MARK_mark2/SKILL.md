# SKILL: Filling MARK_mark2

**Form:** Application for Renewal of a Mark  
**Entity type:** Trademark / Service Mark  
**When to use:** Renew an existing Maine trademark, service mark, or collective mark registration under 10 MRSA §1524. Recites the original charter number, the original mark's text and design features (amendments to TEXT/FEATURES are NOT permitted on renewal), the type of mark (with optional amendment from the original), and any class additions or deletions. Mark.* schema family is shared verbatim with MARK_mark1 (initial registration); only renewal-specific keys (mark.charter_number, mark.type, mark.type_amended, mark.class_changes[*]) are introduced here.

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
| `filing.date_signed` | text | high | G. Date of this application |
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.expedited_service` | text | high | Hold attested copy for pick up |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |

_Showing 12 of 36 canonical keys — the full set is in mapping.json._

## Conditional logic

- mark.applicant.entity_name is non-empty (mark owner's identity). (depends on `mark.applicant.entity_name`)
- mark.applicant.mailing_address is non-empty. (depends on `mark.applicant.mailing_address`)
- At least one of mark.text_words.line1 or mark.design_features.line1 is non-empty (the original mark must have had text or design content). (depends on `mark.text_words.line1`, `mark.design_features.line1`)
- mark.type is non-empty. (depends on `mark.type`)
- Exactly one of the C 'amendment yes / no' checkboxes is selected. (depends on `mark.type_amended`)
- If mark.class_changes[0].class_number is set, exactly one of mark.class_changes[0].action ('added' / 'deleted') must also be set. (depends on `mark.class_changes[0].class_number`, `mark.class_changes[0].action`)
- If mark.class_changes[0].action='added', mark.class_changes[0].description.line1 must be non-empty. (depends on `mark.class_changes[0].action`, `mark.class_changes[0].description.line1`)
- Exactly one mark.applicant.entity_type option is selected. (depends on `mark.applicant.entity_type`)
- If mark.applicant.entity_type='other', mark.applicant.entity_type_other_explanation must be non-empty. (depends on `mark.applicant.entity_type`, `mark.applicant.entity_type_other_explanation`)
- If mark.applicant.entity_type is one of {corporation, limited_partnership, general_partnership, association, union} (or 'other' resolving to a registered entity), mark.applicant.jurisdiction_of_organization and mark.applicant.date_of_organization must be set. (depends on `mark.applicant.entity_type`, `mark.applicant.jurisdiction_of_organization`, `mark.applicant.date_of_organization`)
- mark.signer.printed_name_and_capacity is non-empty. (depends on `mark.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty and not in the future. (depends on `filing.date_signed`)

## Example case data

```json
{
  "mark": {
    "charter_number": 99999,
    "text_words": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "design_features": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "type": "Sample Value",
    "type_amended": true,
    "class_changes": [
      {
        "class_number": "99999"
      }
    ]
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
