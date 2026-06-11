# NP_MNPCA-11B — Statement of Revocation of Voluntary Dissolution Proceedings (Nonprofit)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 36  
**Mapped fields:** 34  
**Filer role:** any duly authorized officer of the nonprofit corporation (per *footnote on page 1: 'This document MUST be signed by any authorized officer.' 13-B MRSA §104.1.B). Two *By signature slots are provided; one is sufficient.

## Purpose

Revoke previously authorized voluntary dissolution proceedings for a Maine domestic nonprofit corporation under 13-B MRSA §1102. Recites current officers (President, Treasurer, Secretary, Clerk) and up to three directors, identifies the consent source (members vs directors, with written consent attached as Exhibit A), and states the corporation's Maine registered office. Signed by an authorized officer; if consent is by members, the clerk/secretary attests minutes custody.

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

- `revocation.consent_source` binds as a single enum_select selecting among 2 option widgets (accepted values: members, directors).
- `registered_agent.physical_address` maps to 2 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: Page 1 contains a 'MUST BE COMPLETED FOR VOTE OF MEMBERS' inset box with a clerk/secretary minutes-custody attestation signature line. The line is visually present but has NO AcroForm widget — it cannot be filled programmatically. Upstream template bug (similar to MNPCA-10's missing widgets); flag for normalize_fields pass. When revocation.consent_source = 'members', this attestation is statutorily required but cannot be captured by the AcroForm.
- Open question: Form provides 7 inline officer/director rows with '(List additional directors on reverse side)' note for spillover. Current schema models exactly 7; rubric should treat officer_8+ as out-of-scope for this template (would require attached pages, which AcroForm doesn't bind).
- Open question: registered_agent.physical_address is captured by two parallel widgets (18 inline + 19 full-width). MBCA-9 / MBCA-11 use a similar pattern. Filler should write the complete address into widget 19 (full width) and leave widget 18 blank, OR write a partial leading-text into 18 and the address proper into 19. Current convention: write to widget 19 only.
