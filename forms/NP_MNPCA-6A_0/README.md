# NP_MNPCA-6A_0 — Restated Articles of Incorporation (Domestic Nonprofit Corporation, alternate template)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 32  
**Mapped fields:** 25  
**Filer role:** duly authorized officer of the nonprofit corporation, and (when adopted by member vote) the clerk/secretary certifying custody of the minutes

## Purpose

File Restated Articles of Incorporation for an existing Maine domestic nonprofit corporation under 13-B MRSA §805. The full restated text MUST be attached as an exhibit (typically the contents of Form MNPCA-6-1, which the form footnote requires accompany this filing). The form records the adoption date and the adoption method (one of: members-at-meeting majority, members-at-meeting supermajority per articles, written consent of all entitled members, or board majority vote when there are no entitled members). It also captures the (possibly new) registered agent. This is the alternate template variant — uses a 'Filer Contact Cover Letter' (page 2) with C1-C12 widget naming and an additional 'List type of filing(s) enclosed' free-text block not present in the standard cover-letter primitive.

## Field mapping

This directory contains a machine-readable mapping between canonical data keys and the PDF's AcroForm widget names.

| File | Purpose |
|------|---------|
| `form.yaml` | Form metadata |
| `mapping.json` | canonical_key to widget mapping |
| `schema.json` | JSON Schema for fill data |
| `fields.csv` | Flat field inventory |
| `rubric.yaml` | Validation checks |
| `README.md` | This file |
| `SKILL.md` | Agent fill guidance |

## Known ambiguities

- `restatement.adoption_method` maps to 4 widgets; all receive the same value.
- `registered_agent.type` maps to 2 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Text17 (page 1) is a second **By signature block. The MUST-BE-COMPLETED-FOR-VOTE-OF-MEMBERS box on the same page asks the clerk/secretary to certify custody of the minutes — but that box has its own SEPARATE wet-ink-only signature line ('signature of clerk, secretary or asst. secretary') with no AcroForm widget. So Text17 is most likely a SECOND officer's signature block (forms with §1007/§805 sometimes require two officers), not the clerk attestation. Confirm by inspecting whether Text17 is conventionally filled separately from the clerk attestation when a member vote was used.
- Open question: Check Box10 (board-vote adoption method) is rendered visually below the SECOND registered-agent block rather than grouped with Check Box4/5/6 above. This appears intentional in the template to highlight the 'no members or none entitled to vote' precondition — synth/rubric should treat all four boxes (4, 5, 6, 10) as a single mutually-exclusive group despite the visual gap.
- Open question: The page-2 cover letter is the alternate 'Filer Contact Cover Letter' template (C1-C12 widget naming, includes the 'List type of filing(s) enclosed' free-text block, omits entity.annual_report_reminder_email). This differs from the standard cover-letter primitive used by the 15 prior pass-1 forms. Worth tracking which forms use which cover-letter variant for synth dispatch.
- Open question: Form footnote: '*Form MNPCA-6-1 MUST accompany this filing.' Synth/assemble layer must bundle MNPCA-6A_0 with MNPCA-6-1 and use the same restatement.text_exhibit_letter on both. The bundled-forms relationship is not yet captured in the schema.
