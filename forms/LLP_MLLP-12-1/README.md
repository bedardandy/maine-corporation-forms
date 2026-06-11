# LLP_MLLP-12-1 — Application for Authority to do Business (Foreign Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** (no body signature widget) — when this -1 variant is used standalone, the signing happens on the bundled primary filing or on a separately attached signature page. The non-suffixed MLLP-12 includes its own signature block. See open_questions.

## Purpose

Qualify a foreign Limited Liability Partnership (LLP) to transact business in Maine under 31 MRSA §852.3 (the '-1' variant of MLLP-12, which carries the body but does NOT include the standard signature block or cover letter — those are bundled when this form accompanies a primary filing). Captures home-jurisdiction name, optional professional-LLP election with services description, fictitious Maine name (with FICT-4 bundle indicator), home-jurisdiction date and place of organization, principal-office address, nature of Maine business, registered-agent appointment (commercial vs noncommercial), contact partner, and Maine-activities commencement date.

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
- Open question: **Template anomaly: no signature block widgets.** All 21 widgets are on pages 0–1 (body). The template lacks the (DATED, *By, signature, capacity) widgets that appear on the parent MLLP-12 and most other Maine SOS body forms. The '-1' suffix and the absence of signature widgets together suggest this is a partial/companion form intended to be bundled with another primary filing whose signature governs both. Synth fills can populate the body but cannot bind a body-side filing.signer.* — that key is undefined for this form. Recommend confirming with the parent MLLP-12 whether MLLP-12-1 is always bundled or if filers ever submit it standalone.
- Open question: **Template anomaly: no cover-letter widgets.** No page-2 cover letter exists on this template. Filings of MLLP-12-1 inherit the cover-letter primitive from the bundled primary filing (mirroring CORP_MBCA-6-1's bundled-with-merger pattern). The cover-letter canonical keys (filing.entities, filing.contact.*, filing.expedited_service, filing.attested_copy_recipient.*) are unbound for this form.
- Open question: Text4 (FOURTH professional-partners-licensed statement) is a free-text widget despite the label reading like a binary declaration. Consider whether a future redraft should split into entity.professional_partners_all_licensed (boolean) + entity.professional_partners_licensure_jurisdictions (text). Pass-1 keeps the single-string shape to match the widget.
- Open question: ELEVENTH paragraph (if it exists in the body — visible on the page render) requires an attached certificate of existence dated within 90 days; this is process-level (no widget). Same convention as LLP_MLLP-2's entity.certificate_of_existence_attached gap, but no widget binds it on this form.
