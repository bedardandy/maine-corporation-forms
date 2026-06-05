# CORP_MBCA-3A-NCRA — Statement of Resignation of Noncommercial Clerk (Domestic Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 20  
**Filer role:** the noncommercial clerk who is resigning (signs the lower half of page 0 over the '(signature of noncommercial clerk)' caption)

## Purpose

File a statement of resignation by the noncommercial clerk currently appearing on the Maine SOS record for a Maine domestic business corporation, pursuant to 5 MRSA §111. The clerk attests to their identity and address as on record (FIRST), names a corporate officer to whom the SOS-required notice of resignation will be sent (SECOND), dates and signs the statement. The clerk's appointment terminates 31 days after this filing is delivered to the corporation. Filing fee is $35 per the page-0 header. 2 pages, 22 widgets. Domestic-BC sibling of CORP_MBCA-12E-NCRA (foreign-BC variant) and LLC_MLLC-3A-NCRA — identical body structure, differs only in entity-type heading. 'Clerk' here is the legacy 13-C MRSA term for what newer entity statutes call 'registered agent'; canonical keys reuse the registered_agent.* namespace per the MBCA-12E-NCRA / MLLC-3A-NCRA precedent so synth/rubric authors do not have to disambiguate clerk vs RA.

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
- Open question: Drafter initially proposed resigning_clerk.* and notice_recipient.* namespaces; corrected during review to reuse the existing registered_agent.* and resignation_notice.* keys per MBCA-12E-NCRA / MLLC-3A-NCRA precedent. The 5 MRSA §111 statute applies uniformly to corporate-clerk and registered-agent resignations across entity types — no need for entity-type-specific namespaces.
- Open question: Page 0 has no explicit signature-image widget separate from Text8. Text8 sits below the '(signature of noncommercial clerk)' caption with its own '(type or print name)' caption, suggesting it captures only the typed/printed name; the actual signature is presumably handwritten or applied as an image after print, not via an AcroForm field. Same convention as MBCA-12E-NCRA / MLLC-3A-NCRA.
- Open question: The 'NCRA' suffix on the form_id is a convention shared with MBCA-12E-NCRA and MLLC-3A-NCRA — synth/rubric should treat *_NCRA forms as the noncommercial-clerk/RA-resignation family, with body-structure variations confined to entity-type heading and signer-block caption.
