# NP_MNPCA-2 — Application for Registration of Name (Foreign Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 24  
**Mapped fields:** 21  
**Filer role:** any duly authorized individual of the foreign nonprofit corporation (signs at bottom of page 0)

## Purpose

Register or renew the corporate name of a foreign nonprofit corporation in Maine under 13-B MRSA §303-A. A registration secures the name for the calendar year of filing; renewal must be filed between October 1 and December 31. Requires an attached certificate of existence (or document of similar import) authenticated by the home jurisdiction within 90 days before delivery.

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

- `filing.application_type` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FIRST checkbox group is implemented as two small /Tx widgets (2two, 2three, ≈17 wide) rather than /Btn checkboxes — the user types an X. Filler must emit 'X' (or similar mark) into exactly one of the two widgets based on filing.application_type. Same /Tx-as-checkbox anomaly seen on a few other SOS templates.
- Open question: FIFTH paragraph requires an attached 'certificate of existence or a document of similar import duly authenticated by the Secretary of State or other official having custody of corporate records in the state or country under whose laws it is incorporated' dated within 90 days before delivery. Not bound to any AcroForm widget — a separate attachment. Track separately in filing.notes / synth metadata; rubric cannot fail-fast on this without out-of-band evidence.
- Open question: Drafter originally proposed entity.principal_office.physical_address / physical_address_line2 / physical_address_line3; corrected in review to the two-line entity.principal_office.address_line{1,2} pattern that matches the existing registered_office.address_line{1,2} convention. The form has only TWO physical address widgets (2five, 2six), not three — drafter conflated 2four (the home-jurisdiction trailing blank) with the address.
