# NP_MNP-6 — Certificate of Organization (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 52  
**Mapped fields:** 49  
**Filer role:** incorporator(s) — natural persons. Per page-1 footnote ('Pursuant to 13 MRSA §901, at least 3 incorporators are required'), the form requires ≥3 incorporator signatures.

## Purpose

Form a Maine domestic nonprofit corporation under 13 MRSA §903 (older 'MNP-' prefixed form, predecessor to NP_MNPCA-6 under 13-B MRSA). Captures entity name (FIRST), public-benefit vs mutual-benefit selection with a free-text purpose block (THIRD, two parallel checkboxes plus two free-text blocks), municipality + county location (FOURTH), four named officer slots — President / Vice-President / Secretary or Clerk / Treasurer (FIFTH) plus an officer count, three directors/trustees (SIXTH), an entity-level contact person with mailing + physical address (SEVENTH), the signature/dating block, and up to ~6 individual incorporator rows (each with printed name, street, city/state/zip — wet-ink signatures). Filing fee is $5 per the page-0 header. 3 pages, 51 widgets. Distinct from NP_MNPCA-6 in that this older form has no registered-agent block, no member-class election, and no 501(c) opt-ins; instead it has the named officer roster + entity-contact-person block.

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
- 1 low-confidence mapping(s) need human review: `incorporator_7.address.street`
- Open question: WIDGET-COUNT MISMATCH ON PAGE 1 INCORPORATOR BLOCK: widget data shows 20 widgets in 10 evenly-spaced rows (y=445, 411, 377, 343, 311, 275, 243, 209, 175, 141), each row having both a left-column and right-column widget. The visual form layout shows 6 incorporator slots × 2 lines each (signature wet-ink + print name on left; Street + city/state/zip on right) = 12 rows × ~3 widgets per incorporator = 18 widgets, plus Dated = 19 widgets. The drafter's interpretation maps Text19 (Dated) plus 6 incorporators (Text20-Text37 as 6 × 3 widgets) plus Text38 as a possible 7th-slot Street. Pass-2 visual-fill testing needed to confirm the row pairing — synth should populate 6 incorporators and verify which fields render where. The medium-confidence rationales on Text20-Text38 reflect this open question.
- Open question: Form pre-dates the registered-agent regime (13 MRSA §903 vs the modern 13-B MRSA §403). Synth and rubric for this form should NOT populate registered_agent.* keys; the location/agency function is satisfied by entity.location.* and entity.contact_person.*.
- Open question: The 'MNP-' prefix coexists with the modern 'MNPCA-' prefix in the SOS template lineage (MNP-3, MNP-6, MNP-9 all under the older 13 MRSA; MNPCA-6, MNPCA-10, MNPCA-12 under modern 13-B MRSA). Document the dual-prefix lineage in synth so that filers picking 'nonprofit formation' get the right modern form (MNPCA-6) by default unless they specifically need the legacy MNP-6 version.
- Open question: SECOND recital (anti-inurement statement) has no widget — it is a representation by the corporation, not a captured field. No rubric check needed.
- Open question: The 'Secretary or Clerk' role is a single named slot (entity.officers.secretary_or_clerk.name) — the form combines the two terms because 13 MRSA's terminology was less consistent than modern 13-B MRSA's distinction between Secretary (officer) and Clerk (statutory agent). Synth populates one name string for whichever applies.
- Open question: Drafter initially proposed entity.benefit_type and a unified entity.purpose_statement; corrected to entity.nonprofit_type and the split entity.public_benefit_purpose / entity.mutual_benefit_purpose during review per NP_MNPCA-6 precedent.
