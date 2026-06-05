# LLC_MLLC-12A — Statement of Change of Foreign Qualification

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 31  
**Mapped fields:** 28  
**Filer role:** authorized signatory of the foreign LLC (signs at bottom of page 1). Single-signer Shape B — printed name only (no separate title field on this form).

## Purpose

Update the Secretary of State's records for a foreign limited liability company already authorized in Maine, per 31 MRSA §1622.3 / §1632. Captures changes to the entity's home-jurisdiction name (FIRST), Maine fictitious name (SECOND), original Maine qualification date (THIRD, recital-only), nature of business (FOURTH), principal-office address (FIFTH), registered agent (SIXTH), home jurisdiction (EIGHTH), and any other changes via an attached exhibit (NINTH). A certificate of existence (or equivalent), dated within 90 days of delivery, must accompany the filing. 3 pages, 33 widgets.

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

- `registered_agent.name` maps to 2 widgets; all receive the same value.
- Open question: FIRST's 'proposed name to be used in this State' is keyed to entity.maine_assumed_name_for_suffix despite the change-form trigger differing from MLLC-12's suffix-compliance trigger. Both forms use the slot to capture the Maine-side name to use going forward; broadening the key's semantics is preferred over inventing a parallel entity.proposed_maine_name_after_home_change key. Synth may emit '(no change)' literal when the home name is unchanged, per the parenthetical instruction.
- Open question: THIRD's 'date qualified in Maine' is keyed to the existing entity.maine_authorization_date (defined in CORP_MBCA-12B). The terminology differs across statutes — 13-C MRSA uses 'authorized'; 31 MRSA uses 'qualified' — but both name the same Maine-side anniversary, so reusing one canonical key is preferred.
- Open question: Three unnamed /Btn checkboxes (FICT-4-accompanies on page 0, SIXTH-Commercial on page 1, two of three expedite-service boxes on page 2) lack /T names and must be bound by index or rect. Pattern is the same as MBCA-10's six unnamed election checkboxes — filler engine should already accept rect-binding from that form's handling.
- Open question: Drafter initially proposed two new schema-gap keys (entity.maine_qualification_date, filing.other_changes_exhibit_letter); both are removed in this review — the date concept reuses entity.maine_authorization_date, and the exhibit-letter reuses filing.other_amendments_exhibit_letter (LP_MLPA-12A precedent). No new canonical keys are required for this form.
