# NP_MLC-6 — Certificate of Organization (Domestic Nonprofit Corporation Independent Local Church)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 42  
**Mapped fields:** 38  
**Filer role:** the corporation's officers (Clerk, Treasurer) and trustees, executing as the originators of the new church-corporation under 13 MRSA §3021. Per-officer signer pattern (Shape E) variant — signers are role-bearing officers/trustees of the entity being formed, not a single 'filing.signer.*' filer

## Purpose

Form a Maine domestic nonprofit corporation organized as an independent local church under 13 MRSA §3021. Records the church's name, the Maine city/town where it is located, the number of trustees and an inline trustees-named recital (THIRD), and the named-and-addressed officers (Clerk, Treasurer) and Trustees who execute the certificate. Filing fee is $5.

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

- `entity.trustee_names_inline` maps to 3 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: The form has THREE inline trustee-name lines (fields 64/65/66) on page 0 (the THIRD recital) AND structured per-trustee blocks (614-628) on page 1. Both must be populated — the THIRD recital is a prose listing, the structured blocks capture address detail. Synth should write the same trustee names in prose into 64/65/66 and into trustee_N.printed_name on page 1.
- Open question: The form provides exactly 5 trustee slots on page 1. If entity.trustee_count > 5, additional trustees go on an attached exhibit (form does not provide an exhibit-letter widget; presumably attached pages are captioned manually).
- Open question: The form does not have AcroForm signature widgets for the Clerk, Treasurer, or Trustees — only printed-name and address widgets. Wet-ink signatures are expected (a separate piece of paper is signed and returned). No fillable signature flow is needed.
- Open question: 13 MRSA §3021 is a narrow church-formation statute; the role names (Clerk, Treasurer, Trustee) are church-specific and don't generalize to other nonprofit forms. The clerk.* / treasurer.* singleton-role keys are introduced here but expected to remain narrow in scope (NP_MNPCA-6 uses incorporator_N.* instead because it's the general nonprofit statute under 13-B MRSA).
