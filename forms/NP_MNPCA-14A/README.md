# NP_MNPCA-14A — Certificate of Resumption (Domestic Nonprofit Corporation)

**Entity type:** Nonprofit Corporation  
**Statute:** Maine Nonprofit Corporation Act (13-B M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 30  
**Mapped fields:** 24  
**Filer role:** any duly authorized officer of the nonprofit corporation per 13-B MRSA §104.1.B (page-1 footnote). When adopted by member vote, the clerk/secretary or assistant secretary co-signs the 'MUST BE COMPLETED FOR VOTE OF MEMBERS' attestation block (wet-ink only — no AcroForm widget).

## Purpose

Resume the carrying-on of activities for a Maine domestic nonprofit corporation that has previously suspended/forfeited its existence, pursuant to 13-B MRSA §1301.6. FIRST recites that the certificate was adopted by the corporation's members or directors on a stated date and location, either at a meeting legally called and held or by unanimous written consent. SECOND certifies that a majority of members or directors have voted to resume carrying on activities. THIRD records the (current) Maine registered office address. FOURTH classifies the corporation as a public-benefit or mutual-benefit corporation. After filing, the corporation is required to file annual reports beginning with the next reporting deadline.

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

- `resumption.adopting_body` maps to 2 widgets; all receive the same value.
- `resumption.method` maps to 2 widgets; all receive the same value.
- `resumption.voting_body` maps to 2 widgets; all receive the same value.
- `entity.nonprofit_type` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: FIRST paragraph layout: the form reads 'This certificate was adopted by a majority of the [members][directors] on (date) at (location). [meeting][written consent]' — i.e., the meeting/written-consent radio appears AFTER the date/location line. On the meeting branch, location is clearly the meeting location. On the written-consent branch, the (location) blank is conventionally filled with the place of execution OR left blank — either is accepted by SOS in practice. Synth should leave adoption_location blank when method='written_consent'; rubric treats it as required only when method='meeting'.
- Open question: SECOND paragraph duplicates the members/directors selection from FIRST. The form does not enforce equality, but in normal practice the same body adopts and votes — captured as an advisory rubric check (adopting-and-voting-bodies-match).
- Open question: Page 1 has TWO *By signature blocks (Text15, Text16). The MUST-BE-COMPLETED-FOR-VOTE-OF-MEMBERS box on the same page contains a SEPARATE wet-ink-only signature line for 'signature of clerk, secretary or asst. secretary' — there is NO AcroForm widget for that clerk signature. So Text16 is most likely a SECOND officer's signature block (parallel to NP_MNPCA-6A_0.Text17), not the clerk attestation. May be left empty when only one officer signs.
- Open question: THIRD's registered-office address widgets (10, 11) follow the MARK1 .line1/.line2 multi-widget single-concept pattern. This is registered_office.address (the corporation's OWN office), distinct from registered_agent.physical_address (where the agent receives service). The 14A form does not itself update the registered agent — agent changes use a separate CLKRA filing.
- Open question: Page-0 footnote at FOURTH includes both 'public benefit corporation' and 'mutual benefit corporation' but no 'religious corporation' option, even though 13-B distinguishes religious nonprofits in some contexts. Synth should restrict entity.nonprofit_type to {public_benefit, mutual_benefit} on this form.
