"""Qwen + Opus testing loop for Maine SoS business-entity forms.

A two-model pipeline that exercises the fill engine end to end:

* **Qwen** (free, local) generates diverse filing *scenarios*; a deterministic
  step injects synthetic identities so no model-invented or real-world entity
  data ever enters a case.
* **Opus** adjudicates in two passes -- a *visual* pass (does the rendered form
  read right?) and a *form-logic* pass (are the answers legally coherent?).

Everything in between -- coverage gating, signer-rule validation, fill, render --
is deterministic. Endpoints are read from environment variables; nothing here
hard-codes a host. See ``tools/audit/README.md``.
"""

from __future__ import annotations

__all__ = ["synthetic", "llm", "factgen", "render", "audit", "run"]
