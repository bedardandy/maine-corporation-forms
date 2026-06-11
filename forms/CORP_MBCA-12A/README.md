# CORP_MBCA-12A — Amended Application for Authority to Do Business (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 27  
**Mapped fields:** 27  
**Filer role:** duly authorized officer of the foreign corporation per 13-C MRSA §121.5 (page-1 footnote: '*This document MUST be signed by any duly authorized officer'). Single-signer Shape A — split widgets for printed name and title.

## Purpose

Amend a foreign business corporation's authority to do business in Maine under 13-C MRSA §1504. Records the entity's current name and current home jurisdiction (FIRST recital — used to identify the existing SOS record), the date the corporation was originally authorized in Maine (SECOND recital), then captures any of: a new corporate name (THIRD; with optional fictitious name + FICT-4 attachment), a new principal-office address (FOURTH), or a new home jurisdiction (FIFTH; requires an attached certificate of existence dated within 90 days). Filing fee $76 base, $35 if amending ONLY Item FOURTH (principal-office address). 3 pages, 28 widgets.

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
- Open question: Drafter collapsed the on-record recitals (Text1 'Name of Corporation' top-of-form, Text2 'jurisdiction currently appearing on the record') and the new/effective values (Text4 THIRD new name, Text8 FIFTH new jurisdiction) into single keys (entity.home_jurisdiction_name, entity.home_jurisdiction). On amendment forms these are genuinely two distinct values — reviewer split them with new schema-gap keys entity.home_jurisdiction_name_on_record and entity.home_jurisdiction_on_record. Synth fills the on-record keys with current data and the canonical keys with post-amendment data.
- Open question: Drafter swapped page-1 widget assignments: claimed Text9=DATED, Text10=printed_name, Text11=title. By widget rect, Text11 (left, y=748–768) is DATED, Text9 (right, y=716–736) is the printed-name line, and Text10 (right, y=684–703) is the title line. Reviewer corrected.
- Open question: Form is a single-form amendment-of-authority — Shape A (split printed_name + title) per page-1 layout, distinct from the parent CORP_MBCA-12 which uses Shape D (combined printed_name_and_capacity). The two captions on MBCA-12A page 1 — '(type or print name)' and '(title of signer)' — confirm Shape A; same convention as CORP_FICT-4 and CORP_CLKRA-3.
- Open question: filing.certificate_of_existence_attached is a new schema-gap key. Earlier foreign-entity forms require a COE attachment but do not provide a form-level checkbox (rubric tracks via filing.notes). MBCA-12A introduces an explicit attestation checkbox (Check Box2 at rect y≈97), making the attachment requirement enforceable from form fields. Synth must set this true whenever entity.home_jurisdiction has changed.
- Open question: Drafter populated schema_gaps with many existing canonical keys (entity.home_jurisdiction_name, entity.home_jurisdiction, entity.maine_authorization_date, entity.maine_fictitious_name, filing.fict4_accompanies, entity.principal_office.physical_address, entity.principal_office.mailing_address, filing.date_signed, filing.signer.printed_name, filing.signer.title). All removed in this review — schema_gaps now contains only genuinely-novel keys.
