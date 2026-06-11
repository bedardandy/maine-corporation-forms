# CORP_MBCA-13A — Amended Annual Report (Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 24  
**Mapped fields:** 24  
**Filer role:** duly authorized officer or the clerk of the corporation (per 13-C MRSA §121.5 and the page-1 footnote enumerating who may sign by entity-status). Sister-form LP_MLPA-13A uses the per-officer general_partner pattern; MBCA-13A instead uses the standard single filing.signer block (Shape D — combined name and capacity).

## Purpose

File an amended annual report for a Maine domestic or foreign business corporation under 13-C MRSA §1623 to correct or update information previously filed on the current year's annual report. Captures the corporation's jurisdiction of incorporation (FIRST), the date of the original annual report being amended (SECOND), the substantive changes (THIRD, 4 inline lines + attachable additional pages), and the date the changes occurred (FOURTH). Per the * footnote on page 1: 'An amended annual report may be filed by the corporation to change information currently on file. The time for filing an amended annual report is from the date of the original filing until December 31st of that filing year.' Filing fee is $85 domestic / $150 foreign per the page-0 header.

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
- Open question: Field IDs are mostly the literal label text or 'undefined_N' (e.g., 'Name of Corporation', 'DATED', 'undefined_2'/'undefined_3'/'undefined_4' for the three unlabeled date/jurisdiction widgets). Preserved verbatim.
- Open question: MBCA-13A has 4 inline change-description lines vs. LP_MLPA-13A's 8 — the line count differs but the canonical-key family (amendment.changes_description.lineN) is shared.
- Open question: The page-0 'By ___ (authorized signature)' line itself has no AcroForm widget — only the 'type or print name and capacity' text widget binds. This is consistent with most SOS forms (the visible signature line is for a wet signature; the printed-name widget is the canonical-key anchor).
- Open question: Page-1 footnote enumerates who may sign by entity-status (e.g., authorized officer, clerk) but doesn't capture the role as a separate field. Capacity is captured inline within filing.signer.printed_name_and_capacity (Shape D).
