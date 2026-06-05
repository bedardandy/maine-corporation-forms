# CORP_MBCA-12 — Application for Authority to do Business (Foreign Business Corporation)

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 39  
**Mapped fields:** 35  
**Filer role:** an officer of the foreign corporation per 13-C MRSA §1121.5 (signs in EIGHTH signature block on page 2)

## Purpose

Qualify a foreign business corporation to transact business in Maine under 13-C MRSA Chapter 15, providing home-jurisdiction name, optional fictitious-name election (when home name fails §401 / Chapter 22-A §736), Maine registered agent, jurisdiction and date of incorporation, principal-office address, list of current directors and officers, and a certificate of existence dated within 90 days of filing.

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
- Open question: FOURTH paragraph (For professional corporations only) is conditional text that recites the §22-A §730 ownership/licensure requirements but introduces no fillable widgets. entity.is_professional_corporation triggers it; no further fields to capture. Confirm no widget was missed by pdftk/pypdf.
- Open question: Text20 label says 'type or print name and capacity/title' (with slash). Other 13-C MRSA forms use 'capacity' alone (MBCA-11) or 'title' alone (MBCA-9). Mapping to filing.signer.printed_name_and_capacity to match MBCA-11 / MLLC-12, but a filer might write a title here instead. Vision-judge should accept either.
- Open question: SEVENTH section says '(Attach additional pages, if necessary.)' but provides no opt-in checkbox for 'additional officers attached'. Compare MBCA-6 entity.additional_incorporators_exhibit_letter and MLLC-12 manager.additional_attached — those forms do have explicit opt-ins. On MBCA-12 the attachment is expected to be informal; canonical key family does not need an additional_attached flag.
- Open question: Page 0 SECOND registered-agent address widget label reads '(physical location, P.O. Box - street, city, state and zip code)' which could be parsed as 'physical OR P.O. Box accepted'. Other 13-C MRSA forms (MBCA-6) explicitly say 'not P.O. Box'. Confirm whether MBCA-12 actually permits a P.O. Box for the registered agent's physical location, or if the parenthetical has a typo (missing 'not').
