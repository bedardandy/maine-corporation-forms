# NP_MLC-3_0 — Change of Clerk and/or Address (Domestic Nonprofit Corporation / Independent Local Church)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 30  
**Mapped fields:** 22  
**Filer role:** the clerk OR another duly authorized officer of the corporation (per the page-1 footnote: 'This document MUST be signed by the clerk or other duly authorized officer'). Form provides two parallel signer slots; only one is statutorily required.

## Purpose

Update the registered clerk and/or address of record for a Maine domestic nonprofit corporation or independent local church under 13 MRSA §3025. The FIRST election picks among four mutually-exclusive change types (A: change of address only; B: change of clerk and address; C: change of clerk only; D: change in name of current clerk). SECOND recites the clerk currently on record (name + address). THIRD captures the new information per the FIRST election. Filing fee is $5.00 per the page-0 header — markedly cheaper than CLKRA-3 ($35) because §3025 governs church/nonprofit clerk changes specifically. 3 pages, 28 widgets. Sister-form NP_CLKRA-3 (multi-entity Statement of Appointment or Change of Clerk/RA) covers the broader §1604 case; MLC-3 is the §3025 narrow case for churches and small nonprofits.

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

- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Drafter initially proposed clerk_current.* and clerk_new.* namespaces; corrected during review to reuse the existing clerk_change.* namespace per NP_CLKRA-3 / CORP_CLKRA-3 precedent. Two new keys added to clerk_change.* (clerk_change.change_type and clerk_change.current_clerk_or_agent_address) — the former because MLC-3's enum differs from CLKRA-3's, the latter because MLC-3 captures the current clerk's address (which CLKRA-3 doesn't).
- Open question: FIRST caption reads ('X all boxes that apply') but the four options are semantically mutually exclusive (option B already covers the union of A and C). Synth/rubric treat the four checkboxes as a single radio-style enum. If a real filing checks multiple, the SOS likely treats the most-inclusive option (B) as canonical.
- Open question: Form_id has unusual '_0' suffix (NP_MLC-3_0). Believed to be a revision suffix for the first/canonical version of MLC-3; a future MLC-3_1 revision could appear if the form is amended. Preserve verbatim in DB and downstream tooling.
- Open question: Page-1 has only DATED + 2 signer-printed-name widgets — the visible '*By ___' signature lines are wet-ink-only with no AcroForm binding (same convention as MBCA-14, MBCA-14A, MLLC-13A).
- Open question: The §3025 statute scope is narrower than the §1604 generic clerk/RA change (which CLKRA-3 covers). MLC-3 is for nonprofit corporations + independent local churches only; for general nonprofits using a CRA, NP_CLKRA-3 is the right form.
