# Examples

Worked fill examples using synthetic data only. No real entities, registered
agents, or CRA numbers appear here.

## CORP_MBCA-6 — Articles of Incorporation

`corp_mbca-6.case.json` forms a fictional business corporation,
"Wabanaki Widgets, Inc.", with a made-up commercial clerk and a placeholder
CRA public number (`P99999`).

Fill it from the repository root:

```
python3 -m engine.fill CORP_MBCA-6 examples/corp_mbca-6.case.json out.pdf
```

Validate the case data against the form schema first (optional):

```python
import json
from engine import schema
errors = schema.validate("CORP_MBCA-6", json.load(open("examples/corp_mbca-6.case.json")))
assert errors == []
```

The output `out.pdf` is an ordinary filled AcroForm PDF. Open it in any PDF
reader, or read the values back with pypdf to confirm the fields were set.
