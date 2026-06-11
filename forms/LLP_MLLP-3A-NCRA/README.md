# LLP_MLLP-3A-NCRA — Statement of Resignation of Noncommercial Registered Agent (Maine Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 22  
**Filer role:** the noncommercial registered agent who is resigning (signs the lower half of page 0 over the '(signature of noncommercial registered agent)' caption)

## Purpose

File a statement of resignation by the noncommercial registered agent currently appearing on the Maine SOS record for a Maine Limited Liability Partnership, pursuant to 5 MRSA §111. The agent attests to their identity and address as on record (FIRST), names a person at the LLP to whom the SOS-required notice of resignation will be sent (SECOND), and signs the statement. The agent's appointment terminates 31 days after this statement is delivered to the LLP. Filing fee is $35 per the page-0 header. 2 pages, 22 widgets. LLP sibling of CORP_MBCA-3A-NCRA / CORP_MBCA-12E-NCRA / LLC_MLLC-3A-NCRA — identical body structure, differs only in entity-type heading and signer-block label.

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
- Open question: Drafter initially proposed resigning_agent.* and notification_recipient.* namespaces; corrected during review to reuse the existing registered_agent.* and resignation_notice.* keys per MBCA-3A-NCRA / MBCA-12E-NCRA / MLLC-3A-NCRA precedent. The 5 MRSA §111 statute applies uniformly to noncommercial-RA resignations across entity types — no need for entity-type-specific namespaces.
- Open question: Page 0 has no explicit signature-image widget separate from Text9. Text9 sits below the '(signature of noncommercial registered agent)' caption with its own '(type or print name)' caption, suggesting it captures only the typed/printed name; the actual signature is presumably handwritten or applied as an image after print, not via an AcroForm field. Same convention as the MBCA-3A-NCRA / MLLC-3A-NCRA family.
- Open question: The 'NCRA' suffix on the form_id is a convention shared with MBCA-3A-NCRA, MBCA-12E-NCRA, and MLLC-3A-NCRA — synth/rubric should treat *_NCRA forms as the noncommercial-agent-resignation family, with body-structure variations confined to entity-type heading and signer-block caption.
- Open question: 13-C MRSA does not directly govern LLPs (which are organized under 31 MRSA chapter 21); the resignation procedure is uniformly governed by 5 MRSA §111 regardless of entity type.
