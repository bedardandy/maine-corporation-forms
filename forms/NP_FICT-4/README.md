# NP_FICT-4 — Statement of Intention to Do Business Under a Fictitious Name (Foreign Entities Only)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 21  
**Mapped fields:** 21  
**Filer role:** duly authorized officer of the foreign nonprofit corporation per the page-0 footnotes (§1304 for nonprofit corporations). Signature footnote enumerates authorized signers by entity type — for a foreign nonprofit, the signer is typically a President, Vice-President, Treasurer, Secretary, or other duly authorized officer.

## Purpose

Foreign-entity-only filing declaring intent to transact business in Maine under a fictitious name when the entity's real name is unavailable in this State per 31 MRSA §1508 / 13-C MRSA §1505. The PDF is shared across entity types — the page-0 footnotes enumerate authorizing statutes for foreign business corporations (§1505), foreign LLCs (§1626), foreign LPs (§1308), foreign LLPs (§869), and foreign nonprofits (§1304). The NP_FICT-4 alias names the nonprofit-only invocation of the shared form (filing fee $25); CORP_FICT-4 names the for-profit invocation (filing fee $40). Identical widget composition to CORP_FICT-4 (md5-identical PDF).

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
- Open question: NP_FICT-4 and CORP_FICT-4 share an md5-identical PDF and an identical widget composition — they are the same form filed under two namespace aliases. The only practical difference at fill time is the fee tier (nonprofit $25 vs for-profit $40). Synth/rubric should treat NP_FICT-4 as a thin wrapper that selects the $25 fee branch when populating filing.total_fees_dollars. Drafter initially proposed schema_gaps for entity.home_jurisdiction_name, entity.maine_fictitious_name, entity.home_jurisdiction, and entity.maine_authorization_date — these were rejected during review because all four keys already exist upstream (in MLLC-12, CORP_FICT-4, CORP_CLKRA-3).
- Open question: Page 0 widget naming: the FIRST blank uses field-id 'undefined', the SECOND-line jurisdiction blank uses 'and the date on which' (auto-generated from the label text after the blank), and the SECOND-line date blank uses 'undefined_2'. This naming is unique to FICT-4 within the SOS corpus and is preserved verbatim upstream. The filler engine must accept these unusual field-ids without normalization.
- Open question: FICT-4 is commonly bundled with foreign-qualification filings (e.g., MLLC-12 when the foreign LLC's home name is unavailable in Maine, MNPCA-1 when a foreign nonprofit qualifies). Synth should reuse entity.home_jurisdiction_name and entity.maine_fictitious_name across the bundled forms when applicable.
- Open question: Page-0 footnotes enumerate authorized-signer rules by entity type and statute. For NP_FICT-4 specifically, the controlling statute is 13-C MRSA §1304 (foreign nonprofits), with the corresponding signer-title scope as documented in the signer-title rubric check.
