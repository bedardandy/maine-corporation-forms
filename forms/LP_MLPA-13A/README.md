# LP_MLPA-13A — Amended Annual Report (Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 30  
**Mapped fields:** 30  
**Filer role:** at least one general partner of the LP per 31 MRSA §1324.1.J (individual or authorized representative of an entity GP, signs on page 1)

## Purpose

File an amended annual report for a Maine domestic or foreign limited partnership under 31 MRSA §1330.2 to correct or update information previously filed on the current year's annual report. Captures the LP's home jurisdiction (FIRST), the date of the original annual report being amended (SECOND), the substantive changes (THIRD, 8 inline lines + attachable additional pages), and the date the changes occurred (FOURTH). Per the * footnote on page 1: 'An amended annual report may be filed by the limited partnership to change information currently on file. The time for filing an amended annual report is from the date of the original filing until December 31st of that filing year.'

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
- Open question: Field IDs are mostly the literal label text (e.g., 'Name of Limited Partnership', 'Dated', 'type or print name') rather than 'TextN'. The two unlabeled date widgets and the jurisdiction widget got auto-named 'undefined_2', 'undefined_3', 'undefined_4' — preserved verbatim.
- Open question: No filing-fee callout is visible in the page-0 header on this form (unlike most SOS forms which carry a 'Filing Fee $XX' box). The cover-letter still asks for total fees enclosed; rubric does not currently enforce a specific base fee for this form.
- Open question: Page 1 has only one inline individual-signer slot — matches the §1324.1.J one-signer requirement and parallels MLPA-12A/12B/17.
- Open question: amendment.changes_description.lineN reuses the line-indexed multi-line shape established by upstream amendment.nature_and_text.lineN (NP_MNP-9). Considered using the same key (amendment.nature_and_text) but the form's own label is 'The information has changed as follows', which is a different semantic (delta description vs. amendment text), so a separate key keyed to 'changes_description' is more faithful.
