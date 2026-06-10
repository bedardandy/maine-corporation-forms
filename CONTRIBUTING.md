# Contributing

This library is built form-by-form. The smallest useful contribution is
improving a single form folder; the most valuable is verifying a mapping against
a real filled output. You never need to touch the whole repo to improve one form.

## The inner loop: improve one form

Pick a form, edit `forms/<ID>/mapping.json`, and validate that one form. The
validator is offline and needs no blank PDF:

```bash
python3 tools/validate_form.py CORP_MBCA-6     # one form, verbose
make validate FORM=CORP_MBCA-6                  # same, via make
make coverage                                   # every form + the review worklist
```

It checks each mapped field against the form's widget inventory (`fields.csv`)
and JSON Schema, prints the confidence mix, and flags review items: a widget the
inventory does not list, a key not yet in `schema.json`, a low-confidence field,
or an unsupported `when` expression. Those review items are the worklist. The
validator exits non-zero only on structural breakage, which is the same gate CI
runs (`make test`).

## Verifying a mapping (the high-value work)

A form is **production-ready** when its `mapping.json` is verified against real
output, not only auto-derived:

1. Build a synthetic case-data object that exercises the form's fields (see the
   model in `docs/data-model.md`; reuse canonical keys, do not invent them).
2. Plan it — `python3 -m engine.plan <ID> case.json` — to see coverage with no
   PDF.
3. Fetch the blank and fill it: `python3 -m engine.fill <ID> case.json out.pdf`.
4. Open `out.pdf` and check every value lands in the right widget.
5. Fix `widget_id` / `field_type` where placement is wrong, then raise the
   per-field `confidence` to `high`.

`CORP_MBCA-6` is the reference hand-curated form — match its mapping shape. A
verified mapping plus a worked example in `examples/` is the gold standard.

## Mapping quality bar

- `form.yaml` is the source of truth; catalogs and per-form `README.md` /
  `SKILL.md` are generated views — regenerate, don't hand-edit.
- `confidence: low` means auto-derived and **not** trusted.
- Cross-check every `widget_id` against the real AcroForm field names.
- Reuse canonical keys from `docs/field-schema.md` / `docs/data-model.md` so
  mappings stay portable across forms and adapters.
- Enum and radio fields bind each value to a widget via an `options` map; keep
  the `options` values in sync with the schema `enum`.
- After adding a mapping key, run `python3 tools/sync_schema.py <ID>` (or
  `make sync-schema`) to extend `schema.json` to cover it.

## Regenerating from source (maintainers)

The per-form folders are generated from upstream source data (the blank PDFs plus
pass-1 field-mapping analysis), which is not part of this public repo. With those
inputs, `tools/build_from_pass1.py --pdf-dir ... --pass1-dir ...` rewrites the
per-form artifacts and the `catalog/` indices idempotently. Hand-maintained forms
(`tools/HAND_MAINTAINED.txt`) are skipped unless forced. Most contributions edit
a single `mapping.json` directly and do not need the generator.

## Scope discipline

One form (or one entity-type family) per PR. Keep engine changes separate from
form-data changes. Keep filled PDFs and run artifacts out of git (`.gitignore`).

## Clean-room hygiene (this repo is public)

No absolute local paths, host names, internal infrastructure, or real
entity/agent names in committed files. Examples use synthetic data only.
