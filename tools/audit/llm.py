"""Minimal, dependency-free clients for the models in the audit loop.

* Qwen via an OpenAI-compatible chat endpoint (a local cluster serves this).
  ``qwen_chat`` is text-only; ``qwen_vision`` sends rendered pages, so a vision
  Qwen (e.g. qwen3.6-27b) can run the visual pass locally instead of Opus.
* Opus via the Anthropic Messages API (also supports image input).

Both use only the standard library (``urllib``) so the loop adds no third-party
dependency. Endpoints and keys come from the environment -- nothing here names a
host:

  Qwen:  AUDIT_QWEN_BASE_URL     (e.g. http://HOST:PORT/v1)
         AUDIT_QWEN_MODEL        (text model; default: qwen)
         AUDIT_QWEN_VISION_MODEL (vision model for qwen_vision; default: text model)
         AUDIT_QWEN_API_KEY      (optional)

  Opus:  ANTHROPIC_API_KEY    (required for live Opus)
         AUDIT_OPUS_MODEL     (default: claude-opus-4-8)
         AUDIT_OPUS_BASE_URL  (default: https://api.anthropic.com)

The visual pass picks its backend from AUDIT_VISION_BACKEND (``qwen`` routes it
to the local cluster; otherwise Opus). Thinking traces are disabled via
``chat_template_kwargs.enable_thinking=false`` for Qwen3.x models.

If ``AUDIT_OFFLINE=1`` (or an endpoint/key is missing) the clients report
unavailable so the pipeline skips the model passes and still completes.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request


class LLMUnavailable(RuntimeError):
    pass


def _post_json(url: str, headers: dict, payload: dict, timeout: float = 120.0) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise LLMUnavailable(f"HTTP {e.code}: {body[:500]}") from e
    except Exception as e:  # connection refused, timeout, DNS, ...
        raise LLMUnavailable(str(e)) from e


def _offline() -> bool:
    return os.environ.get("AUDIT_OFFLINE") == "1"


# --------------------------------------------------------------------------- #
# Qwen (OpenAI-compatible chat completions)
# --------------------------------------------------------------------------- #
def qwen_available() -> bool:
    return bool(os.environ.get("AUDIT_QWEN_BASE_URL")) and not _offline()


def qwen_chat(system: str, user: str, *, max_tokens: int = 2048, temperature: float = 0.4) -> str:
    if not qwen_available():
        raise LLMUnavailable("Qwen endpoint not configured (set AUDIT_QWEN_BASE_URL).")
    base = os.environ["AUDIT_QWEN_BASE_URL"].rstrip("/")
    url = f"{base}/chat/completions"
    headers = {"Content-Type": "application/json"}
    key = os.environ.get("AUDIT_QWEN_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    payload = {
        "model": os.environ.get("AUDIT_QWEN_MODEL", "qwen"),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        # Disable thinking traces where the server honors it (Qwen3.x).
        "chat_template_kwargs": {"enable_thinking": False},
    }
    resp = _post_json(url, headers, payload)
    return resp["choices"][0]["message"]["content"]


def qwen_vision(system: str, user: str, image_paths=None, *,
                max_tokens: int = 1024, temperature: float = 0.0,
                timeout: float = 180.0) -> str:
    """Visual pass on the local cluster (a vision Qwen, e.g. qwen3.6-27b).

    Sends one or more rendered PNGs plus a prompt via the OpenAI-compatible
    image_url block format, so the free local cluster can read back a filled
    form instead of calling a paid vision model.
    """
    if not qwen_available():
        raise LLMUnavailable("Qwen endpoint not configured (set AUDIT_QWEN_BASE_URL).")
    base = os.environ["AUDIT_QWEN_BASE_URL"].rstrip("/")
    headers = {"Content-Type": "application/json"}
    key = os.environ.get("AUDIT_QWEN_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    content = [{"type": "text", "text": user}]
    for p in image_paths or []:
        b64 = base64.b64encode(open(p, "rb").read()).decode("ascii")
        content.append({"type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}"}})
    payload = {
        "model": os.environ.get("AUDIT_QWEN_VISION_MODEL",
                                os.environ.get("AUDIT_QWEN_MODEL", "qwen")),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": content},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    resp = _post_json(f"{base}/chat/completions", headers, payload, timeout=timeout)
    return resp["choices"][0]["message"]["content"]


# --------------------------------------------------------------------------- #
# Opus (Anthropic Messages API, with optional images)
# --------------------------------------------------------------------------- #
def _use_cli_backend() -> bool:
    return os.environ.get("AUDIT_OPUS_BACKEND") == "claude_cli"


def opus_available() -> bool:
    if _offline():
        return False
    if _use_cli_backend():
        from . import claude_cli

        return claude_cli.available()
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _image_block(png_path: str) -> dict:
    raw = open(png_path, "rb").read()
    b64 = base64.b64encode(raw).decode("ascii")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": "image/png", "data": b64},
    }


def opus_message(system: str, text: str, image_paths=None, *, max_tokens: int = 2048) -> str:
    if not opus_available():
        raise LLMUnavailable("Opus not configured (set ANTHROPIC_API_KEY).")
    if _use_cli_backend():
        from . import claude_cli

        try:
            return claude_cli.message(system, text, image_paths, max_tokens=max_tokens)
        except claude_cli.CLIError as e:
            raise LLMUnavailable(str(e)) from e
    base = os.environ.get("AUDIT_OPUS_BASE_URL", "https://api.anthropic.com").rstrip("/")
    url = f"{base}/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
    }
    content = []
    for p in image_paths or []:
        content.append(_image_block(p))
    content.append({"type": "text", "text": text})
    payload = {
        "model": os.environ.get("AUDIT_OPUS_MODEL", "claude-opus-4-8"),
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": content}],
    }
    resp = _post_json(url, headers, payload, timeout=180.0)
    parts = [b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text"]
    return "".join(parts)


# --------------------------------------------------------------------------- #
# Robust JSON extraction (models wrap JSON in prose / fences)
# --------------------------------------------------------------------------- #
def extract_json(text: str):
    """Best-effort parse of a JSON object/array embedded in model output."""
    text = (text or "").strip()
    if not text:
        return None
    if text.startswith("```"):
        text = text.split("```", 2)[1] if text.count("```") >= 2 else text
        if text.lstrip().startswith("json"):
            text = text.lstrip()[4:]
    try:
        return json.loads(text)
    except Exception:
        pass
    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        if start < 0:
            continue
        depth = 0
        for i in range(start, len(text)):
            if text[i] == opener:
                depth += 1
            elif text[i] == closer:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except Exception:
                        break
    return None
