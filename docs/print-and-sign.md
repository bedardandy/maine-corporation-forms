# Print fidelity, overflow schedules, signing, and the audit loop

Maine SoS business filings are, in practice, **printed and signed in wet ink**,
and statute restricts **who** may sign. Three layers handle this; the first two
are deterministic, the third adds a two-model review.

## 1. Print-ready copies (`engine/printcopy.py`)

The reference filler sets AcroForm values and `NeedAppearances` but bakes no
appearance streams, so a viewer that ignores `NeedAppearances` can print blank
fields. `printcopy` fixes that with PyMuPDF:

```bash
python3 -m engine.printcopy CORP_MBCA-6 case.json out.pdf
# options: --no-flatten  --no-overflow
```

```python
from engine import printcopy
report = printcopy.fill_print_copy("CORP_MBCA-6", case, "out.pdf")
# {"out": "...", "overflows": [...], "flattened": true}
```

What it does:

1. **Bakes appearances** — regenerates every widget's appearance from its value
   so the rendered text is faithful in any viewer.
2. **Spills overflow to schedules** — a value too long for its field rectangle is
   replaced in place with `See Schedule A (attached)` and the full text is
   appended on a clean, Word-style continuation page (auto-lettered,
   back-referenced to the field). This is how real filings handle overrun, and it
   keeps the official form pages byte-faithful.
3. **Flattens** (default) — converts widgets to static content so the print copy
   prints identically everywhere and cannot be re-edited.

The official blank PDFs are never modified; this runs on a filled *copy*. The
signature *line* stays blank for the pen — flattening never fabricates a
signature, because the only signer fields are for the *printed* name/title/date.

### Why not interactive "add a schedule" buttons?

PDF-JavaScript buttons that spawn template pages were considered and rejected:
they only run in Adobe Acrobat (browser/Preview/mobile and most e-filing portals
ignore or strip JS), they mutate the official PDF (breaking byte-faithfulness),
and **you cannot click a button on a printed page**. Overflow must
be resolved at generation time, which is what the schedule pass does.

## 2. Who may sign (`tools/signer_rules.py`)

Signer rules are encoded as data and validated deterministically rather than left
to a language model:

```bash
python3 -m tools.signer_rules CORP_MBCA-6      # show one form's rules
python3 -m tools.signer_rules build            # write catalog/signer_rules.json
```

```python
from tools import signer_rules
rules = signer_rules.rules_for("LP_MLPA-10")
# {"signature_mode": "wet_ink",
#  "allowed_signer_capacities": ["general partner"], ...}
issues = signer_rules.validate("CORP_MBCA-6",
                               {"signature": {"capacity": "general partner"}})
# [{"severity": "required", "code": "capacity-not-allowed", ...}]
```

Defaults by entity class (grounded in the Maine entity statutes; the form's
printed signature block is authoritative, and a per-form
`forms/<ID>/signer_rules.json` overrides). Formation filings are detected from
the form title (Articles of Incorporation / Organization, Certificate of
Formation / Limited Partnership):

| Entity | Formation/registration | Other filings |
|---|---|---|
| Business corporation (13-C) | incorporator | officer / incorporator / director |
| Nonprofit (13-B) | incorporator | officer / director / incorporator |
| LLC (31) | authorized person / member / manager | same |
| Limited partnership (31) | general partner | general partner |
| LLP (31) | partner / authorized partner | same |
| General partnership (31) | partner | partner |
| Trademark (10) | applicant / officer / authorized person | same |

Agent-designation forms also allow the **registered agent** to sign the
acceptance.

`signature_mode` is `wet_ink` for these filings. The e-sign exporter
(`tools/export/exporters.py`) reads it and refuses to emit a real `signHere`
tab for a wet-ink form — it downgrades the signature to a placeholder and
attaches a `wet_ink_warning`, so the e-sign maps can be used for internal
routing/approval without implying an electronic signature is acceptable for the
actual filing.

## 3. The Qwen + Opus audit loop (`tools/audit/`)

A two-model loop that exercises the whole pipeline and reviews the result. Qwen
(free, local) generates diverse scenarios; deterministic code injects synthetic
identities, gates coverage, and validates signers; a judge adjudicates the
rendered output in two passes — *visual* (does it read right?) and *form-logic*
(are the answers coherent?).

The visual pass can run on **Opus** or, for free, on a **local vision model**.
A vision-capable Qwen (e.g. `qwen3.6-27b`) reads the rendered pages directly, so
the whole loop runs offline on the cluster. Set `AUDIT_VISION_BACKEND=qwen` to
route the visual pass there; `qwen_vision` disables Qwen3.x thinking traces via
`chat_template_kwargs.enable_thinking=false`.

```bash
# Offline: every deterministic stage + render runs; model passes are skipped.
AUDIT_OFFLINE=1 python3 -m tools.audit.run --form CORP_MBCA-6

# Fully local: factgen + visual pass both on the cluster (no paid model).
export AUDIT_QWEN_BASE_URL=http://YOUR_HOST:PORT/v1
export AUDIT_QWEN_MODEL=qwen3.6-27b          # text (factgen)
export AUDIT_QWEN_VISION_MODEL=qwen3.6-27b   # vision (visual pass)
export AUDIT_VISION_BACKEND=qwen
python3 -m tools.audit.run --form CORP_MBCA-6 --qwen

# Or use Opus as the visual/logic judge instead.
export ANTHROPIC_API_KEY=sk-...
export AUDIT_OPUS_MODEL=claude-opus-4-8
python3 -m tools.audit.run --all --limit 20        # broad sweep
```

Per case it emits a verdict with: coverage buckets, signer-gate result (the
`signer_bad` variant must fail; others must pass), detected overflows (the
`overflow` variant must spill a schedule), and the two Opus verdicts. Output goes
to `build/audit/report.json` + `summary.tsv`. Endpoints are read from the
environment; no host is hard-coded, and all generated data is synthetic.
