# LLC_MLLCSOA — Statement of Authority (for a Maine LLC)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 35  
**Mapped fields:** 33  
**Filer role:** authorized person(s) of the LLC. Up to three may sign — multi-signer at the filing level (filing.signer_N.printed_name_and_capacity, N=1..3). Distinct from the per-party merger signature pattern (merger.parties[N].signature_block.signer_M) and from the single-filer Shape D pattern.

## Purpose

File a Statement of Authority under 31 MRSA §1542.1 to grant or limit the authority of specific persons or existing positions to enter into transactions or otherwise bind a Maine LLC. Supports up to three inline authority blocks (each: a person or position name + four free-form authority/limitation text lines), an optional exhibit letter for additional authority blocks beyond three, and up to three authorized signers (filing.signer_N pattern) — some entity-level decisions under 31 MRSA require multiple signers.

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
- Open question: Considered collapsing authority_N.authority_text_line_M (M=1..4) into a single multi-line key authority_N.authority_text. Kept per-line keys to preserve form fidelity at fill time — the form has 4 distinct single-line widgets per block, not one multi-line widget. A higher-level helper can join lines with newlines for synth readability.
- Open question: Multi-signer pattern (filing.signer_N) parallels the multi-signer slot composition on LP_MLPA-9's Authorized Signatories block (which uses general_partner_N.printed_name because LP signers are role-keyed). LLCs use member-managers/managers but the Statement-of-Authority form uses generic 'authorized person' language without a specific role — hence filing.signer_N rather than manager_N or member_N.
- Open question: Three signer slots is a hard cap on this form (no 'attach additional pages'). 31 MRSA §1542.1 doesn't itself limit signer count; the form's three-slot cap is a template choice, not a statutory one. Synth should use 1-2 signers for typical fills.
- Open question: The exhibit affordance has no checkbox — only the letter widget. Synth should treat presence of authority.additional_exhibit_letter as the exhibit-attached signal.
