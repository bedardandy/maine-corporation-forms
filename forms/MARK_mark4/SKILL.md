# SKILL: Filling MARK_mark4

**Form:** Application for Assignment of a Mark  
**Entity type:** Trademark / Service Mark  
**When to use:** Record the assignment (transfer of ownership) of a registered Maine trademark or service mark under 10 MRSA §1525. Recites the original mark by charter number and TEXT/FEATURES (no amendments permitted), identifies assignor and assignee with parallel entity-type/jurisdiction blocks, and captures the transfer date and signatures. The mark.* schema family is shared with MARK_mark1 (registration), MARK_mark2 (renewal), and MARK_mark6 (cancellation); this form adds mark.assignor.*, mark.assignee.*, and mark.assignment.* sub-namespaces to capture the two-party transfer pattern.

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
| `filing.entities[0].name` | text | high | Name of entity(s) on the submitted filings [1] |
| `filing.entities[1].name` | text | high | Name of entity [2] |
| `filing.total_fees_dollars` | text | high | Total fee(s) enclosed: $ |
| `mark.assignee.date_of_organization` | text | high | E.2: ...and the date of incorporation/organization is |
| `mark.assignee.date_signed` | text | high | E.3: Dated |

_Showing 12 of 35 canonical keys — the full set is in mapping.json._

## Conditional logic

- At least one of mark.charter_number, mark.text_words.line1, or mark.design_features.line1 is non-empty (the assigned mark must be identifiable). Mirrors MARK_mark6's mark-identifier check. (depends on `mark.charter_number`, `mark.text_words.line1`, `mark.design_features.line1`)
- mark.type is non-empty (TYPE recited from the original registration; amendments not permitted on assignment). (depends on `mark.type`)
- mark.assignor.name_and_address is non-empty. (depends on `mark.assignor.name_and_address`)
- Exactly one mark.assignor.entity_type option is selected. (depends on `mark.assignor.entity_type`)
- If mark.assignor.entity_type='other', mark.assignor.entity_type_other_explanation must be non-empty. (depends on `mark.assignor.entity_type`, `mark.assignor.entity_type_other_explanation`)
- If mark.assignor.entity_type is one of {corporation, limited_partnership, general_partnership, association, union} (or 'other' resolving to a registered entity), mark.assignor.jurisdiction_of_organization and mark.assignor.date_of_organization must be set. (depends on `mark.assignor.entity_type`, `mark.assignor.jurisdiction_of_organization`, `mark.assignor.date_of_organization`)
- mark.assignor.printed_name_and_capacity is non-empty (binds to both the Whereas recital and the Signature-line widgets). (depends on `mark.assignor.printed_name_and_capacity`)
- mark.assignor.date_signed is non-empty and not in the future. (depends on `mark.assignor.date_signed`)
- mark.assignment.date_of_transfer is non-empty and not after mark.assignor.date_signed (the assignment cannot be effective after the assignor signed). (depends on `mark.assignment.date_of_transfer`, `mark.assignor.date_signed`)
- mark.assignee.name_and_address is non-empty. (depends on `mark.assignee.name_and_address`)
- Exactly one mark.assignee.entity_type option is selected. (depends on `mark.assignee.entity_type`)
- If mark.assignee.entity_type implies a registered entity, mark.assignee.jurisdiction_of_organization and mark.assignee.date_of_organization must be set. (depends on `mark.assignee.entity_type`, `mark.assignee.jurisdiction_of_organization`, `mark.assignee.date_of_organization`)
- mark.assignee.date_signed is non-empty and on or after mark.assignment.date_of_transfer. (depends on `mark.assignee.date_signed`, `mark.assignment.date_of_transfer`)

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
    "assignor": {
      "name_and_address": "Sample Value",
      "entity_type": "Sample Value"
    }
  }
}
```
