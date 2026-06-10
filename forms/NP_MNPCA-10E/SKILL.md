# SKILL: Filling NP_MNPCA-10E

**Form:** Articles of Consolidation (Domestic and Foreign Nonprofit Corporations)  
**Entity type:** Nonprofit Corporation  
**When to use:** Consolidate two or more existing nonprofit corporations (domestic and/or foreign) into a single NEW nonprofit corporation under 13-B MRSA §906. Distinct from a merger (which produces a survivor): consolidation produces a brand-new entity. Records the names + descriptors of participating corps, the new consolidated entity, the plan-of-consolidation exhibit, per-domestic-party adoption manner (4 mutually-exclusive vote/consent options each with date), registered-office addresses for each party, optional future effective date, and dual signature blocks with member-vote clerk certifications.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `consolidation.effective_date` | text | high | SIXTH: Effective date of the consolidation (if later than date of filing of Articles) is ___ (Not to exceed 60 days from date of filing of the Articles) |
| `consolidation.foreign_jurisdictions` | text | high | FIRST: The laws of the State(s) of ___, under which the foreign corporation(s) is (are) organized, permit said corporation(s) and the domestic corporation(s) to consolidate. |
| `consolidation.new_entity.descriptor` | text | high | (A ___ Corporation) FORMING — new corp descriptor |
| `consolidation.new_entity.governing_law_state` | text | high | SECOND: ...and it is to be governed by the laws of the State of ___ |
| `consolidation.new_entity.name` | text | high | (A ___ Corporation) FORMING — new consolidated corp name (fills multiple widgets) |
| `consolidation.new_entity.service_address` | text | high | SECOND: ...the address to which the Secretary of State shall mail a copy of any process in such proceeding is ___ |
| `consolidation.parties[0].adoption_date` | text | high | FOURTH option 1 date: ...at a meeting on (date) ___ (fills multiple widgets) |
| `consolidation.parties[0].adoption_method` | text | high | FOURTH option 1: [ ] By the members at a meeting on (date) ___ at which a quorum was present and such plan received at least a majority of the votes which members were entitled to cast. (fills multiple widgets) |
| `consolidation.parties[0].descriptor` | text | high | (A ___ Corporation) — first participating corp descriptor |
| `consolidation.parties[0].name` | text | high | (A ___ Corporation) — first participating corp name (top recital) (fills multiple widgets) |
| `consolidation.parties[0].registered_office_address_line2` | text | high | FIFTH (domestic): ___ (street, city, state and zip code) |
| `consolidation.parties[0].signature_block.corporation_name` | text | high | (name of corporation) — signature block 1, right column |

_Showing 12 of 39 canonical keys — the full set is in mapping.json._

## Conditional logic

- At least two consolidation.parties[N].name are non-empty (consolidation requires ≥2 participating corporations). (depends on `consolidation.parties[0].name`, `consolidation.parties[1].name`)
- If consolidation.parties[N].name is non-empty, consolidation.parties[N].descriptor must also be non-empty (every party has a name + descriptor pair on page 0). (depends on `consolidation.parties[0].name`, `consolidation.parties[0].descriptor`, `consolidation.parties[1].name`, `consolidation.parties[1].descriptor`)
- consolidation.new_entity.name and consolidation.new_entity.descriptor are both non-empty (the consolidation produces a NEW corp, which must be named). (depends on `consolidation.new_entity.name`, `consolidation.new_entity.descriptor`)
- consolidation.plan_exhibit_letter is a single uppercase letter (THIRD references the plan via exhibit). (depends on `consolidation.plan_exhibit_letter`)
- consolidation.parties[0].adoption_method is exactly one of the 4 enum values (FOURTH 'X one box only'). (depends on `consolidation.parties[0].adoption_method`)
- If consolidation.parties[0].adoption_method is set, consolidation.parties[0].adoption_date must also be set. (depends on `consolidation.parties[0].adoption_method`, `consolidation.parties[0].adoption_date`)
- Both parties' FIFTH registered-office addresses (line2, the labeled street/city/state/zip line) are non-empty. (depends on `consolidation.parties[0].registered_office_address_line2`, `consolidation.parties[1].registered_office_address_line2`)
- If consolidation.effective_date is set, it must be on or after filing.date_signed AND no later than filing.date_signed + 60 days (per 13-B MRSA §906 cap). (depends on `consolidation.effective_date`, `filing.date_signed`)
- Each party's signature_block has date_signed, corporation_name, and printed_name_and_capacity populated. (signature widget is wet-ink and may be blank.) (depends on `consolidation.parties[0].signature_block.date_signed`, `consolidation.parties[0].signature_block.corporation_name`, `consolidation.parties[0].signature_block.printed_name_and_capacity`, `consolidation.parties[1].signature_block.date_signed`, `consolidation.parties[1].signature_block.corporation_name`, `consolidation.parties[1].signature_block.printed_name_and_capacity`)
- Exactly one of the cover-letter expedite checkboxes ('hold' / '24h' / 'imm') is selected. (depends on `filing.expedited_service`)

## Example case data

```json
{
  "consolidation": {
    "parties[0]": {
      "name": "Sample Value",
      "descriptor": "Sample Value"
    },
    "parties[1]": {
      "name": "Sample Value",
      "descriptor": "Sample Value"
    },
    "new_entity": {
      "name": "Sample Value",
      "descriptor": "Sample Value",
      "governing_law_state": "Sample Value"
    },
    "foreign_jurisdictions": "Sample Value"
  }
}
```
