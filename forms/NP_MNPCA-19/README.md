# NP_MNPCA-19 — Articles of Domestication and Conversion (Foreign Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 20  
**Filer role:** an officer or other duly authorized representative of the foreign nonprofit corporation (signs the *By line at the bottom of page 0; widget captures '(type or print name and capacity)')

## Purpose

Domesticate and convert a foreign nonprofit corporation into a Maine nonprofit corporation. Records the foreign entity's name in its home jurisdiction, the proposed Maine name (if unavailable in foreign form), home jurisdiction, original incorporation date, attached new Articles of Incorporation exhibit (per FORM MBCA-6-1 reference in the template), and an optional future effective date. Page-0 header recites '13-C MRSA §942' but the page-0 banner is FOREIGN NONPROFIT CORPORATION — see open_questions: this is the same upstream template-text quirk seen on NP_MNPCA-19A (template appears forked from CORP_MBCA-19 without updating Title 13-C statutory references for the 13-B nonprofit equivalent).

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
- Open question: Page-0 header cites 'Pursuant to 13-C MRSA §942' but the page banner is FOREIGN NONPROFIT CORPORATION — 13-C is the Maine Business Corporation Act (for-profit), and nonprofit corporations are governed by 13-B MRSA. Same upstream template-text error pattern flagged on NP_MNPCA-19A: the template was likely forked from CORP_MBCA-19 without updating the statutory citation. Footer also cites '§942.1' for the signer requirement. Does not affect canonical-key mapping — flagged for upstream correction.
- Open question: THIRD paragraph references attaching 'Articles of Incorporation (MBCA-6-1)' — but MBCA-6-1 is the BC articles form. For a nonprofit domestication, the attached articles would conventionally be MNPCA-6-1 (the nonprofit equivalent). Same template-text fork issue as the §942 citation. Synth/assemble layer should treat the bundled form as MNPCA-6-1 even though the template names MBCA-6-1; flagged for upstream correction.
- Open question: filing.entities[1].name on the cover letter is likely populated with the bundled MNPCA-6-1 articles exhibit's entity for SOS routing. Cross-form bundling is also seen on NP_MNPCA-12 / CORP_MBCA-19 / CORP_MBCA-21 — a canonical filing.bundled_forms[] family is not yet defined.
- Open question: SECOND paragraph (authorization recital) has no widget and no opt-in checkbox — the recital is implicitly assumed by virtue of the foreign nonprofit signing and filing the articles. No rubric check beyond the form-level signature.
