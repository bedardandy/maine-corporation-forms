# CORP_MBCA-20A — Articles of Charter Surrender (Upon Nonprofit Conversion)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 20  
**Filer role:** officer or other duly authorized representative of the domestic business corporation (per the page-0 footnote and 13-C MRSA §934.1)

## Purpose

Surrender the Maine charter of a domestic business corporation when it converts to a FOREIGN nonprofit corporation under 13-C MRSA §§934 and 935. The filing records the effective date of the foreign conversion (FIRST), recites shareholder approval (SECOND, no widget), identifies the new (non-Maine) jurisdiction of incorporation (THIRD), appoints the Secretary of State as agent for service of process re shareholder appraisal rights and provides a forwarding mailing address (FOURTH), and recites the surviving entity's obligation to pay appraisal-rights amounts under chapter 13 (FIFTH, no widget). Filing fee is $90 per the page-0 header. 2 pages, 20 widgets.

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
- Open question: FIFTH (chapter-13 appraisal-rights payment recital) has no widget — it is a representation by the corporation, not a captured field. No rubric check beyond signature.
- Open question: SECOND (shareholder-approval recital) has no widget and no opt-in checkbox — implicit by virtue of the corporation filing. Same convention as MBCA-20 / MBCA-21.
- Open question: Form has no widget for the actual signature line — only the typed-name-and-capacity widget. Wet-ink only (same convention as MBCA-13A and other Shape-D forms).
- Open question: filing.entities[1].name on the cover letter is unlikely to be populated for charter surrender (no bundled formation form — the new entity is being formed in another jurisdiction, not in Maine).
- Open question: conversion.new_jurisdiction is the FIRST observed instance of an outbound jurisdiction key. If subsequent forms (e.g., outbound LLC conversion, cross-form mergers) reuse this key, consider promoting it to a documented schema-gap convention.
