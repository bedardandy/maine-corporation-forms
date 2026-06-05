# NP_MNPCA-3A-NCRA — Statement of Resignation of Noncommercial Registered Agent (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 20  
**Filer role:** the noncommercial registered agent who is resigning (signs the lower half of page 0 over the '(signature of noncommercial registered agent)' caption)

## Purpose

File a statement of resignation by the noncommercial registered agent currently appearing on the Maine SOS record for a Maine domestic nonprofit corporation, pursuant to 5 MRSA §111. The agent attests to identity and address as on record (FIRST), names a corporate officer to whom the SOS-required notice of resignation will be sent (SECOND), dates and signs the statement. The agent's appointment terminates 31 days after this filing is delivered to the corporation. Nonprofit sibling of CORP_MBCA-3A-NCRA / CORP_MBCA-12E-NCRA / LLC_MLLC-3A-NCRA — identical body structure, differs only in entity-type heading. Canonical keys reuse the registered_agent.* and resignation_notice.* namespaces per the NCRA-family precedent so synth/rubric authors do not have to disambiguate by entity type.

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
- Open question: Drafter initially proposed resigning_agent.* and notice_recipient.* namespaces; corrected during review to reuse the existing registered_agent.* and resignation_notice.* keys per the NCRA-family precedent (MBCA-3A-NCRA / MBCA-12E-NCRA / MLLC-3A-NCRA). The 5 MRSA §111 statute applies uniformly to noncommercial-RA resignations across entity types — no need for entity-type-specific namespaces.
- Open question: Page 0 has no explicit signature-image widget separate from Text8. Text8 sits below the '(signature of noncommercial registered agent)' caption with its own '(type or print name)' caption, suggesting it captures only the typed/printed name; the actual signature is presumably handwritten or applied as an image after print, not via an AcroForm field. Same convention as the rest of the NCRA family.
- Open question: The 'NCRA' suffix on the form_id places this form in the noncommercial-RA-resignation family — synth/rubric should treat *_NCRA forms as a single family, with body-structure variations confined to entity-type heading and signer-block caption.
