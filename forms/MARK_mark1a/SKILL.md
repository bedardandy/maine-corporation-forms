# SKILL: Filling MARK_mark1a

**Form:** Mark Disclaimer  
**Entity type:** Trademark / Service Mark  
**When to use:** File a disclaimer of exclusive rights to specific portions of a trademark or service mark (text or design features) when registering a mark with the Maine Secretary of State under 10 MRSA §1521 et seq. Filed in conjunction with the primary mark-registration application (MARK_mark1) — does not stand alone, so the applicant identity and mark name live on the parent form, not on this one.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `disclaimer.disclaimed_portion_description.line1` | text | high | A. I hereby disclaim the exclusive right to (describe portion of text or feature disclaimed) — line 1 |
| `disclaimer.disclaimed_portion_description.line2` | text | high | A. (continuation) — line 2 |
| `filing.date_signed` | text | high | Dated: |
| `mark.design_features.line1` | text | high | B.2. FEATURES - describe in detail the design to be protected, if any (if none, so indicate) — line 1 |
| `mark.design_features.line2` | text | high | B.2. FEATURES (continuation) — line 2 |
| `mark.text_words.line1` | text | high | B.1. TEXT - list word(s) to be protected, if any (if none, so indicate) — line 1 |
| `mark.text_words.line2` | text | high | B.1. TEXT (continuation) — line 2 |
| `mark.type` | enum_select | high | C. TYPE OF MARK: Trademark - a mark applied to goods applicant manufactures or sells |

## Conditional logic

- disclaimer.disclaimed_portion_description.line1 is non-empty (the form's purpose is to disclaim something — empty disclaimer is meaningless). (depends on `disclaimer.disclaimed_portion_description.line1`)
- Exactly one mark.type checkbox is selected (form instruction: 'X' one box only). (depends on `mark.type`)
- At least one of mark.text_words.line1 or mark.design_features.line1 is non-empty (or both contain explicit 'none' per the form's 'if none, so indicate' instruction). The mark must claim something protectable beyond the disclaimed portion. (depends on `mark.text_words.line1`, `mark.design_features.line1`)
- filing.date_signed is non-empty. (depends on `filing.date_signed`)

## Example case data

```json
{
  "disclaimer": {
    "disclaimed_portion_description": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    }
  },
  "mark": {
    "text_words": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "design_features": {
      "line1": "Sample Value",
      "line2": "Sample Value"
    },
    "type": "trademark"
  },
  "filing": {
    "date_signed": "2026-01-15"
  }
}
```
