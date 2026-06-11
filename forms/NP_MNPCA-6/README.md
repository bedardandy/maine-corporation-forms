# NP_MNPCA-6 — Articles of Incorporation (Nonprofit)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 57  
**Mapped fields:** 48  
**Filer role:** incorporator(s) — natural persons or corporate incorporators executing on behalf of an entity per 13-B MRSA §401

## Purpose

Form a Maine domestic nonprofit corporation under 13-B MRSA §403, designating public-benefit vs mutual-benefit purpose, registered agent, board structure, member structure, optional 501(c) provisions, and incorporator signatures (individual or corporate).

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

- `registered_agent.name` maps to 2 widgets; all receive the same value.
- `entity.no_political_activities_clause` maps to a single checkbox widget (`Check Box25`).
- `entity.has_501c_exhibit` maps to a single checkbox widget (`Check Box26`).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: The form uses two parallel mechanisms for SEVENTH/EIGHTH opt-ins: tiny X-mark text widgets ('Optional', 'Optional_2') and AcroForm checkboxes (Check Box25, Check Box26). Should fill logic write to one, both, or only the X-mark text widget?
- Resolved: the SECOND, THIRD, and SIXTH radio groups are backed by the button groups 'bene', 'cra', 'mem' (kid on-states verified by geometry+text; e.g. 'cra' on-states Yes = Commercial Registered Agent, cra2 = Noncommercial Registered Agent). The tiny X-mark text widgets overlaying the boxes are stray and stay unmapped — `entity.nonprofit_type`, `registered_agent.type`, and `entity.has_members` each select through the group binding in mapping.json.
- Open question: Page 1 incorporator block has 8 text fields for what appears to be 3 incorporator slots (3 print_name + 3 street + 3 city_state_zip = 9). One field (Text17) doesn't fit cleanly — could be an additional Dated/header field or one of the rows is partial. y-coordinate analysis suggests row assignments need disambiguation by visual fill testing.
- Open question: Most/all SOS forms have separate fields for Commercial vs Noncommercial registered agent (CRA name vs noncommercial name) — confirm canonical fill rule (single 'registered_agent.name' written to whichever slot matches selected type).
