# LP_MLPA-12B — Notice of Cancellation of Certificate of Authority to Transact Business (Foreign Limited Partnership)

**Entity type:** Limited Partnership  
**Statute:** Maine Revised Uniform Limited Partnership Act (31 M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 3  
**Fields:** 27  
**Mapped fields:** 25  
**Filer role:** at least one general partner of the foreign LP (individual or authorized representative of an entity GP) per 31 MRSA §1324.1.M (cf. §1321 formation requirement of all GPs)

## Purpose

Cancel a foreign limited partnership's certificate of authority to transact business in Maine under 31 MRSA §1417. Captures the LP's home-jurisdiction name, optional Maine fictitious name (per §1508), home jurisdiction and date of organization, original Maine authorization date, and current principal-office and (optional) required-office addresses. Pursuant to SEVENTH, the SOS is automatically appointed as agent for service of process for residual rights of action arising from the LP's prior Maine activities.

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
- Open question: FIFTH (required office) is conditional per the * footnote: 'Provided only if the laws of the jurisdiction under which the foreign limited partnership is organized require the foreign limited partnership to maintain an office in that jurisdiction.' There is no checkbox on the form to indicate applicability — the rubric treats it as optional and only enforces the not-P.O.-Box constraint when populated.
- Open question: SIXTH (cancellation recital) and SEVENTH (statutory SOS-as-agent appointment) are fixed recitals with no widgets — they don't require filer input. SEVENTH is analogous to merger.foreign_survivor.service_of_process_mailing_address on MERGFOR but here the appointment is automatic and address-less (residual service goes to SOS forwarding to the last known principal office).
- Open question: Page 1 has only one inline individual-signer slot (vs. 3 on LP_MLPA-6 formation). This matches the §1324.1.M one-signer requirement and parallels the LP_MLPA-12A (amendment) and LP_MLPA-17 (correction) signer block.
