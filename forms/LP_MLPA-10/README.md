# LP_MLPA-10 — Articles of Merger (Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 4  
**Fields:** 48  
**Mapped fields:** 44  
**Filer role:** for each preexisting constituent LP — all general partners listed in the Certificate of Limited Partnership; for each other preexisting constituent — an authorized representative (per page-2 footnote)

## Purpose

File Articles of Merger relating to a Limited Partnership under 31 MRSA §1438. Records the constituent (party) organizations, the surviving organization (name, form, jurisdiction), THIRD declaration that the survivor was created by the merger, FOURTH effective date, FIFTH election (created-by-merger vs. preexisted, with sub-options for org-doc amendments), SEVENTH service-of-process address for foreign survivors, EIGHTH additional-info exhibit, and per-party signature blocks (4 inline + copy-page overflow). For preexisting LP constituents, §1438 footnote requires signature by ALL general partners listed in the LP's Certificate of Limited Partnership.

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

- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FIRST recital widgets (Text1–4) are single underlined blanks despite the form's 3-column header (Name | Form of organization | Jurisdiction). Synth must produce a combined recital string per row; rubric must accept either pipe-separated or whitespace-separated formats. Same pattern as CORP_MBCA-10 (which has a 4-column header).
- Open question: THIRD (Check Box20) and FIFTH option 1 (Check Box21) both declare 'survivor created by the merger'. They appear to be parallel statements and should always agree. Rubric `third-fifth-consistency` enforces this — synth should populate them in lock-step.
- Open question: Page 2 footnote: 'Copy this page, and modify participant number, if more signature spaces are needed' — the form supports >4 parties via copied-page overflow. The schema's `merger.parties[N]` array is open-ended; the form's 4 inline slots are a UI convenience, not a hard cap.
- Open question: Page 2 footnote also clarifies §1438 signing requirements: preexisting LP constituents must be signed by ALL their general partners; other preexisting constituents by an authorized representative. This is why the form has 2 signer slots per constituent — a 2-GP LP fits inline, but 3+ GP LPs must use copied overflow pages.
- Open question: Widget IDs are scrambled across pages (Text11–13, 16 on page 1 = party 1; Text27–30 on page 1 = party 2; Text14–15, 17–18 on page 2 = party 3; Text31–34 on page 2 = party 4). Preserved verbatim — the AcroForm naming reflects PDF authoring quirks rather than logical order.
