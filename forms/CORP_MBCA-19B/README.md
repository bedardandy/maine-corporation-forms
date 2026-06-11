# CORP_MBCA-19B — Statement of Abandonment of Domestication (Domestic or Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 19  
**Filer role:** an officer or other duly authorized representative of the corporation per 13-C MRSA §926 (signs at bottom of page 0 — page-0 footnote: '*This document MUST be signed by an officer or other duly authorized representative.')

## Purpose

Abandon a pending domestication of a business corporation under 13-C MRSA §926. The form has two mutually-exclusive paths: (1) Domestic Business — abandons a charter-surrender filing (CORP_MBCA-19A) before its effective date, keeping the corporation's Maine domestic status; (2) Foreign Business — abandons an articles-of-domestication filing (CORP_MBCA-19) before it has become effective, keeping the corporation as foreign. Both paths require an officer's signature and result in the underlying domestication being treated as if never filed.

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
- Open question: DUAL-MODE entity-name slot: this form is filed in either direction (domestic or foreign), so the meaning of widget 19b1 depends on FIRST. For abandonment.path='domestic', 19b1 holds the Maine domestic name (entity.name). For abandonment.path='foreign', 19b1 holds the foreign home-jurisdiction name (semantically entity.home_jurisdiction_name on single-mode foreign forms like CORP_FICT-4 / LLC_MLLC-12 / CORP_MBCA-19). Mapped to entity.name uniformly per the CORP_CLKRA-3 dual-mode precedent. Synth and rubrics that need 'the entity's name' should reference filing.entities[0].name (the universal handle) rather than entity.name directly.
- Open question: The (signature of an officer or other duly authorized representative) line above 19b6 is wet-ink only — no AcroForm widget. Consistent with CORP_MBCA-19 / CORP_MBCA-19A / CORP_MBCA-11.
- Open question: 13-C MRSA §926 governs both abandonment paths. The form's SECOND paragraph — 'This statement takes effect upon filing, and the domestication is considered abandoned and does not become effective.' — is informational; no widget binds it.
- Open question: Page-1 widget IDs for the cover letter on this template diverge from the standard 'Check Box14/15/16' pattern (using 'hold', '24', 'imm' instead) and 'Name of entity' (using 'Name of entitys on the submitted filings 1' instead). Filler engine should accept multiple cover-letter naming conventions across template generations.
- Open question: The form-name parenthetical reads '(Name of Corporations)' (plural) on some renderings and '(Name of Corporation)' on others — a minor template typo. Single corporation per filing regardless.
