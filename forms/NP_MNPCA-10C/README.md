# NP_MNPCA-10C — Articles of Merger (Merger of Domestic and Foreign Nonprofit Corporations)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 47  
**Mapped fields:** 36  
**Filer role:** an officer of each participating corporation signs in that corporation's signature block on page 1 (per 13-B MRSA §906); a clerk/secretary additionally certifies the member-vote action when applicable (only the domestic corporation has a member-vote certification — the foreign corp's adoption is governed by its home-jurisdiction laws and is not recorded here)

## Purpose

File Articles of Merger between a Maine domestic nonprofit corporation and one or more foreign corporations under 13-B MRSA §906. Records the two participating corporations and their home jurisdictions, public-vs-mutual benefit classification (only when the surviving corp is Maine), the foreign jurisdictions whose laws permit the merger, the surviving corporation's identity / governing law / service-of-process address (when foreign), the plan-of-merger exhibit, the domestic corporation's adoption method (4 mutually-exclusive options), registered-office addresses for both corps, optional future effective date, and dual signature blocks with member-vote certifications.

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

- `merger.surviving_corp.name` maps to 2 widgets; all receive the same value.
- `merger.surviving_corp.home_jurisdiction` maps to 2 widgets; all receive the same value.
- `merger.surviving_corp.benefit_type` maps to 2 widgets; all receive the same value.
- `merger.domestic_corp.vote_method` maps to 4 widgets; all receive the same value.
- `merger.domestic_corp.vote_method_date` maps to 4 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: The 'MUST BE COMPLETED FOR VOTE OF MEMBERS' inset blocks (one under each DATED row on page 1) have NO matching widgets in the AcroForm — visually each inset has a (name of corporation) line and a (signature of clerk, secretary or asst. secretary) line. These mirror NP_MNPCA-10's clerk_certification.* keys but are unbindable on this template (same upstream template gap as NP_MNPCA-10). Recommend an upstream pdftk/normalize_fields pass to add the missing widgets; until then, synth fill cannot populate the clerk-certification block via AcroForm.
- Open question: Field 27 has the read-only flag (4194304) on this template, which is unusual — it suggests the SOS template may have intended the (surviving corporation) name to be auto-populated from field 3. The filler engine should either honor the read-only flag (and skip filling) or override it to populate consistently. If skipped, the rendered output will show field 3's value but the AcroForm value of field 27 will remain empty — visual fidelity preserved but data extraction inconsistent.
- Open question: Foreign corp's adoption method is NOT recorded on this form (no FIFTH-style block for it) — the form assumes foreign-side adoption is governed by the foreign jurisdiction's laws and certified out-of-band (the SECOND recital's general assertion that 'foreign corporation(s) ... has (have) complied with the applicable provisions of such laws' is the only attestation). Synth and rubric should NOT add a foreign-side vote_method.
- Open question: The form cites both 13-B MRSA §906 (current) and an older 13 MRSA §906 (page-0 statute reference). Field set is identical regardless of which statute the filing invokes; the citation is informational.
- Open question: Page-0 widget naming uses bare digit ids (1-20) plus one anomalous 'Text7' for the FOURTH exhibit-letter blank. Filler engine should accept both bare-digit and Text-prefixed naming conventions on the same form.
- Open question: Page-1 footnote: '*Must provide address of registered office in Maine. If the corporation does not have a registered office in Maine, the address given should be the principal or registered office of the corporation wherever located.' This relaxes the SIXTH 'in the State of Maine' requirement for foreign parties — synth/rubric should accept any valid address rather than enforce a Maine zip.
