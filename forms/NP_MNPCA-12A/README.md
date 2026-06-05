# NP_MNPCA-12A — Amended Application for Authority to Carry on Activities (Foreign Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 32  
**Mapped fields:** 25  
**Filer role:** any duly authorized individual of the foreign nonprofit corporation (per *footnote on page 1: 'This document MUST be signed by any duly authorized individual.'). Single *By signature slot.

## Purpose

Amend an existing foreign nonprofit corporation's authority to carry on activities in Maine under 13-B MRSA §1207. Captures the home-jurisdiction name, original Maine authorization date, the proposed amendment text, optional name-change information (new home-jurisdiction name + date + fictitious-name election), updated activities/business purpose, and updated principal-office and Maine-registered-office addresses. Signed by any duly authorized individual.

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

- `amendment.description` maps to 2 widgets; all receive the same value.
- `entity.home_jurisdiction_name_new` maps to 2 widgets; all receive the same value.
- `entity.maine_business_purpose` maps to 3 widgets; all receive the same value.
- `registered_agent.physical_address` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Most body fields permit 'If no change, so indicate' as a literal value — the form treats unchanged sections explicitly rather than leaving them blank. Synth must produce a literal 'No change.' (or similar) string when amendment scope doesn't include that section, so rubrics that check non-emptiness still pass. Rubric required-checks should accept either real content or the literal 'no change' marker.
- Open question: FOURTH (name-change) is conditionally required: only populated when the home-jurisdiction name actually changed. The rubric `name-change-date-paired` enforces internal consistency but does NOT require these fields to be non-empty. Synth should toggle the FOURTH block on/off based on amendment scope.
- Open question: SEVENTH and EIGHTH each have inline+continuation widget pairs (12a14 alone for SEVENTH wide line; 12a15 inline + 12a16 wide for EIGHTH). Filler rule: write the full address into the widest widget; leave inline blanks empty unless the address is short.
