# NP_MNPCA-10A — Articles of Consolidation (Domestic Nonprofit Corporations)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 48  
**Mapped fields:** 32  
**Filer role:** an authorized officer of each of the two participating corporations signs in that corporation's signature block on page 1 (per 13-B MRSA §904); a clerk/secretary additionally certifies the member-vote action when applicable. Note: this form is structurally the consolidation analog of NP_MNPCA-10 (merger), with the key difference that consolidation produces a new entity (entity.name) rather than designating a survivor.

## Purpose

Consolidate two existing Maine domestic nonprofit corporations into a brand-new Maine nonprofit corporation under 13-B MRSA §904 or 13 MRSA §961. Records the names of the two participating corporations, the name of the new resulting corporation, the plan-of-consolidation exhibit, the per-corporation method of adoption (member vote / written consent / board vote), the registered office of the new corporation, the optional future effective date, and dual signature blocks (with member-vote clerk certifications) for each participating corporation.

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

- `consolidation.parties[0].name` maps to 2 widgets; all receive the same value.
- `consolidation.parties[1].name` maps to 2 widgets; all receive the same value.
- `entity.name` maps to 3 widgets; all receive the same value.
- `consolidation.parties[0].vote_method_date` maps to 4 widgets; all receive the same value.
- `consolidation.parties[1].vote_method_date` maps to 4 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: The 'MUST BE COMPLETED FOR VOTE OF MEMBERS' boxes on page 1 (one inset under each DATED row) have NO matching widgets in the AcroForm — only the outer signature widgets ('29'-'36') are bound. Visually each inset has a (name of corporation) line and a (signature of clerk, secretary or asst. secretary) line. These parallel the merger pattern's clerk_certification.* keys but are unbindable on this template. Likely a 2003-revision template bug analogous to the missing widgets on NP_MNPCA-10. Recommend an upstream pdftk dump_data_fields pass or a normalize_fields step to add the missing widgets; until then, a synth fill cannot populate the clerk-certification block via AcroForm.
- Open question: Template-level naming: most text widgets on this form use bare digit names ('1'-'6', '8', '10'-'36') instead of the 'TextN' prefix used on newer forms. Filler engine should accept both naming styles (same caveat as NP_MNPCA-10).
- Open question: FOURTH paragraph blank '24' is the new corp's name re-stated inline. Synth should populate it with the same value as entity.name to keep the recital consistent.
- Open question: FIFTH effective-date cap notes 'Not to exceed 60 days from date of filing of the Articles' — enforced by the future-effective-date-cap rubric.
- Open question: On a single-template form covering both '13-B MRSA §904' and the older '13 MRSA §961' citations, the field set is identical; the choice of statute is informational and does not change the canonical-key shape.
