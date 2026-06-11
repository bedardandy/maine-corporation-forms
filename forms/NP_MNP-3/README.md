# NP_MNP-3 — Change of Contact Person and/or Address (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 27  
**Mapped fields:** 24  
**Filer role:** varies by FIRST selection per page-1 footnote: '*This change MUST be signed as follows: (1) if Item First, A or D was selected, then by the contact person OR (2) if Item First, B or C was selected, then by the secretary or clerk'

## Purpose

Update the contact person and/or address for an existing Maine domestic nonprofit corporation pursuant to 13-B MRSA §910. Captures (FIRST) one of four mutually exclusive change types (A: address only; B: contact person + address; C: contact person only; D: name change of current contact person), (SECOND) the current contact person on record, (THIRD) the new contact person and/or address per the FIRST selection, and the signer block (Shape A: name + title).

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

- `contact_change.action_type` binds as a single enum_select selecting among 4 option widgets (accepted values: change_of_address, change_of_contact_person_and_address, change_of_contact_person, change_in_name_of_current_contact_person).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: FIRST instructs the filer to 'X all boxes that apply' but the page-1 footnote and the THIRD instructions both treat the choice as mutually exclusive. Confirm whether the form's PDF logic enforces single-selection or whether the filer literally checks multiple boxes (e.g., A+C for both an address change and a person change, even though option B already covers both). Reviewer modeled as a flat 4-way enum following the THIRD instruction structure.
- Open question: Reviewer corrected drafter's contact_person.current.* / contact_person.new.* nested namespace to a flat contact_change.{current_name, current_address, new_name, new_physical_address, new_mailing_address} pattern that mirrors CORP_CLKRA-3's clerk_change.* convention. This keeps the change-type-prefixed-flat-key convention consistent across analogous SOS change forms.
- Open question: Page-1 signer footnote prescribes a specific title constraint by action_type. The signer-title-matches-action-type rubric check encodes this — but the form does not have separate widgets for 'Contact Person' vs 'Secretary or Clerk', so synth must populate filing.signer.title with a string that matches the prescribed role.
- Open question: Form-id naming uses the 'MNP-N' prefix (also seen on NP_MNP-9 just reviewed) rather than the 'MNPCA-N' prefix used by NP_MNPCA-6 / NP_MNPCA-10 / NP_MNPCA-12. The two prefixes appear to coexist in the SOS template lineage (footer dated 2/01/2020 here vs 4/14/2014 on MNP-9). Document the dual prefix convention to avoid synth/rubric collisions.
