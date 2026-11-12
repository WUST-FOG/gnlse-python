"""Run every example in a separate Python process (Windows and Linux)."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = sorted((ROOT / "examples").glob("*.py"))

if not EXAMPLES:
    raise SystemExit("No Python examples were found")

for example in EXAMPLES:
    print(f"Running {example.name}", flush=True)
    subprocess.run([sys.executable, str(example)], cwd=ROOT, check=True)

print(f"All {len(EXAMPLES)} examples completed successfully")
