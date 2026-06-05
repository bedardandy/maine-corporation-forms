# CORP_RO-E911 — Notification of Change in Address by Municipality or U.S. Postal Service

**Entity type:** Business Corporation  
**Statute:** Maine Business Corporation Act (13-C M.R.S.)  
**Source:** Maine Secretary of State  
**Pages:** 2  
**Fields:** 23  
**Mapped fields:** 20  
**Filer role:** municipal official or postmaster (page-0 footnote: '*This document MUST be signed by the municipal official or postmaster'). Single-signer Shape D — printed name and capacity combined in one widget.

## Purpose

Notify the Maine Secretary of State that the address of a registered entity's clerk or registered agent has been administratively changed by either the local municipality (e.g., E911 street-renumbering) or the U.S. Postal Service (e.g., zip-code reassignment). The entity itself does not initiate this filing — the municipal official or postmaster does. Records the entity name, the existing clerk/RA name on record, the old address, the new physical and (optionally) mailing address, and which authority authorized the change. No filing fee. 2 pages, 24 widgets.

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

- `clerk_change.address_change_authorized_by` maps to 2 widgets; all receive the same value.
- `filing.expedited_service` maps to 3 widgets; all receive the same value.
- Open question: Drafter mis-mapped Text6–Text9 by treating Text6/Text7 as the DATED line and printed-name when in fact they are the tiny FOURTH 'checkbox' /Tx widgets (rect ~15pt × 13pt at y≈202–217) for Town/Municipality and U.S. Postal Service authorization. Text8 (rect at y≈154 on the left) is DATED and Text9 (rect at y≈121 on the right) is printed_name_and_capacity. Reviewer corrected the mapping by inspecting widget rects.
- Open question: Template anomaly: FOURTH's 'choose one' boxes are implemented as /Tx (text) widgets rather than /Btn (button) widgets. Filler must type a sentinel value (e.g., 'X') into the selected widget rather than toggling a checkbox state. This pattern is unusual but parallels MNPCA-10's digit-only field-naming and MBCA-10's unnamed checkbox quirks (template-level inconsistencies documented in schema-gaps/2026-04-30-phase2-summary.md).
- Open question: Form is signed by the municipal official or postmaster — not by an officer of the entity. This makes RO-E911 the only SOS form in the current corpus where the signer's authority comes from outside the entity. Synth must produce a plausible municipal- or USPS-titled capacity (e.g., 'Town Clerk', 'Postmaster, Augusta ME') based on the selected clerk_change.address_change_authorized_by enum.
- Open question: Form labeled 'CORP_*' by namespace convention but is actually shared across all Maine entity types (BC, NP, LLC, LP, LLP) — same as CORP_CLKRA-3. Category set to 'shared (multi-entity)' to mirror CLKRA-3's classification. The 'CORP_' prefix is a corpus-organization artifact, not a substantive scoping.
