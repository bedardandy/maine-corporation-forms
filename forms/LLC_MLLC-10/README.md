# LLC_MLLC-10 — Statement of Merger (Relating to a Limited Liability Company)

**Entity type:** Limited Liability Company  
**Statute:** Maine Limited Liability Company Act (31 M.R.S. ch. 21)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 49  
**Mapped fields:** 47  
**Filer role:** for each constituent organization, an authorized representative (per 31 MRSA §§1643.1 and 1676.1) signs the per-party signature block. The form provides two signer slots per constituent for entity types whose authorization rules require multiple signers; only one is required by statute.

## Purpose

File a Statement of Merger involving at least one Maine LLC under 31 MRSA §1641. Records the constituent (party) organizations to the merger, the surviving organization (name, form, jurisdiction, date of organization, principal office), the THIRD-paragraph election (survivor created by this merger vs. preexisted, with sub-options for organizational-document amendments), the effective date, the foreign-survivor service-of-process address (SIXTH), an additional-information exhibit (SEVENTH), and per-party signature blocks (4 inline + copy-page overflow). Per 31 MRSA §§1643.1 / 1676.1, the statement must be signed by an authorized representative of each constituent organization.

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

- `merger.third_election` binds as a single enum_select selecting among 2 option widgets (accepted values: created, existed_before).
- `filing.expedited_service.*` maps to 3 independent boolean checkboxes (hold_for_pickup, expedite_24h, immediate).
- Open question: FIRST recital widgets (Text1–Text4) are single underlined blanks despite the form's 4-column header (Name | Form of Organization | Jurisdiction | Date of Organization). Synth must produce a combined recital string per row; rubric must accept either pipe-separated or whitespace-separated formats. Same pattern as CORP_MBCA-10 and LP_MLPA-10.
- Open question: Page 1 widget IDs are scrambled across the three signature blocks: party 1 uses Text20 (date), Text21–22 (signers), and Text24 (name); party 2 uses Text23 (name) and Text25–27 (date + signers); party 3 uses Text28–31 in order. Drafter initially mapped Text23 to party 1 and Text24 to party 2 — reviewer corrected based on y-coordinate ordering (Text24 y≈462 is higher on page 1 than Text23 y≈295). AcroForm naming reflects PDF authoring quirks rather than logical order — same as LP_MLPA-10.
- Open question: Page 2 inline note: 'Copy this page, and modify participant number, if more signature spaces are needed' — the form supports >4 parties via copied-page overflow. The schema's merger.parties[N] array is open-ended; the form's 4 inline slots are a UI convenience, not a hard cap.
- Open question: SIXTH foreign-survivor address (Text17, Text18) has two address lines. Per LP_MLPA-10's convention these split into physical_address and mailing_address; LLC_MLLC-10's heading 'address of its principal office for the purpose of §1644.2' doesn't explicitly distinguish physical from mailing, so the mapping is conventional rather than statutory.
- Open question: Each constituent's signature block has two signer slots (signer_1, signer_2). 31 MRSA §1643.1 says 'signed by a person authorized', singular, but multi-member LLCs or other entity types may require multiple authorized signers — hence the two slots. Rubric treats signer_2 as optional.
