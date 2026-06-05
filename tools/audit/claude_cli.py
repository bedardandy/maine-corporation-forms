"""Headless Claude Code backend for the Opus adjudication passes.

When ``AUDIT_OPUS_BACKEND=claude_cli`` the audit loop drives Opus through the
locally installed ``claude`` CLI (``claude -p``) instead of the Anthropic
Messages API. This uses the machine's existing Claude Code session credentials,
so it works where a raw ``ANTHROPIC_API_KEY`` is unavailable or rejected.

The CLI reads page images with its own ``Read`` tool: image paths are listed in
the prompt and the tool is allowed for exactly the directories that hold them.
The broken/absent ``ANTHROPIC_API_KEY`` is stripped from the child environment
so the CLI falls back to session auth rather than the key.

Nothing here hardcodes a host, path, or credential.
"""

from __future__ import annotations

import json
import os
import subprocess


class CLIError(RuntimeError):
    pass


def available() -> bool:
    """True if the ``claude`` CLI is on PATH and not disabled by AUDIT_OFFLINE."""
    if os.environ.get("AUDIT_OFFLINE") == "1":
        return False
    from shutil import which

    return which("claude") is not None


def message(system: str, text: str, image_paths=None, *, max_tokens: int = 2048,
            timeout: float = 600.0) -> str:
    """Run one headless Claude turn and return its text result.

    ``image_paths`` are read by the CLI's own Read tool; ``max_tokens`` is
    accepted for interface parity with the API client (the CLI manages its own
    output budget).
    """
    paths = [os.path.abspath(p) for p in (image_paths or [])]
    prompt = text
    if paths:
        listing = "\n".join(f"- {p}" for p in paths)
        prompt = (
            f"{text}\n\nRead these rendered page image(s) with the Read tool and "
            f"judge ONLY what you can see:\n{listing}"
        )

    env = dict(os.environ)
    # Force session auth: a present-but-invalid key would otherwise win.
    env.pop("ANTHROPIC_API_KEY", None)

    model = os.environ.get("AUDIT_OPUS_MODEL", "claude-opus-4-8")
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--model", model,
        "--append-system-prompt", system,
    ]
    if paths:
        cmd += ["--allowedTools", "Read"]
        for d in sorted({os.path.dirname(p) for p in paths}):
            cmd += ["--add-dir", d]

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=env,
        )
    except subprocess.TimeoutExpired as e:
        raise CLIError(f"claude CLI timed out after {timeout}s") from e
    except FileNotFoundError as e:
        raise CLIError("claude CLI not found on PATH") from e

    if proc.returncode != 0:
        raise CLIError(
            f"claude CLI rc={proc.returncode}: "
            f"{(proc.stderr or proc.stdout or '')[:400]}"
        )

    try:
        obj = json.loads(proc.stdout)
    except Exception as e:
        raise CLIError(f"claude CLI non-JSON output: {proc.stdout[:400]}") from e

    if obj.get("is_error"):
        raise CLIError(f"claude CLI error: {str(obj.get('result'))[:400]}")
    return obj.get("result", "")
