"""Opus 4.8 adjudication: a visual pass and a form-logic pass.

Opus is the precise adjudicator (the expensive half); deterministic checks
(coverage, signer rules, overflow detection) already ran upstream and are the
oracle for anything mechanical. Opus is asked only for judgment that needs a
reader: does the rendered form read correctly, and are the answers coherent.

Both passes return structured verdicts. When Opus is unavailable (offline / no
key) they return a ``skipped`` verdict so the pipeline still completes.
"""

from __future__ import annotations

import json
import os

from . import llm

_VISUAL_SYS = (
    "You are a meticulous document-QA reviewer for U.S. state business filings. "
    "You are shown rendered pages of a filled PDF form. Judge ONLY what you can "
    "see. Report any field whose text is clipped, overflowing its box, "
    "overlapping other text, or placed in the wrong area; any checkbox marked in "
    "the wrong place; and whether the signature line is correctly left blank for "
    "a wet-ink signature. If a page is a 'SCHEDULE' continuation, confirm it is "
    "legible and references a field. Respond ONLY with JSON."
)

_VISUAL_SCHEMA = (
    '{"reads_correctly": bool, "issues": [{"page": int, "field_or_area": str, '
    '"problem": str, "severity": "low|medium|high"}], "notes": str}'
)

_LOGIC_SYS = (
    "You are a corporate-filings analyst checking a filled Maine SoS form for "
    "logical and legal coherence (not formatting). Given the form's purpose, the "
    "filled field values, the signer rules, and the rubric checks, find "
    "contradictions, wrong party in wrong role, signer capacity inconsistent "
    "with how the person appears elsewhere, out-of-order or impossible dates, "
    "conditional sections that don't agree, and required-when violations. "
    "Deterministic facts (a chosen enum value, a party index) are NOT problems. "
    "Respond ONLY with JSON."
)

_LOGIC_SCHEMA = (
    '{"coherent": bool, "issues": [{"keys": [str], "problem": str, '
    '"severity": "low|medium|high"}], "notes": str}'
)


def visual_pass(form_id: str, png_paths, *, max_pages: int = 8) -> dict:
    # AUDIT_VISION_BACKEND=qwen runs the visual pass on the local vision cluster
    # (e.g. qwen3.6-27b) instead of Opus — free and offline.
    use_qwen = os.environ.get("AUDIT_VISION_BACKEND") == "qwen" and llm.qwen_available()
    if not use_qwen and not llm.opus_available():
        return {"status": "skipped", "reason": "no_vision_model"}
    text = (
        f"Form: {form_id}. Review the {len(png_paths)} rendered page image(s). "
        f"Respond ONLY with JSON matching: {_VISUAL_SCHEMA}"
    )
    images = list(png_paths)[:max_pages]
    try:
        if use_qwen:
            raw = llm.qwen_vision(_VISUAL_SYS, text, image_paths=images)
        else:
            raw = llm.opus_message(_VISUAL_SYS, text, image_paths=images)
    except llm.LLMUnavailable as e:
        return {"status": "error", "reason": str(e)}
    verdict = llm.extract_json(raw)
    if verdict is None:
        return {"status": "unparsed", "raw": raw[:1000]}
    verdict["status"] = "ok"
    return verdict


def logic_pass(form_id: str, *, title: str, values: dict, rules: dict, rubric_checks) -> dict:
    # AUDIT_LOGIC_BACKEND=qwen runs the form-logic pass on the local cluster.
    use_qwen = os.environ.get("AUDIT_LOGIC_BACKEND") == "qwen" and llm.qwen_available()
    if not use_qwen and not llm.opus_available():
        return {"status": "skipped", "reason": "no_logic_model"}
    payload = {
        "form_id": form_id,
        "title": title,
        "signer_rules": {
            "signature_mode": rules.get("signature_mode"),
            "allowed_signer_capacities": rules.get("allowed_signer_capacities"),
        },
        "filled_values": values,
        "rubric_checks": rubric_checks,
    }
    text = (
        "Check this filled form for logical/legal coherence. Data:\n"
        + json.dumps(payload, indent=2)
        + f"\n\nRespond ONLY with JSON matching: {_LOGIC_SCHEMA}"
    )
    try:
        raw = llm.qwen_chat(_LOGIC_SYS, text) if use_qwen else llm.opus_message(_LOGIC_SYS, text)
    except llm.LLMUnavailable as e:
        return {"status": "error", "reason": str(e)}
    verdict = llm.extract_json(raw)
    if verdict is None:
        return {"status": "unparsed", "raw": raw[:1000]}
    verdict["status"] = "ok"
    return verdict
