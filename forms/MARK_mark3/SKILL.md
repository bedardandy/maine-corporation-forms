# SKILL: Filling MARK_mark3

**Form:** Application for Amendment of a Mark  
**Entity type:** Trademark / Service Mark  
**When to use:** Amend an existing Maine trademark/service mark registration under 10 MRSA §1525-A. Permits adding/deleting classes of goods/services and updating the owner's contact information. Page-0 instructions explicitly prohibit amending the text or design features of the mark itself — those changes require a new application (MARK-1). Captures (A) charter number of the existing registration, (B) a recital of existing text and design features, (C) current type of mark and a yes/no for whether the type is being amended, (D) class number being added/deleted plus description of goods/services and manner of use, (E-F) a refreshed applicant identity block (name, mailing address, entity type, jurisdiction, formation date), (G) date of application, and a single signer block. 3 pages, 45 widgets.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.additional_pages_attached` | text | high | [ ] Attach additional pages, if necessary. |
| `amendment.class_action` | text | high | [ ] Deleted (fills multiple widgets) |
| `amendment.class_number` | text | high | CLASS NUMBER: |
| `amendment.manner_of_use` | text | high | DESCRIBE manner in which mark is applied to the goods or used to promote their sale and/or the manner in which the mark is used in connection with the service — line 1 (fills multiple widgets) |
| `amendment.new_class_description` | text | high | DESCRIBE goods manufactured or sold and/or the service that is provided |
| `filing.attested_copy_recipient.firm` | text | high | (Firm or Company) |
| `filing.attested_copy_recipient.mailing_address.city_state_zip` | text | high | (City, State & Zip) |
| `filing.attested_copy_recipient.mailing_address.street` | text | high | (Mailing Address) |
| `filing.attested_copy_recipient.name` | text | high | (Name of attested copy recipient) |
| `filing.contact.email` | text | high | (Contact email address for this filing) |
| `filing.contact.name` | text | high | (Name of contact person) |
| `filing.contact.phone` | text | high | (Daytime telephone number) |

_Showing 12 of 34 canonical keys — the full set is in mapping.json._

## Conditional logic

- mark.applicant.entity_name is non-empty (mark owner identity, refreshed on amendment). (depends on `mark.applicant.entity_name`)
- mark.applicant.mailing_address is non-empty. (depends on `mark.applicant.mailing_address`)
- Exactly one mark.applicant.entity_type option is selected. (depends on `mark.applicant.entity_type`)
- If mark.applicant.entity_type='other', mark.applicant.entity_type_other_explanation must be non-empty. (depends on `mark.applicant.entity_type`, `mark.applicant.entity_type_other_explanation`)
- If mark.applicant.entity_type is one of {'corporation','limited_partnership','general_partnership','association','union'}, mark.applicant.jurisdiction_of_organization and mark.applicant.date_of_organization must be set. (depends on `mark.applicant.entity_type`, `mark.applicant.jurisdiction_of_organization`, `mark.applicant.date_of_organization`)
- Exactly one of mark.type_changed yes/no checkboxes is selected. (depends on `mark.type_changed`)
- Exactly one of amendment.class_action 'added'/'deleted' checkboxes is selected (or amendment.additional_pages_attached=true if amending multiple classes via exhibit). (depends on `amendment.class_action`, `amendment.additional_pages_attached`)
- If amendment.class_action='added', amendment.new_class_description and amendment.manner_of_use must both be non-empty (a class addition must describe the goods/services and manner of use). If 'deleted', both may be empty. (depends on `amendment.class_action`, `amendment.new_class_description`, `amendment.manner_of_use`)
- mark.signer.printed_name_and_capacity is non-empty. (depends on `mark.signer.printed_name_and_capacity`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.contact.{name,phone,email} are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "mark": {
    "charter_number": "P99999",
    "text_elements": "Sample Value",
    "design_description": "Sample Value",
    "type": "Sample Value",
    "original_type_if_changed": true,
    "type_change_explanation": true,
    "type_changed": "Sample Value"
  },
  "amendment": {
    "class_number": "P99999"
  }
}
```
