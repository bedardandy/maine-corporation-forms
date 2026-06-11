# LLC_MLLC-3A-NCRA — Statement of Resignation of Noncommercial Registered Agent (Maine or Foreign LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 22  
**Mapped fields:** 22  
**Filer role:** the noncommercial registered agent who is resigning (signs the lower half of page 0 over the '(signature of resigning noncommercial registered agent)' caption)

## Purpose

File a statement of resignation by the noncommercial registered agent currently appearing on the Maine SOS record for a Maine or foreign LLC, pursuant to 5 MRSA §111. The agent attests to their identity and address as on record (FIRST), names a person at the LLC to whom the SOS-required notice will be sent (SECOND), and signs the statement. The agent's appointment terminates 31 days after this statement is delivered to the LLC. Filing fee is $35 per the page-0 header. 2 pages, 22 widgets. LLC sibling of CORP_MBCA-12E-NCRA (foreign-BC variant) — identical body structure, differs only in the entity-type heading and signer-block label.

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
- Open question: Page 0 has no explicit signature-image widget separate from Text8. Text8 sits below the '(signature of resigning noncommercial registered agent)' caption with its own '(type or print name)' caption, suggesting it captures only the typed/printed name; the actual signature is presumably handwritten or applied as an image after print, not via an AcroForm field. Same convention as MBCA-12E-NCRA.
- Open question: The '5 MRSA §111' citation governs noncommercial-RA resignations across all entity types; this form is the LLC variant in a family that includes CORP_MBCA-12E-NCRA (foreign business corporation) and likely domestic-BC, LP, LLP, NP variants. The resignation_notice.* and registered_agent.* keys generalize cleanly across all entity types — the only per-form variation is entity.name vs entity.home_jurisdiction_name (here entity.name suffices because the form identifies the LLC by its on-record Maine name regardless of domestic/foreign domicile).
- Open question: Drafter initially proposed resigning_agent.{name, physical_address, printed_name} and notification_recipient.{name, mailing_address, title} as new schema-gap namespaces; corrected during review to reuse the existing registered_agent.* and resignation_notice.* keys per MBCA-12E-NCRA precedent. No new schema gaps remain.
- Open question: The 'NCRA' suffix on the form_id is a convention shared with MBCA-12E-NCRA — synth/rubric should treat *_NCRA forms as the noncommercial-RA-resignation family.
