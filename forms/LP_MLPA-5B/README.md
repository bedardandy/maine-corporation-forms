# LP_MLPA-5B — Statement to Add/Delete/Change Location Where an Assumed Name is Used in Maine (Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 29  
**Mapped fields:** 28  
**Filer role:** at least one general partner of the LP per page-1 footnote citing 31 MRSA §1324.1.J — individual signer OR authorized representative of an entity GP. The 'execution constitutes an oath under penalties of false swearing under 17-A MRSA §453' clause matches MLPA-5A.

## Purpose

Update the location(s) where a Maine limited partnership uses a previously filed assumed name (DBA) under 31 MRSA §1308.2. The form (3 pages, 29 widgets, $35 base fee) captures the LP's real name, the assumed name affected (FIRST), the location currently associated with that assumed name (SECOND), and one or more elections — Change location(s) / Add additional location(s) / Delete location(s) — together with a 2-line free-text description of the change (THIRD). An optional exhibit may be attached if more locations are needed than fit inline. Sibling of LP_MLPA-5A (terminate an assumed name); same single-slot signer block (individual GP OR entity GP). Same body shape as the LLC_MLLC-* and LLP_MLLP-* assumed-name-modification forms in the family.

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
- Open question: Reviewer corrected drafter on signer block: drafter mapped Text12/Text13/Text14 to general_partner_1.printed_name / general_partner_entity_1.name / general_partner_entity_1.signer_printed_name_and_capacity (role-keyed multi-slot pattern). Per MLPA-5A precedent, single-slot post-formation modification forms use the filing.signer.* / filing.signer_entity.* family instead — the role-keyed pattern is reserved for formation filings like MLPA-6 where the LP is being created. Note: MLPA-13A (amended annual report) uses general_partner_1.* with a single inline slot — a known inconsistency in the upstream corpus; future cleanup may want to align MLPA-13A to the MLPA-5A convention.
- Open question: Drafter also mapped Text22 (rect [433.5, 65.9, 572.0, 71.7] — narrow ~5.8pt-tall widget at the very bottom of page 1) to general_partner_1.signature with medium confidence. The rect is too small to be a meaningful signature widget and sits below the visible signature/entity-signer block; it appears to be a stray or legacy widget not bound to any captioned label on the rendered form. Consistent with MLPA-5A's open question that 'Form has no AcroForm widget for the wet-ink signature lines' — signatures are collected as wet-ink overlays. Text22 omitted from field_mappings as unbound.
- Open question: Multiple change actions (Check Box4/5/6) may be selected on the same filing per the form's 'The limited partnership intends to:' phrasing, mapping to 3 independent booleans rather than a single enum. This contrasts with the formation-form 'X one box only' transaction-type radio on MLPA-6-1 (which uses a single enum filing.accompanying_transaction_type).
