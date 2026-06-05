# SKILL: Filling NP_MNPCA-16

**Form:** Approval of Local Development Corporation by Municipal Officers  
**Entity type:** Nonprofit Corporation  
**When to use:** Record the majority vote of municipal officers authorizing the formation of a Local Development Corporation (LDC) under 5 MRSA §13120-B.9. Filed as an attachment to the Articles of Incorporation (NP_MNPCA-6) for an LDC; carries no cover letter of its own and 'No Fee Required' (the LDC's MNPCA-6 carries the standard $40 fee).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `entity.name` | text | high | The name of the corporation is intended to be ___ |
| `filing.date_signed` | text | high | Dated: ___ (Affix Municipal Seal) |
| `municipal_clerk.printed_name_and_capacity` | text | high | Attest: ___ (Signature of Municipal Clerk) / (type or print name and capacity) |
| `municipal_officer_1.printed_name_and_capacity` | text | high | Name and Capacity (signature row 1) |
| `municipal_officer_2.printed_name_and_capacity` | text | high | Name and Capacity (signature row 2) |
| `municipal_officer_3.printed_name_and_capacity` | text | high | Name and Capacity (signature row 3) |
| `municipal_officer_4.printed_name_and_capacity` | text | high | Name and Capacity (signature row 4) |
| `municipal_officer_5.printed_name_and_capacity` | text | high | Name and Capacity (signature row 5) |
| `municipality.additional_officers_exhibit_letter` | text | high | ...attached hereto as Exhibit ___ |
| `municipality.additional_officers_present` | checkbox | high | [ ] Names, capacities and signatures of additional municipal officers attached hereto as Exhibit ___, and made a part hereof |
| `municipality.name` | text | high | The municipal officers of ___ have, by majority vote, authorized the formation of a Local Development Corporation |

## Conditional logic

- municipality.name is non-empty. (depends on `municipality.name`)
- entity.name (the proposed LDC name) is non-empty and matches the entity.name on the accompanying NP_MNPCA-6. (depends on `entity.name`)
- At least one municipal_officer_N.printed_name_and_capacity (N=1..5) is populated. The form recites 'majority vote' but provides no widgets to capture the body's total size, so a single populated row is the floor for syntactic completeness; a true majority check requires out-of-band knowledge of the council/select-board's composition. (depends on `municipal_officer_1.printed_name_and_capacity`, `municipal_officer_2.printed_name_and_capacity`, `municipal_officer_3.printed_name_and_capacity`, `municipal_officer_4.printed_name_and_capacity`, `municipal_officer_5.printed_name_and_capacity`)
- If municipality.additional_officers_present is true, municipality.additional_officers_exhibit_letter must be a non-empty letter (A, B, …). (depends on `municipality.additional_officers_present`, `municipality.additional_officers_exhibit_letter`)
- municipal_clerk.printed_name_and_capacity is non-empty. (depends on `municipal_clerk.printed_name_and_capacity`)
- filing.date_signed is non-empty and on or before the date the bundled NP_MNPCA-6 is filed (the LDC-authorization vote must precede or accompany incorporation). (depends on `filing.date_signed`)

## Example case data

```json
{
  "municipality": {
    "name": "Sample Value",
    "additional_officers_present": true
  },
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  },
  "municipal_officer_1": {
    "printed_name_and_capacity": "Sample Value"
  },
  "municipal_officer_2": {
    "printed_name_and_capacity": "Sample Value"
  },
  "municipal_officer_3": {
    "printed_name_and_capacity": "Sample Value"
  },
  "municipal_officer_4": {
    "printed_name_and_capacity": "Sample Value"
  },
  "municipal_officer_5": {
    "printed_name_and_capacity": "Sample Value"
  }
}
```
