# SKILL: Filling NP_MNP-9

**Form:** Certificate of Amendment (Domestic Nonprofit Corporation)  
**Entity type:** Nonprofit Corporation  
**When to use:** File a Certificate of Amendment to amend the articles of organization of a Maine domestic nonprofit corporation under 13-B MRSA §934. Captures entity name, nonprofit type (public-benefit vs mutual-benefit), the inline nature-and-text of the amendment (15-line free-text block), the adoption date and method (member vote vs board/managing-board vote), and the secretary/clerk authorized signature.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `amendment.adoption_date` | text | high | THIRD: The amendment was adopted on (date) ___ |
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
| `amendment.nature_and_text.line5` | text | high | SECOND: amendment text (line 5) |

## Conditional logic

- entity.name is non-empty (header) and matches filing.entities[0].name (cover-letter row 1). (depends on `entity.name`, `filing.entities[0].name`)
- Exactly one of FIRST public_benefit/mutual_benefit options is selected. (depends on `entity.nonprofit_type`)
- At least amendment.nature_and_text.line1 is non-empty (a Certificate of Amendment must describe what is changing). (depends on `amendment.nature_and_text.line1`)
- amendment.adoption_date is non-empty. (depends on `amendment.adoption_date`)
- amendment.adoption_date is not in the future relative to filing.date_signed. (depends on `amendment.adoption_date`, `filing.date_signed`)
- Exactly one of THIRD member_vote/board_of_directors_majority_vote options is selected. (depends on `amendment.adoption_method`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)
- filing.signer.printed_name_and_capacity is non-empty (Shape D). (depends on `filing.signer.printed_name_and_capacity`)
- filing.signer.printed_name_and_capacity contains 'Secretary' or 'Clerk' (form footnote requires the document be signed by the secretary or clerk). (depends on `filing.signer.printed_name_and_capacity`)

## Example case data

```json
{
  "entity": {
    "name": "Wabanaki Widgets, Inc.",
    "nonprofit_type": true
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
