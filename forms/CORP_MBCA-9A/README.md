# CORP_MBCA-9A — Articles of Amendment (Reorganization ordered or decreed by a court)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** individual(s) designated by the court (page-0 footer: 'This document MUST be signed by the individual or individuals designated by the court'). Multi-signer pattern using filing.signer.* and filing.signer_2.* — both Shape D (printed name + capacity combined).

## Purpose

File Articles of Amendment for a Maine domestic business corporation when the amendment is ordered or decreed by a court (typically a Chapter 11 bankruptcy reorganization) under 13-C MRSA §1008. The signer is an individual designated by the court — not a corporate officer — and shareholder approval is not required because the court's order substitutes for the usual approval mechanism. The form supports up to two parallel court-designated signers.

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
- Open question: The form has two parallel '*By ___' signer blocks (9a6 and 9a7) without explicit numbering on the form itself. Some court orders designate a single individual; others designate two (e.g., a trustee and a co-trustee). The second slot is optional, hence the at-least-one-signer rubric rather than both-required.
- Open question: No widgets capture the court's case number separately — case number, court name, and case caption all collapse into amendment.reorganization_proceeding_title (single widget 9a4). If a future form (e.g., a non-bankruptcy court-ordered amendment) splits these, additional keys (amendment.court_case_number, amendment.court_name) could be added without breaking this convention.
- Open question: MBCA-9A is the court-ordered variant of MBCA-9 (standard Articles of Amendment). The two forms differ in: (1) signer pattern — MBCA-9 uses a corporate-officer signer with shareholder-vote recital, MBCA-9A uses court-designated individual(s); (2) exhibit reference — both have an exhibit-letter pattern; (3) statutory authority — MBCA-9 is §1006/§1007, MBCA-9A is §1008. Synth should not conflate the two.
