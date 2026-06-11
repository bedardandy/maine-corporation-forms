# NP_MNPCA-10E — Articles of Consolidation (Domestic and Foreign Nonprofit Corporations)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 49  
**Mapped fields:** 37  
**Filer role:** duly authorized officer of each participating corporation signs in that corporation's signature block on page 1 (per 13-B MRSA §906); a clerk/secretary additionally certifies the member-vote action when applicable (the 'MUST BE COMPLETED FOR VOTE OF MEMBERS' inset block on page 1)

## Purpose

Consolidate two or more existing nonprofit corporations (domestic and/or foreign) into a single NEW nonprofit corporation under 13-B MRSA §906. Distinct from a merger (which produces a survivor): consolidation produces a brand-new entity. Records the names + descriptors of participating corps, the new consolidated entity, the plan-of-consolidation exhibit, per-domestic-party adoption manner (4 mutually-exclusive vote/consent options each with date), registered-office addresses for each party, optional future effective date, and dual signature blocks with member-vote clerk certifications.

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

- `consolidation.parties[0].name` maps to 3 widgets; all receive the same value.
- `consolidation.parties[1].name` maps to 2 widgets; all receive the same value.
- `consolidation.new_entity.name` maps to 2 widgets; all receive the same value.
- `consolidation.parties[0].adoption_method` maps to 4 widgets; all receive the same value.
- `consolidation.parties[0].adoption_date` maps to 4 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- 2 low-confidence mapping(s) need human review: `consolidation.parties[0].signature_block.signature`, `consolidation.parties[1].signature_block.signature`
- Open question: Template gap: the 'MUST BE COMPLETED FOR VOTE OF MEMBERS' inset block on page 1 (between the two signer blocks) contains visible '(name of corporation)' and '(signature of clerk, secretary or asst. secretary)' lines, but widgets.json has NO AcroForm widgets for these. Likely a 2006-revision template bug — parallel to the missing MNPCA-10 clerk-cert widgets noted in schema-gaps/2026-04-30-phase2-summary.md. The clerk certification is required when adoption_method ∈ {majority_member_vote, supermajority_member_vote, written_consent_of_members}; not required for board_of_directors_majority_vote. Filer must complete by hand. Recommend upstream fix.
- Open question: Template gap: the option-2 percentage blank ('the percentage of votes ___ of the members required by the Articles of Incorporation') is visible on page 0 as an inline underlined blank but has no AcroForm widget. Field 18 was previously ambiguous but is resolved to option-3 written-consent date by y-proximity (Check Box11 y=122, field 18 y=115). The option-2 percentage must be hand-written. Recommend upstream fix.
- Open question: Template-naming variant: the cover-letter expedite checkboxes use bare digit-style field-ids ('hold', '24h', 'imm') instead of the conventional 'Check Box14/15/16' naming used on most other forms (e.g., MBCA-6, MNPCA-10). Filling engine should accept both naming styles per cover-letter-primitive.md aliases. Similarly, page-2 entity-name fields use 'Name of entitys on the submitted filings 1' (with typo 'entitys' and trailing index) rather than the conventional 'Name of entity'.
- Open question: Form layout supports only ONE FOURTH adoption-manner block inline (for the domestic participating corp). Multi-party-domestic consolidations require attached exhibits for each additional domestic party's adoption manner. Synth fixture should populate consolidation.parties[0].adoption_* and document additional parties in exhibits.
- Open question: Per the form's bottom note: 'If a domestic corporation is the result of this consolidation, THIS FORM MUST BE ACCOMPANIED BY FORM MNPCA-18 (Acceptance of Appointment as Registered Agent §204.3.).' This is a conditional bundling requirement when consolidation.new_entity.governing_law_state='Maine'. Tracked as a multi-form bundle hint but not a per-widget mapping concern. **MNPCA-18 is not published by the Secretary of State** (verified 2026-06-11: the official nonprofit forms listing goes MNPCA-17 → MNPCA-19, and the file host 404s for mnpca18.pdf), so this repo cannot carry it — the note is stale upstream text from this form's 8/2006 revision. See docs/upstream-worklist.md.
