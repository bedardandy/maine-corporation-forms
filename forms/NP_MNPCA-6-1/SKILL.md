# SKILL: Filling NP_MNPCA-6-1

**Form:** Articles of Incorporation (Nonprofit) — to accompany Conversion or Restatement  
**Entity type:** Nonprofit Corporation  
**When to use:** Attachment-form variant of MNPCA-6 (Articles of Incorporation, 13-B MRSA §403) used when articles are filed alongside an Articles of Nonprofit Conversion (13-C MRSA §933), Statement of Conversion (31 MRSA §1645), or Restated Articles of Incorporation (13-B MRSA §805). Captures entity name, public-vs-mutual benefit purpose, registered agent, board structure, member structure, and optional 501(c)/political-activities provisions. Has no incorporator signature block — signatures are on the accompanying primary document and no cover-letter block (cover letter is filed with the primary).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.501c_exhibit_letter` | text | high | Exhibit ___ attached hereto |
| `entity.directors_max_count` | text | high | FIFTH: ...and the maximum number of directors shall be ___ |
| `entity.directors_min_count` | text | high | FIFTH: The minimum number of directors (not less than 3) shall be ___ |
| `entity.has_501c_exhibit` | checkbox | high | EIGHTH: (Optional) ... Other provisions ... are set out in Exhibit ___ |
| `entity.has_members` | checkbox | high | SIXTH: There shall be no members. (fills multiple widgets) |
| `entity.initial_directors_count` | text | high | FIFTH: ...the initial board of directors of the corporation, if the number has been determined ... is ___ |
| `entity.mutual_benefit_purpose` | text | high | (mutual benefit purposes description) |
| `entity.name` | text | high | FIRST: The name of the corporation is |
| `entity.no_political_activities_clause` | text | high | SEVENTH: (Optional) ... No substantial part of the activities ... shall be the carrying on of propaganda ... |
| `entity.nonprofit_type` | text | high | SECOND: The corporation is organized as a public benefit corporation for the following purpose or purposes (fills multiple widgets) |
| `entity.public_benefit_purpose` | text | high | (public benefit purposes description) |
| `filing.accompanying_document_type` | text | high | Articles of Nonprofit Conversion (13-C MRSA §933) (fills multiple widgets) |

_Showing 12 of 17 canonical keys — the full set is in mapping.json._

## Conditional logic

- Exactly one of the three accompanying-document-type checkboxes is selected. (depends on `filing.accompanying_document_type`)
- entity.name is non-empty. (depends on `entity.name`)
- Exactly one of SECOND public_benefit/mutual_benefit options is selected. (depends on `entity.nonprofit_type`)
- If nonprofit_type = 'public_benefit', entity.public_benefit_purpose must be non-empty. If nonprofit_type = 'mutual_benefit' AND not 'all purposes permitted', entity.mutual_benefit_purpose must be non-empty. (depends on `entity.nonprofit_type`, `entity.public_benefit_purpose`, `entity.mutual_benefit_purpose`)
- Exactly one of THIRD commercial/noncommercial options is selected. (depends on `registered_agent.type`)
- If registered_agent.type = 'commercial', registered_agent.cra_public_number must be set. (depends on `registered_agent.type`, `registered_agent.cra_public_number`)
- If entity.initial_directors_count is set, it must be ≥3. If min/max are set, both must be ≥3 and min ≤ max. (depends on `entity.initial_directors_count`, `entity.directors_min_count`, `entity.directors_max_count`)
- Exactly one of SIXTH no-members/has-members options is selected. (depends on `entity.has_members`)
- If entity.has_501c_exhibit is true, entity.501c_exhibit_letter must be set. (depends on `entity.has_501c_exhibit`, `entity.501c_exhibit_letter`)

## Example case data

```json
{
  "filing": {
    "accompanying_document_type": "Sample Value"
  },
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "nonprofit_type": "Sample Value",
    "public_benefit_purpose": "Sample Value",
    "mutual_benefit_purpose": "Sample Value"
  },
  "registered_agent": {
    "type": "Sample Value",
    "cra_public_number": "P99999",
    "name": "Sample Value"
  }
}
```
