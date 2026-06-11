# LLC_MLLC-13A — Amended Annual Report (Maine or Foreign LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 27  
**Mapped fields:** 27  
**Filer role:** person authorized by the LLC per 31 MRSA §1676.1B (page-1 footnote: 'this amended annual report MUST be signed by a person authorized by the limited liability company'). Form provides two parallel signer slots for cases where the LLC's operating agreement requires dual authorization; only one is statutorily mandated.

## Purpose

File an amended annual report for a Maine domestic or foreign LLC under 31 MRSA §1666 to correct or update information previously filed on the current year's annual report. Captures the LLC's jurisdiction of organization (FIRST), the date of the original annual report being amended (SECOND), the substantive changes (THIRD, 6 inline lines + attachable additional pages), and the date the changes occurred (FOURTH). Per the page-1 footnote: 'An amended annual report may be filed by the limited liability company to change information currently on file. The time for filing an amended annual report is from the date of the original filing until December 31st of that filing year.' Filing fee is $85 domestic / $150 foreign per the page-0 header. Two parallel authorized-person signer slots on page 1 (LLC sibling of CORP_MBCA-13A which has only one). 3 pages, 27 widgets.

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

- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: Drafter initially proposed entity.jurisdiction_of_organization, amendment.changes_description_N (with underscore), and amendment.effective_date_of_change; corrected during review to entity.home_jurisdiction, amendment.changes_description.lineN (dotted), and amendment.effective_date per existing CORP_MBCA-13A / LP_MLPA-13A precedent.
- Open question: MLLC-13A has 6 inline change-description lines vs. CORP_MBCA-13A's 4 and LP_MLPA-13A's 8 — line counts differ but the canonical-key family (amendment.changes_description.lineN) is shared. Synth concatenates a longer description across however many lines the form provides.
- Open question: The page-1 'By ___ (signature)' line itself has no AcroForm widget — only the 'type or print name and capacity' text widgets bind. Two parallel signer slots (filing.signer_1 and filing.signer_2) — the second is optional per §1676.1B.
- Open question: Sister-form CORP_MBCA-13A uses single Shape D signer (filing.signer.printed_name_and_capacity); MLLC-13A uses indexed multi-signer pattern (filing.signer_N.*) because the form provides 2 parallel slots. This is a deliberate departure from BC convention reflecting LLC operating-agreement flexibility (per LLC_MLLC-15 precedent).
- Open question: Page 0 has both a 'Filing Fee $85.00 for Maine; $150.00 for Foreign' header — synth must select the correct base fee from entity.home_jurisdiction. Foreign filings are $65 more expensive — confirmed against the form text.
