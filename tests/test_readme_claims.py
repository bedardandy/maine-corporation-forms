"""Per-form README mechanical claims must match the live mapping.json.

tools/audit_readme_claims.py checks every claim a README makes that is
derivable from mapping.json (fan-out lines, low-confidence lists, the
"Mapped fields" header) and exits non-zero when any is provably stale.
This pins the invariant so a remap round can't silently strand README
boilerplate again. After an intentional remap, refresh the lines with:

    python3 tools/audit_readme_claims.py --fix
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_no_stale_mechanical_readme_claims():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "audit_readme_claims.py"),
         "--quiet"],
        capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 0, (
        "stale mechanical README claims; refresh with "
        "`python3 tools/audit_readme_claims.py --fix`:\n"
        + proc.stdout + proc.stderr)
