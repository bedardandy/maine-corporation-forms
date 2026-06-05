# Licensing

This repository mixes material with different appropriate licenses.

## 1. The blank PDF forms

The blank forms are public records of the **Maine Secretary of State**, Bureau
of Corporations, Elections and Commissions, distributed by the state as fillable
AcroForm PDFs for public use. To avoid re-hosting them, the blanks are fetched on
demand (`tools/fetch_pdfs.py`) and verified against the SHA-256, byte size, and
page count in `catalog/pdf_manifest.json`. All 156 are fetched on demand; none is
committed to this repository. See `PROVENANCE.md`.

A `NOTICE` attributing the forms to the Maine Secretary of State is appropriate
for any built artifacts that embed them.

## 2. Code + form metadata/schemas/skills/mappings — Apache-2.0

The repository's own work — code (`engine/`, `tools/`) and the structured form
artifacts (`forms/*/` non-PDF, `catalog/`, `docs/`) — is licensed
**Apache-2.0** (see the `LICENSE` file). Permissive, with an explicit patent
grant, so firms, clinics, the state, and commercial tools can reuse it.

## Structure

```
LICENSE              -> Apache-2.0 (this project's code + metadata)
forms/<ID>/<ID>.pdf  -> Maine Secretary of State public form, fetched on demand
                        (see PROVENANCE.md; never committed here)
```

Copyright 2026 the maine-corporation-forms contributors. The official blank
PDFs remain Maine Secretary of State public records.
