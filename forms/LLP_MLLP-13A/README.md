# LLP_MLLP-13A — Amended Annual Report (Limited Liability Partnership)

**Entity type:** Limited Liability Partnership  
**Statute:** Maine Uniform Partnership Act, LLP provisions (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 27  
**Mapped fields:** 25  
**Filer role:** at least one partner OR any duly authorized person of the LLP, signing under the page-1 footnote 'Certificate MUST be signed by (1) at least one partner OR (2) any duly authorized person.' Two parallel signature blocks: an individual block (Partner(s)*) and an entity block (For Partner(s) which are Entities) — exactly one is populated per filing.

## Purpose

File an amended annual report for a Maine LLP under 31 MRSA §873-A to correct or update information previously reported on a filed annual report. Identifies the LLP (header), its jurisdiction of organization (FIRST), the date the original annual report being amended was filed (SECOND), the substantive changes (THIRD, up to 5 inline lines plus attached pages), and the date on which the underlying information actually changed (FOURTH). Page-2 cover letter is the standard cover-letter primitive. Sibling of LLP_MLLP-13 (the original annual report) and analogous to MBCA-9 / MLLC-9 amended-annual-report patterns.

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
- Open question: Form serves both domestic and foreign LLPs (FIRST captures jurisdiction, page-0 fee schedule lists $85 domestic / $150 foreign). entity.home_jurisdiction is the discriminator at fill time. No separate domestic/foreign opt-in flag needed.
- Open question: THIRD provides 5 inline lines for the changes description plus instruction to 'attach additional pages, if necessary' for overflow. Attachments are physical-only (not bound to AcroForm widgets). Synth packs the description into lines 1..5 sequentially, leaving trailing lines empty.
- Open question: Page-1 entity-signer block (12a13/12a14 in widgets, 'Name of Entity' and 'type or print name and capacity_2' field-ids) parallels MLLP-9 / MLLP-12A. Synth fills EITHER the individual block OR the entity block, not both; rubric flags double-fill as a likely error.
- Open question: Wet-ink (signature) lines on page 1 (above 'type or print name and capacity' and above 'type or print name and capacity_2') have no AcroForm widgets — signature is wet-ink/image overlay only.
- Open question: FOURTH 'This information changed on (date)' is the underlying-change effective date, distinct from filing.date_signed. For contact/address changes the effective date is when the change actually took effect; for typo corrections in the original report, the effective date is typically the same as amendment.original_filing_date (the original report was wrong from the moment it was filed).
- Open question: Field IDs use the AcroForm 'undefined_N' fallback naming for several widgets (undefined_2, undefined_3, undefined_4) — typical of templates that didn't assign explicit field names. Synth/filler must use the literal IDs as captured in widgets.json (no rename).
