# NP_MNPCA-17 — Certificate of Correction (Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 25  
**Mapped fields:** 24  
**Filer role:** any duly authorized officer of the nonprofit corporation (per *footnote on page 1: 'This document MUST be signed by any duly authorized officer.' 13-B MRSA §104.1.B). Two *By signature slots provided; one is sufficient.

## Purpose

Correct an inaccuracy or defect in a previously filed document of a Maine nonprofit corporation (domestic or foreign) under 13-B MRSA §106.4. Identifies the original filing (date + document title), describes the error (THIRD), supplies the corrected text in its entirety (FOURTH), states the Maine registered office, and is signed by an authorized officer. The correction takes effect as of the original filing date except as to persons substantially and adversely affected.

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

- `registered_agent.physical_address` maps to 2 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: The form's preamble offers parallel parenthetical phrasings for domestic vs foreign filers — '(incorporated under the laws of the State of Maine)' vs '(incorporated under the laws of the State of ___)'. The unused parenthetical is conventionally struck through by the filer in pen, but the AcroForm has no widget to capture which option applies. Synth/rubric should infer domestic vs foreign by whether `entity.home_jurisdiction` is set, but the rendered PDF won't show the strike-through unless added at fill time.
- Open question: Drafter pass had page-1 widgets (Text8–Text11) off-by-one. Reviewer corrected via PyMuPDF text-block alignment. The systematic pattern across this batch suggests the drafter prompt should explicitly mention that the SIXTH/registered-office block typically uses an inline+continuation widget pair (Text7+Text8 here), then DATED+signer1+signer2 for the bottom — not DATED first.
- Open question: FIFTH (effective-date provision) is pre-printed legal text with no widget — it states that the correction takes effect as of the original filing date except as to substantially-and-adversely-affected persons. Synth doesn't populate FIFTH; rubric doesn't validate it.
