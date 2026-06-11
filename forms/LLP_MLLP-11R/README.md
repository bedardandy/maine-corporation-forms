# LLP_MLLP-11R — Certificate of Renunciation (Domestic Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 31  
**Mapped fields:** 31  
**Filer role:** per the * footnote on page 1: (1) if partners are winding up the LLP's affairs — by the contact partner OR a majority in interest of the partners; OR (2) if partners are not winding up — by all liquidating trustees; OR (3) any duly authorized person. The form provides three parallel individual-signer slots and three parallel entity-signer slots; the appropriate slot count depends on which authority tier applies.

## Purpose

Renounce LLP status of a Maine domestic registered limited liability partnership under 31 MRSA §825 without affecting the partnership's underlying existence. Captures the date the original LLP certificate was filed (FIRST), the reason for renunciation (SECOND, multi-line), an optional future effective date or time (THIRD), and an optional exhibit reference for additional information (FOURTH). Filing fee $75. The certificate must be signed per §825's three-tier authority rule (see filer_role).

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
- Open question: Field IDs use the form-id-prefixed scheme '11r1'…'11r17' rather than 'TextN' — preserved verbatim. This is unusual for SOS forms (most use TextN); MLLP-11R is the first observed instance.
- Open question: Three individual-signer slots and three entity-signer slots are parallel — the rubric treats them as additive (any signer block, individual or entity, can satisfy §825). Whether the SOS rejects mixed individual+entity signing in practice is unverified.
- Open question: renunciation.* is a new namespace (renunciation of LLP status). Sibling forms in the broader inventory (MLLP-9 dissolution, similar partnership-status-change forms) may or may not reuse renunciation.* — revisit when those are inspected.
- Open question: filing.signer_3.printed_name_and_capacity is a genuine extension of the MLLC-17 signer_2 pattern. Not yet observed on any other form; if a future form requires more than 3 individual signers, the pattern can extend to filing.signer_N for arbitrary N.
- Open question: filing.entity_signer_N.* is a parallel namespace to general_partner_entity_N.* but at the filing level (no role-specific anchor like 'general_partner'). Justified because §825's third tier ('any duly authorized person') doesn't pin the signer to a specific role.
