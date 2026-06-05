# LP_MLPA-5A — Statement of Termination of an Assumed or Fictitious Name (Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 20  
**Mapped fields:** 18  
**Filer role:** at least one general partner of the LP — individual OR an authorized representative of an entity general partner (per page-0 footnote: '*Statement MUST be signed by at least one general partner. (31 MRSA §1324.1.D or 31 MRSA §1324.1.M). The execution of this statement constitutes an oath or affirmation under the penalties of false swearing under 17-A MRSA §453.')

## Purpose

Terminate a previously filed Statement of Intention to do Business Under an Assumed or Fictitious Name for a Maine Limited Partnership under 31 MRSA §1308.2.I or §1415.7. Captures the LP's real name, the assumed/fictitious name being terminated, and a single signer block (individual general partner OR entity general partner). Structurally analogous to LLP MLLP-5A and LLC MLLC-5A.

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
- Open question: Reviewer corrected two material drafter errors: (a) Text3 was mapped to 'general_partner_1.signature' but is actually the DATED widget (filing.date_signed) based on rect position (right of 'GENERAL PARTNER(S)*' header, narrow ~131pt for date entry); (b) drafter used the role-keyed general_partner_N.* / general_partner_entity_1.* multi-slot pattern, but this form has only ONE inline individual slot and ONE inline entity slot — single-slot post-formation termination matches MLLP-5A which uses filing.signer.* / filing.signer_entity.*. The role-keyed pattern (general_partner_N.*) is reserved for formation-style filings like MLPA-6 where the LP is being created.
- Open question: Page-0 footnote cites 31 MRSA §1324.1.D or §1324.1.M for signature authority (rather than §1308.2.I or §1415.7 cited for the form's substantive authority). Confirm signer is a 'general partner' under the §1324 enumeration regardless of which substantive section authorizes the termination.
- Open question: Form has no AcroForm widget for the wet-ink signature lines (left-side underlines under '(signature)' and '(authorized signature)' captions). Signatures are collected as wet-ink/image overlays, consistent with MLLP-5A and the broader filer-engine convention.
- Open question: Sibling forms: LLP_MLLP-5A (LLP termination, single-slot signer + single-slot entity-signer) and LLC_MLLC-5A (LLC termination, two-slot signer, no entity slot). The three sibling forms have related but not identical signer-block shapes — the canonical-key family follows the form's literal widget composition rather than the form's shared termination purpose.
