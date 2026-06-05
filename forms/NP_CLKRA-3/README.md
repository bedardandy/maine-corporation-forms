# NP_CLKRA-3 — Statement of Appointment or Change of Clerk or Registered Agent

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 33  
**Mapped fields:** 28  
**Filer role:** an officer or other authorized signer per the entity-type-specific footnotes; for nonprofits, an officer or director per 13-B MRSA

## Purpose

File a statement appointing a new clerk/registered agent or changing existing clerk/RA information (address, name) for a Maine domestic or foreign nonprofit corporation. The form template is shared with CORP_CLKRA-3 (multi-entity version) — the NP_ namespace tracks usage by the nonprofit category specifically; the form itself supports BC, NP, LLC, LP, LLP, and foreign variants.

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

- `clerk_change.action_type` maps to 2 widgets; all receive the same value.
- `clerk_change.modify_subtype` maps to 2 widgets; all receive the same value.
- `clerk_change.bc_authorization` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: This is the same form template as CORP_CLKRA-3 (and presumably LLC_CLKRA-3, LP_CLKRA-3 etc.) — the SOS publishes one PDF used across categories with conditional sections (SIXTH: BC-only, SEVENTH: foreign-only, EIGHTH: LP/LLP-only). The NP_ form_id namespaces by the entity category that consumes it; the canonical-key shape is identical to CORP_CLKRA-3 by design.
- Open question: For nonprofits specifically, the form has no nonprofit-only authorization recital (unlike SIXTH for BCs). Authorization is implicit in the filer being an officer/director per 13-B MRSA.
- Open question: filing.signer.title for a nonprofit filing should be a nonprofit-officer title (President, Vice President, Director, Clerk, Treasurer) — not 'Manager' (LLC) or 'General Partner' (LP). Synth and rubric should branch on the entity-type input.
