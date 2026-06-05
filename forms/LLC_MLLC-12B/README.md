# LLC_MLLC-12B — Statement of Cancellation of Foreign Qualification (Foreign LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 24  
**Mapped fields:** 22  
**Filer role:** a person authorized by the foreign LLC to sign per 31 MRSA §1676.1.B (page-1 footnote: 'this statement MUST be signed by a person authorized by the limited liability company.')

## Purpose

Cancel a foreign limited liability company's authority to conduct activities in Maine under 31 MRSA §1665.7 (with §1662 SOS-as-agent appointment when no registered agent is maintained). Recites the entity's home name, fictitious Maine name (if any), home jurisdiction and date of organization, and date of original Maine qualification, then provides a post-cancellation service-of-process mailing address (FIFTH) and the entity's current principal office address (SIXTH). FOURTH and SEVENTH are declarative-only paragraphs with no widgets.

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
- Open question: FOURTH and SEVENTH are declarative-only paragraphs with no widgets. FOURTH recites the cancellation election ('will no longer conduct business … relinquishes its authority'); SEVENTH acknowledges that any §1510-1.A assumed name(s) will be withdrawn upon the effective date. No rubric value to check.
- Open question: FIFTH is conditional: 'If the foreign limited liability company is not maintaining the registered agent in the State of Maine, the mailing address to which service of process may be mailed pursuant to §1662 is …'. The form itself does not include a checkbox to indicate which condition applies — it is inferred by whether Text6/Text7 are populated. A future schema-level flag like entity.maintains_maine_registered_agent could disambiguate but is not currently captured.
- Open question: Text6 and Text7 are both labeled '(Principal office address)' but FIFTH refers to a 'mailing address … pursuant to §1662'. The label on the widget appears to be a copy-paste from a sibling form (e.g., MBCA-12) rather than the §1662 mailing address — a possible upstream template label bug. Mapped to entity.post_cancellation_service_address.{line1,line2} based on the surrounding paragraph text rather than the widget label.
- Open question: Page-1 (authorized signature) line has no AcroForm widget — only Text10 for printed name + capacity. Signature is wet-ink/image overlay, consistent with all other Maine SOS LLC forms.
