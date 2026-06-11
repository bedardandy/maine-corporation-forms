# NP_MNPCA-10 — Articles of Merger (Maine/Maine Domestic Nonprofit)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 48  
**Mapped fields:** 34  
**Filer role:** an officer of each participating corporation signs in that corporation's signature block on page 1 (per 13-B MRSA §904); a clerk/secretary additionally certifies the member-vote action when applicable

## Purpose

File Articles of Merger between two Maine domestic nonprofit corporations under 13-B MRSA §904 (or 13 MRSA §961 for older filings). Records the merging-corp(s) and surviving corp, public-vs-mutual benefit classification, plan-of-merger exhibit, per-corporation voting recital (4 mutually-exclusive options each), registered-office addresses for both, optional future effective date, and dual signature blocks with member-vote certifications.

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

- `merger.parties[0].vote_method_date` maps to 4 widgets; all receive the same value.
- `merger.parties[1].vote_method_date` maps to 4 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Template-level naming inconsistency: most text widgets on this form use bare digit names ('1', '2', '5', '6', '8', '11'-'37') instead of the 'TextN' prefix used on newer forms. Filler engine should accept both naming styles. Consider an upstream normalize_fields pass to migrate to a consistent prefix.
- Open question: FIRST section (public_benefit vs mutual_benefit corporation classification) appears to have TWO checkboxes visible on the rendered page but ZERO matching widgets in the AcroForm. These checkboxes are MISSING from the template. Either (a) FIRST is informational and the classification is captured elsewhere (annual report? articles?), or (b) the template is missing widgets and needs an upstream fix. Recommend pdftk dump_data_fields on a fresh download to rule out an (a) interpretation.
- Open question: Merged-corp signature block on page 1 has only widgets '36' and '37' (apparently DATED + first signer). The parallel widgets for corp-name underline (matching '31'), second signer (matching '33'), and member-vote clerk-cert (matching '34'/'35') are MISSING. Visually these blanks exist on the form. Likely a 2006-revision template bug; flag for upstream fix and treat the missing fields as 'cannot fill via AcroForm' until corrected.
- Open question: FOURTH addresses: form provides 2 underlined blanks per corp (an inline trailing blank ending the sentence + a labeled '(street, city, state and zip code)' line below). Convention here treats them as line1 + line2 of a single address; alternative would be to treat line1 as a continuation-of-sentence space and line2 as the actual address. Confirm with a visual fill test.
- Open question: FIFTH effective-date cap notes 'Not to exceed 60 days from date of filing of the Articles' — should be enforced by rubric (already drafted as future-effective-date-cap).
