# Upstream worklist

Findings that need action from the **Maine Secretary of State** (or a future
re-capture of their forms), not from this repo. Each entry records what was
checked and when, so the next drift pass can re-verify cheaply.

## MNPCA-18 — referenced by a published form, but not published

**Status: cannot be carried.** Not invented; tracked here instead.

- **Referenced by:** `NP_MNPCA-10E` (Articles of Consolidation, nonprofit,
  rev. 8/23/2006). The form's own printed bottom note reads: *"If a domestic
  corporation is the result of this consolidation, THIS FORM MUST BE
  ACCOMPANIED BY FORM MNPCA-18 (Acceptance of Appointment as Registered Agent
  §204.3.)"*.
- **Checked 2026-06-11** against the official sources this repo's
  `catalog/pdf_manifest.json` records:
  - the SoS nonprofit-corporation forms listing
    (`maine.gov/sos/corporations-commissions/i-need-a-business-form/nonprofit-corporation-forms`)
    skips from **MNPCA-17** (Certificate of Correction) straight to
    **MNPCA-19** (Articles of Domestication and Conversion) — no MNPCA-18
    entry exists;
  - the file host pattern every carried MNPCA blank uses
    (`maine.gov/sos/sites/maine.gov.sos/files/inline-files/mnpca<NN>.pdf`)
    returns **404** for `mnpca18.pdf` (and case/hyphen variants), while
    sibling forms (e.g. `mnpca10e.pdf`) still return 200.
- **Action here:** none possible without fabrication — there is no official
  PDF to extract a manifest hash, schema, or mapping from. The referencing
  form's `README.md` records that the cross-reference is stale upstream text
  from the 2006 revision.
- **Re-check trigger:** if a future drift pass finds the SoS publishing
  MNPCA-18 (listing entry or live `inline-files/mnpca18.pdf`), carry it
  through the standard form-by-form pipeline (manifest entry with sha256 +
  source URL, schema/mapping extracted from the PDF, SKILL + tests).

## MARK_mark5 — reference guide, no fillable blank to verify a mapping against

**Status: intentionally unmapped, therefore unstamped.** The
`built_against_sha256` re-verification pass (2026-06-11,
`tools/verify_mapping_fields.py`) verified and stamped **155 of 156**
mappings against the manifest-pinned blanks. The one exception:

- **MARK_mark5** (*Class Numbers for Marks*, the trademark class-number
  reference guide) ships **without an AcroForm** (`has_acroform: false` in
  `catalog/pdf_manifest.json`), so its `mapping.json` carries an empty `map`
  by design — there are no widgets to survive, hence nothing to verify and
  no stamp to carry. The verifier reports it as
  `empty map (recipe pointer) — nothing to verify`.
- **Action here:** none — stamping it would be a blind back-fill.
- **Re-check trigger:** if a future drift pass finds the SoS publishing a
  fillable revision, map it through the standard pipeline and stamp it then.
