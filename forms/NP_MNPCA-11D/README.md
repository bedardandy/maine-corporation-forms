# NP_MNPCA-11D — Articles of Dissolution (Domestic Nonprofit Corporation, post-intent)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 21  
**Mapped fields:** 19  
**Filer role:** duly authorized officer per 13-B MRSA §104.1.B (form footnote permits any one authorized officer; the form provides two parallel signature blocks but the second is optional)

## Purpose

Dissolve a Maine domestic nonprofit corporation under 13-B MRSA §1104 by filing Articles of Dissolution following a previously-filed Statement of Intent to Dissolve. Recites the prior intent-filing date, attests via SECOND/THIRD/FOURTH/FIFTH that distribution of assets, satisfaction of liabilities, and any required vote conditions have been met, and provides the Maine registered-office address. Sister to NP_MNPCA-11 (intent), NP_MNPCA-11A, NP_MNPCA-11C, NP_MNPCA-11E in the dissolution family.

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
- Open question: SECOND, THIRD, FOURTH, and FIFTH paragraphs are declarative recitals about debt distribution / asset transfer / vote conditions / reports filed — no widgets, implicitly satisfied by the act of signing. No additional rubric checks needed beyond the signature.
- Open question: Cover-letter checkbox names on this form are 'Check Box1/2/3' rather than the more common 'Check Box14/15/16' seen on most NP_MNPCA cover letters. This is a template-naming variation, not a semantic difference — same canonical key family (filing.expedited_service tiers).
- Open question: Form has two parallel signature blocks (filing.signer_1 and filing.signer_2) on page 1 even though §104.1.B requires only one authorized officer. The second slot accommodates corporations whose bylaws require dual signatures or that prefer two-officer attestation; treat as optional, same as sister NP_MNPCA-11.
