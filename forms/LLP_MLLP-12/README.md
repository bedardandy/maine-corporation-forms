# LLP_MLLP-12 — Application for Authority to Do Business (Foreign Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 40  
**Mapped fields:** 36  
**Filer role:** an authorized partner or other authorized person of the foreign LLP per 31 MRSA §852 / §1676.1 — signs the page-2 signature block. The form provides parallel slots for an individual signer and an entity signer (where the LLP is signed for by another entity).

## Purpose

Qualify a foreign limited liability partnership to conduct activities in Maine under 31 MRSA §852.3, providing home-jurisdiction name, optional Maine assumed-name (when home name lacks the LLP suffix per §803-A) or fictitious Maine name (when home name is unavailable), Maine registered agent, contact partner, commencement date, optional professional-LLP election, and a certificate of existence (ELEVENTH paragraph). Body schema mirrors LLC_MLLC-12 (foreign-LLC authority) with LLP-specific role-name substitution (contact_partner instead of manager).

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
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: TENTH 'Check only if applicable' checkbox for is_professional_llp is visible on the rendered form but is NOT extracted as an AcroForm widget — same template-level upstream issue as MNPCA-10 / MBCA-10 (see schema-gaps/2026-04-30-phase2-summary.md). Filler engine must either bind by rect or accept the boolean as a synth/data-side flag with no widget. is_professional_llp is still listed as a schema_gap so synth/rubric can reason about it.
- Open question: EIGHTH inline blank '...attached as Exhibit ___' for the exhibit letter is not extracted as an AcroForm widget either. The Check Box26 boolean opt-in is bound, but there is no corresponding text widget for the letter — same pattern as MBCA-12. Filler may need to handle the exhibit-letter as a synth/data-only field.
- Open question: SEVENTH paragraph (RA consent recital) is purely declarative — no widget needed. Confirmed against widgets.json: only Check Box24/25 + Text9–13 on page 1's RA section.
- Open question: Page-2 signature block has parallel individual-signer (Text19/Text20) and entity-signer (Text21/Text22) sub-blocks. Synth should fill EITHER block, not both — rubric flags double-fill as a likely error.
