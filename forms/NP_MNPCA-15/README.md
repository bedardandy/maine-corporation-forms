# NP_MNPCA-15 — Application for the Use of an Indistinguishable Name (Nonprofit)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 20  
**Filer role:** any duly authorized officer of the consenting nonprofit corporation (per *footnote: 'This document MUST be signed by any duly authorized officer.' 13-B MRSA §104.1.B). Two *By signature slots provided; one is sufficient.

## Purpose

Existing Maine nonprofit corporation consents to allow another entity (the 'requestor') to use a name that is indistinguishable from the consenting corporation's current name, pursuant to 13-B MRSA §301-A.4. The consenting corporation simultaneously commits to change its own name to a distinguishable name. Captures: consenting entity name, the indistinguishable name being consented to, the requestor entity name, the consenting entity's new (distinguishable) name, and the consenting entity's Maine registered office.

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
- Open question: Form footnote: '*This application must be accompanied by the applicable form to change its name as provided in Item Third.' Synth/rubric should track that a name-change filing (e.g., MNPCA-1A or similar) bundles with this consent — this consent alone is insufficient. Could be modeled as `filing.accompanying_name_change_form` boolean or similar; not surfaced as an AcroForm widget here.
- Open question: Drafter pass had this form's body widgets off-by-one (mapped widget 2 as requestor instead of the indistinguishable name itself, etc.). Reviewer corrected via PyMuPDF text-block alignment with widget rects. Future drafter prompts should encourage matching widget rects to text-block y-coordinates explicitly to catch off-by-one errors before review.
- Open question: Is the requestor entity always a Maine entity, or could it be a foreign entity seeking Maine qualification? Form text doesn't constrain — `indistinguishable_name.requestor_name` accepts any free-text name and synth need not validate jurisdiction.
