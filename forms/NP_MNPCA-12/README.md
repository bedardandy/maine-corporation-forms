# NP_MNPCA-12 — Application for Authority to Carry on Activities (Foreign Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 36  
**Mapped fields:** 33  
**Filer role:** duly authorized individual of the foreign nonprofit per 13-B MRSA §104.1.B (signs in EIGHTH-block area on page 1)

## Purpose

Qualify a foreign nonprofit corporation to carry on activities in Maine under 13-B MRSA §1202. Recites the entity's home-jurisdiction name, optional Maine fictitious name (with bundled FICT-4 indicator) when the home name is unavailable per §301-A, jurisdiction and date of incorporation, authorized purposes in the home jurisdiction, scope of activities sought in Maine (all-authorized vs. specific-subset), principal/registered office address, Maine registered agent, registered-agent §1105.2 consent recital, and certificate-of-existence attachment. Sister to CORP_MBCA-12 (foreign business corporation) but without an officer roster.

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

- `entity.maine_activities_scope` binds as a single enum_select selecting among 2 option widgets (accepted values: all, specific).
- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: This form does NOT include an officer roster (despite 2026-04-30-officer-roster-pattern.md anticipating one for MNPCA-12). Page 1 contains only SIXTH (registered agent), SEVENTH (5 MRSA §1105.2 RA-consent recital), and EIGHTH (certificate-of-existence recital + signature block) — there are no name/address widgets for current officers/directors. The roster pattern's anticipated key family (officer_N.*) does not apply here; foreign-nonprofit qualification under 13-B MRSA §1202 is structurally simpler than its corporate counterpart (CORP_MBCA-12), which DOES include a 3-row officer roster with overflow.
- Open question: SEVENTH paragraph is a declarative recital that the listed registered agent has consented to serve under 5 MRSA §1105.2 — no widget. Implicitly satisfied by the act of filing. (Note: the form cites '5 MRSA §1105.2' but the MRSA §1105 series governs CRAs / public process under Title 5; this is the correct cite for the registered agent's statutory consent.)
- Open question: Text11 (commercial-RA name) and Text12 (noncommercial-RA name) are physically distinct widgets but share the same canonical key registered_agent.name — only one is populated per filing based on registered_agent.type. The PDF logic does not mirror them automatically; synth must select the correct row by type.
- Open question: (signature of any duly authorized individual) line above Text16 has no AcroForm widget — wet-ink overlay only. Standard Shape-D convention.
