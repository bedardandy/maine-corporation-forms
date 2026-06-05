# LP_MLPA-12-1 — Application for Certificate of Authority to Transact Business (Foreign LP) — accompanying Application for Transfer of Authority

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 28  
**Mapped fields:** 26  
**Filer role:** authorized representative of the foreign limited partnership; signature is captured on the accompanying Application for Transfer of Authority (this MLPA-12-1 has no signature widgets)

## Purpose

Qualify a foreign limited partnership (LP, LLLP, or PLLLP) to transact business in Maine under 31 MRSA §1412 in connection with an Application for Transfer of Authority. The form (2 pages, 28 widgets) captures the proposed Maine name and required statutory suffix (FIRST), an optional fictitious-name election when the home name is unavailable in Maine (SECOND), LLLP / PLLLP status elections (THIRD/FOURTH), home-jurisdiction date and state of organization plus principal-office address (FIFTH), required-office address (SIXTH), Maine registered-agent appointment (SEVENTH/EIGHTH — commercial XOR noncommercial), and the general-partner roster (NINTH — 3 inline rows + exhibit overflow). TENTH paragraph requires that an attached certificate of existence is dated within 90 days before delivery. There is no cover letter or signature block on this form — those live on the accompanying Application for Transfer of Authority that this form bundles with.

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

- `registered_agent.type` maps to 2 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- Open question: MLPA-12-1 has only 28 widgets (2 pages) — there is no cover-letter primitive on this form and no signature/signer widget. The form is filed as an attachment to an Application for Transfer of Authority, which carries the cover letter and signature block. Synth must populate the parent form's cover letter, not this one.
- Open question: FIRST captures the Maine-use name (with required statutory suffix) but the form does not separately capture the home-jurisdiction name — the certificate of existence required by TENTH attests to the home name. Mapped FIRST to entity.maine_assumed_name_for_suffix per the schema-gap convention, but a future cleanup may want to alias to entity.name when the home and Maine names are identical.
- Open question: Text12 and Text13 both map to registered_agent.name with the convention that exactly one is filled based on registered_agent.type (commercial→Text12, noncommercial→Text13). Filler / synth must pick the right slot — having two widgets for the same canonical key is intentional on the form (different physical rows for the two registered-agent types).
- Open question: Text3 and Text4 both belong to entity.professional_services_description; split into .line1/.line2 to mirror the multi-line shape used by amendment.changes_description.lineN on MLPA-13A. Synth concatenates non-empty lines for downstream rubric/text consumers.
- Open question: Form ID has a '-1' suffix (cf. LLP_MLLP-12-1 with the same pattern) indicating it's the second sheet in a 2-form bundle. The widgets.json has 28 widgets and the manifest confirms 2 pages.
