# SKILL: Filling NP_MNPCA-10A

**Form:** Articles of Consolidation (Domestic Nonprofit Corporations)  
**Entity type:** Nonprofit Corporation  
**When to use:** Consolidate two existing Maine domestic nonprofit corporations into a brand-new Maine nonprofit corporation under 13-B MRSA §904 or 13 MRSA §961. Records the names of the two participating corporations, the name of the new resulting corporation, the plan-of-consolidation exhibit, the per-corporation method of adoption (member vote / written consent / board vote), the registered office of the new corporation, the optional future effective date, and dual signature blocks (with member-vote clerk certifications) for each participating corporation.

## Canonical fields

| Key | Type | Confidence | Notes |
|-----|------|-----------|-------|
| `consolidation.future_effective_date` | text | high | FIFTH: Effective date of the consolidation (if later than date of filing of Articles) is ___ (Not to exceed 60 days from date of filing of the Articles) |
| `consolidation.parties[0].name` | text | high | (A Maine Corporation) [first participating corporation name line at top of page] (fills multiple widgets) |
| `consolidation.parties[0].signature_block.date_signed` | text | high | DATED ___ [first signature block date] |
| `consolidation.parties[0].signature_block.signer_1.printed_name_and_capacity` | text | high | *By (signature) ___ / (type or print name and capacity) [first signature block, signer 1] |
| `consolidation.parties[0].signature_block.signer_2.printed_name_and_capacity` | text | high | *By (signature) ___ / (type or print name and capacity) [first signature block, signer 2] |
| `consolidation.parties[0].vote_method` | enum_select | high | [ ] By the members at a meeting on (date) ___ at which a quorum was present and such plan received at least a majority of the votes which members were entitled to cast. |
| `consolidation.parties[0].vote_method_date` | text | high | By the members at a meeting on (date) ___ [block 1 option 1 date] (fills multiple widgets) |
| `consolidation.parties[1].name` | text | high | AND / (A Maine Corporation) [second participating corporation name line] (fills multiple widgets) |
| `consolidation.parties[1].signature_block.date_signed` | text | high | DATED ___ [second signature block date] |
| `consolidation.parties[1].signature_block.signer_1.printed_name_and_capacity` | text | high | *By (signature) ___ / (type or print name and capacity) [second signature block, signer 1] |
| `consolidation.parties[1].signature_block.signer_2.printed_name_and_capacity` | text | high | *By (signature) ___ / (type or print name and capacity) [second signature block, signer 2] |
| `consolidation.parties[1].vote_method` | enum_select | high | Block 2 option 1: By the members at a meeting on (date)... |

_Showing 12 of 32 canonical keys — the full set is in mapping.json._

## Conditional logic

- entity.name (the new corporation resulting from consolidation) is non-empty and matches across fields 3, 4, and 24. (depends on `entity.name`)
- Both consolidation.parties[0].name and consolidation.parties[1].name are non-empty (the two existing corporations being consolidated). (depends on `consolidation.parties[0].name`, `consolidation.parties[1].name`)
- consolidation.plan_exhibit_letter is non-empty (SECOND requires a plan-of-consolidation exhibit). (depends on `consolidation.plan_exhibit_letter`)
- Each consolidation.parties[N] (N=0,1) has exactly one vote_method selected. (depends on `consolidation.parties[0].vote_method`, `consolidation.parties[1].vote_method`)
- If consolidation.parties[N].vote_method is set, consolidation.parties[N].vote_method_date must also be set (each option references a date). (depends on `consolidation.parties[0].vote_method`, `consolidation.parties[0].vote_method_date`, `consolidation.parties[1].vote_method`, `consolidation.parties[1].vote_method_date`)
- entity.registered_office.address is non-empty (FOURTH requires Maine registered-office address for the new corp). (depends on `entity.registered_office.address`)
- If consolidation.future_effective_date is set, it must be on or after filing.date_signed AND no later than filing.date_signed + 60 days (per 13-B MRSA cap noted on form). (depends on `consolidation.future_effective_date`)
- Each consolidation.parties[N] has at least signer_1.printed_name_and_capacity and date_signed populated; signer_2 may be empty unless the entity type requires two signers. (depends on `consolidation.parties[0].signature_block.signer_1.printed_name_and_capacity`, `consolidation.parties[0].signature_block.date_signed`, `consolidation.parties[1].signature_block.signer_1.printed_name_and_capacity`, `consolidation.parties[1].signature_block.date_signed`)

## Example case data

```json
{
  "consolidation": {
    "plan_exhibit_letter": "Sample Value",
    "parties": [
      {
        "name": "Sample Value",
        "vote_method": "majority_member_vote",
        "vote_method_date": "2026-01-15"
      },
      {
        "name": "Sample Value",
        "vote_method": "majority_member_vote",
        "vote_method_date": "2026-01-15"
      }
    ]
  },
  "entity": {
    "name": "Wabanaki Widgets, Inc."
  }
}
```
