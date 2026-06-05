# SKILL: Filling NP_MNPCA-9

**Form:** Articles of Amendment (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** Amend the Articles of Incorporation of a Maine domestic nonprofit corporation under 13-B MRSA §§802 and 803. The form captures the entity name, nonprofit type (public benefit vs mutual benefit), the inline 15-line nature-of-change/text-of-amendment block, the adoption date and method (member majority, member supermajority, written consent of all members, or board majority), the registered office address (two-line), and the authorized officer signature (two slots; only the first is required).

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.adoption_date` | text | high | THIRD: The amendment was adopted on (date) |
| `amendment.adoption_method` | text | high | THIRD: [ ] By the members at a meeting at which a quorum was present and the amendment received at least a majority of the votes which members were entitled to cast. (fills multiple widgets) |
| `amendment.nature_and_text.line1` | text | high | SECOND: NATURE OF CHANGE / TEXT of amendment (line 1 — top) |
| `amendment.nature_and_text.line10` | text | high | SECOND: amendment text (line 10) |
| `amendment.nature_and_text.line11` | text | high | SECOND: amendment text (line 11) |
| `amendment.nature_and_text.line12` | text | high | SECOND: amendment text (line 12) |
| `amendment.nature_and_text.line13` | text | high | SECOND: amendment text (line 13) |
| `amendment.nature_and_text.line14` | text | high | SECOND: amendment text (line 14) |
| `amendment.nature_and_text.line15` | text | high | SECOND: amendment text (line 15 — bottom) |
| `amendment.nature_and_text.line2` | text | high | SECOND: amendment text (line 2) |
| `amendment.nature_and_text.line3` | text | high | SECOND: amendment text (line 3) |
| `amendment.nature_and_text.line4` | text | high | SECOND: amendment text (line 4) |

## Conditional logic

- entity.name is non-empty (header) and matches filing.entities[0].name (cover-letter row 1). (depends on `entity.name`, `filing.entities[0].name`)
- Exactly one of FIRST public_benefit/mutual_benefit options is selected. (depends on `entity.nonprofit_type`)
- At least amendment.nature_and_text.line1 is non-empty (an Articles of Amendment must describe what is changing). (depends on `amendment.nature_and_text.line1`)
- amendment.adoption_date is non-empty. (depends on `amendment.adoption_date`)
- amendment.adoption_date is not in the future relative to filing.date_signed. (depends on `amendment.adoption_date`, `filing.date_signed`)
- Exactly one of THIRD adoption-method options is selected (member_majority_at_meeting / member_supermajority_at_meeting / member_written_consent / board_of_directors_majority_vote). (depends on `amendment.adoption_method`)
- registered_office.address_line2 (the wide labeled street/city/state/zip line) is non-empty. (depends on `registered_office.address_line2`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.signer_1.printed_name_and_capacity is non-empty (at least one duly authorized officer must sign per 13-B MRSA §104.1.B). (depends on `filing.signer_1.printed_name_and_capacity`)
- filing.contact.name, filing.contact.phone, and filing.contact.email are all non-empty. (depends on `filing.contact.name`, `filing.contact.phone`, `filing.contact.email`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "nonprofit_type": "Sample Value"
  },
  "amendment": {
    "nature_and_text": {
      "line1": "Sample Value",
      "line2": "Sample Value",
      "line3": "Sample Value",
      "line4": "Sample Value",
      "line5": "Sample Value",
      "line6": "Sample Value"
    }
  }
}
```
