# MARK_mark6 — Voluntary Cancellation of Registration of Mark

**Entity type:** Trademark / Service Mark  
**Statute:** Maine Trademark Act (10 M.R.S. ch. 301-A)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 21  
**Filer role:** registrant or assignee of record (signs at bottom of page 1)

## Purpose

Voluntarily cancel an existing Maine trademark/service-mark registration under 10 MRSA §1527.1.B. Identifies the mark by charter number, text words, and design features, and is signed by the registrant or assignee of record.

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
- Open question: Form has no per-body 'applicant' / 'registrant' block — only the printed-name+capacity in Text7 and the cover-letter entity slot. Should mark6 carry a `mark.registrant.*` block analogous to MARK_mark1's `mark.applicant.*`, or is the registrant identity considered already-on-record (linked via charter_number) and the cover-letter row sufficient?
- Open question: Text2/Text3 (text words) and Text4/Text5 (design features) split into line1/line2 mirrors MARK_mark1; consistent with the convention that two-line free-form widgets keep both lines as separate canonical keys with a synth/rubric concatenation step.
- Open question: Mark cancellation can also be involuntary (e.g., SOS-initiated under 10 MRSA §1527.1.A); this form is the *voluntary* path only. A future mark6-involuntary form (if one exists) would have a different filer-role and likely different schema.
- Open question: Page 0 header reads 'Filing Fee $10.00' — confirm whether the rubric should treat this as a hard $10 base or accept a range (some Maine SOS divisions have raised mark fees over time; preserved as $10 advisory for now).
