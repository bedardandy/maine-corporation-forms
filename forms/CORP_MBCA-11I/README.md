# CORP_MBCA-11I — Articles of Dissolution (by Incorporators or Initial Directors)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 23  
**Mapped fields:** 20  
**Filer role:** a majority of the incorporators OR a majority of the initial directors (per the page-0 statutory recital and the form footer 'This document MUST be signed by a majority of the incorporators or initial directors'). Two inline signer slots — overflow when there are >2 signers is not addressed by the form template.

## Purpose

Dissolve a Maine domestic business corporation under 13-C MRSA §1401 by a majority of incorporators or initial directors — the early-dissolution path available when the corporation has not yet issued shares OR has not commenced business. Distinct from MBCA-11 (Articles of Dissolution under §1404, used after operations have begun). Captures entity name, the original incorporation-filing date, the dissolution-authorization date, optional future effective date, the FOURTH-recital basis (no shares issued OR not commenced business), and up to two signer slots.

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

- `dissolution.early_dissolution_basis` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Form provides only TWO inline signer slots (11l8, 11l9) but the footer requires 'a majority of the incorporators or initial directors'. If there are 3+ originators (e.g., 5 incorporators requiring a majority of 3), the form has no widget for the third signer. Likely captured via attached exhibit, but no exhibit-letter widget is bound on this form (unlike MBCA-6 which has entity.additional_incorporators_exhibit_letter for >5-incorporator overflow). Confirm whether §1401 contemplates this or whether the form is structurally limited to 2-signer scenarios.
- Open question: Could not locate a dedicated AcroForm signature widget on either signer line — only the printed-name-and-capacity widgets (11l8, 11l9) are bound. Signatures are wet-ink/image overlays, consistent with MBCA-11 / MLLP-6A.
- Open question: Form distinguishes 'Incorporator' (pre-issuance, named in articles) from 'Initial Director' (named in articles but corporation has issued shares) — both are valid signers under §1401 but for different statutory bases (no shares vs no business). Synth/rubric should pair: 'no_shares_issued' basis ↔ Incorporator capacity OR Initial Director capacity; 'not_commenced_business' basis ↔ Initial Director capacity (since incorporators are typically replaced by directors once shares issue, but §1401.2 still applies).
