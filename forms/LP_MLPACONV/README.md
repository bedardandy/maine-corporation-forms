# LP_MLPACONV — Articles of Conversion (Maine Limited Partnership → Other Type of Organization)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 32  
**Mapped fields:** 31  
**Filer role:** EACH general partner listed in the certificate of limited partnership (per recital on page 1 — 31 MRSA §1324 requires all GPs to sign)

## Purpose

Convert a Maine Limited Partnership into another type of organization under 31 MRSA §1324 and §1432 (per the recital text on page 1 referencing the Maine LP statute). Records the converting LP's name/form/jurisdiction/formation date, the resulting (post-conversion) organization's name/form/jurisdiction/formation date/principal-office address, the effective date of conversion, an optional foreign-survivor service-of-process address, an attached organizing-document exhibit (or election that no filing is required), and the signature of each general partner.

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

- `conversion.result_type` binds as a single enum_select selecting among 2 option widgets (accepted values: filing_required, no_filing_required).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: The recital on page 1 cites '31 MRSA §1324' (Maine LP statute) while the form metadata title cites '§1432'. Both statutes pertain to LP conversion in Maine's chapter on LPs (Chapter 19); the recital is authoritative. Synth/rubric should treat entity.governing_statute_jurisdiction as effectively always 'Maine' on this form unless the form is reused in a context not yet observed.
- Open question: The form has only 2 GP signature slots inline. If the LP has more than 2 GPs, the recital ('signed by each general partner') still requires all signatures — overflow goes on attached pages with no exhibit-letter widget. Synth must either truncate at 2 GPs or attach an addendum out of form.
- Open question: conversion.effective_date (required) vs MBCA-21's conversion.future_effective_date (optional 'if other than the date of filing') is a real semantic split. A future review may decide to unify under conversion.effective_date with an 'is_future' flag, but the current two-key approach preserves widget-shape fidelity per the documented L3-references-not-L2 rule.
- Open question: conversion.new_entity_organizing_document_exhibit_letter (this form) vs conversion.new_entity_provisions_exhibit_letter (MBCA-21) is a real semantic split (whole document vs required-provisions subset). Keep separate.
