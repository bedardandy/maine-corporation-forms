# LP_MLPA-3A-NCRA — Statement of Resignation of Noncommercial Registered Agent (Domestic Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 22  
**Filer role:** the noncommercial registered agent who is resigning (signs the lower half of page 0 over the '(signature of noncommercial registered agent)' caption)

## Purpose

File a statement of resignation by the noncommercial registered agent currently appearing on the Maine SOS record for a Maine domestic limited partnership, pursuant to 5 MRSA §111. The agent attests to their identity and address as on record (FIRST), names a person at the LP to whom the §111-required notice of resignation will be sent (SECOND), and dates and signs the statement. The agent's appointment terminates 31 days after this filing is delivered to the LP. Filing fee is $35 per the page-0 header. 2 pages, 22 widgets. LP sibling of CORP_MBCA-3A-NCRA, CORP_MBCA-12E-NCRA, and LLC_MLLC-3A-NCRA — identical body structure, differs only in entity-type heading and the notice-recipient title caption (LPs have general partners, not corporate officers).

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
- Open question: Drafter initially proposed resigning_agent.* and resignation_notice_recipient.* namespaces; corrected during review to reuse the existing registered_agent.* and resignation_notice.* keys per the NCRA family precedent (CORP_MBCA-3A-NCRA, CORP_MBCA-12E-NCRA, LLC_MLLC-3A-NCRA). The 5 MRSA §111 statute applies uniformly to corporate-clerk and registered-agent resignations across entity types.
- Open question: Page 0 has no explicit signature-image widget separate from Text8. Text8 sits below the '(signature of noncommercial registered agent)' caption with its own '(type or print name)' caption, suggesting it captures only the typed/printed name; the actual signature is presumably handwritten or applied as an image after print, not via an AcroForm field. Same convention as the rest of the NCRA family.
- Open question: The 'NCRA' suffix on the form_id is shared across the noncommercial-clerk/RA-resignation family. LP_MLPA-3A-NCRA differs from the BC variant only in (a) entity-type heading and (b) notice-recipient-title caption ('(title of person notified)' instead of '(title of corporate officer)'), permitting 'General Partner' as the typical recipient title.
