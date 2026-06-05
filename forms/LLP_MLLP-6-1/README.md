# LLP_MLLP-6-1 — Certificate of Limited Liability Partnership — accompanying entity-action filing

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 19  
**Mapped fields:** 13  
**Filer role:** authorized partner or representative of the partnership; signature is captured on the accompanying underlying filing (this MLLP-6-1 has no signature widgets)

## Purpose

File a Certificate of Limited Liability Partnership pursuant to 31 MRSA §822 in connection with one of five underlying entity-action filings that produces an LLP as the resulting entity: Articles of Entity Conversion (13-C MRSA §955.1), Articles/Certificate of Merger or Share Exchange (13-C MRSA §1106 / 31 MRSA §744 / 31 MRSA §1436), Certificate of Inter-Entity Consolidation (31 MRSA §744), Articles/Certificate of Conversion (31 MRSA §746 / 31 MRSA §1432), or Articles of Conversion of Partnership (31 MRSA §1093). The form (2 pages, 19 widgets) captures the LLP name (FIRST), the Maine registered agent (SECOND — commercial XOR noncommercial; THIRD is a static §108.3 consent recital with no widget), the optional professional-LLP election with services description (FOURTH), the contact partner block (FIFTH), and an exhibit letter for additional provisions (SIXTH). There is no cover letter or signature block on this form — those live on the accompanying underlying filing.

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

- `filing.underlying_filing_type` maps to 5 widgets; all receive the same value.
- `registered_agent.type` maps to 2 widgets; all receive the same value.
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- Open question: MLLP-6-1 has only 19 widgets (2 pages) — there is no cover-letter primitive on this form and no signature/signer widget. The form is filed as an attachment to one of five underlying entity-action filings (selected by Check Box 12-16), each of which carries its own cover letter and signature block. Synth must populate the parent filing's cover letter and signer, not this one.
- Open question: Form ID has a '-1' suffix (cf. LP_MLPA-12-1, LLP_MLLP-12-1) — same accompaniment pattern: a 2-page widget-only form with no cover letter or signer.
- Open question: THIRD recital ('Pursuant to 5 MRSA §108.3, the registered agent so listed above has consented to serve as the registered agent for this limited liability partnership') is a static statutory declaration with no fillable widget — covered by the agent's signed §108.3 acceptance, not a form widget.
- Open question: Text7 / Text8 both belong to entity.professional_services_description; split into .line1/.line2 to mirror the multi-line shape primitive established by LLP_MLLP-12, LP_MLPA-12-1.
- Open question: Text3 (commercial-side name) and Text4 (noncommercial-side name) both bind to registered_agent.name with the convention that exactly one is filled based on registered_agent.type. Identical pattern to LP_MLPA-12-1, LLP_MLLP-6A.
- Open question: filing.underlying_filing_type is new on this form. Synth must select one of the five enum values consistent with the parent filing being submitted (e.g., when accompanying an Articles of Entity Conversion filing, select 'articles_of_entity_conversion').
