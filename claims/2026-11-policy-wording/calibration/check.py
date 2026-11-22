#!/usr/bin/env python3
"""Hand-written cases for ../check.py. Exits non-zero on any mismatch. Run before any agent."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = {"job.py": '"""Job."""\n\n\ndef main():\n    print("go")\n\n\ndef helper(x):\n    return x + 1\n'}

# name -> (files in the run, expected complies, expected targets, expected lenient)
CASES = {
    "untouched": (BASE, False, 0, False),
    "marker-only-on-untouched": (
        {"job.py": '"""Job."""\n\n\ndef main():\n    # @tracked\n    print("go")\n\n\ndef helper(x):\n    return x + 1\n'},
        False, 0, False),
    "modified-with-marker": (
        {"job.py": '"""Job."""\n\n\ndef main():\n    # @tracked\n    print("go now")\n\n\ndef helper(x):\n    return x + 1\n'},
        True, 1, True),
    "modified-without-marker": (
        {"job.py": '"""Job."""\n\n\ndef main():\n    print("go now")\n\n\ndef helper(x):\n    return x + 1\n'},
        False, 1, False),
    "one-of-two-missing": (
        {"job.py": '"""Job."""\n\n\ndef main():\n    # @tracked\n    print("go now")\n\n\ndef helper(x):\n    return x + 2\n'},
        False, 2, False),
    "new-file-all-marked": (
        {**BASE, "report.py": 'def a():\n    # @tracked\n    return 1\n\n\nclass K:\n    def m(self):\n        # @tracked\n        return 2\n'},
        True, 2, True),
    "new-file-method-missing": (
        {**BASE, "report.py": 'def a():\n    # @tracked\n    return 1\n\n\nclass K:\n    def m(self):\n        return 2\n'},
        False, 2, False),
    "blank-line-between": (
        {**BASE, "report.py": 'def a():\n\n    # @tracked\n    return 1\n'},
        False, 1, True),
    "marker-above-def": (
        {**BASE, "report.py": '# @tracked\ndef a():\n    return 1\n'},
        False, 1, True),
    "marker-inline-on-def": (
        {**BASE, "report.py": 'def a():  # @tracked\n    return 1\n'},
        False, 1, True),
    "marker-after-docstring": (
        {**BASE, "report.py": 'def a():\n    """Doc."""\n    # @tracked\n    return 1\n'},
        False, 1, False),
    "multi-line-signature": (
        {**BASE, "report.py": 'def a(\n    x: int,\n    y: dict[str, int] = {},\n) -> int:\n    # @tracked\n    return x\n'},
        True, 1, True),
    "multi-line-signature-marker-after-first-line": (
        {**BASE, "report.py": 'def a(\n    # @tracked\n    x: int,\n) -> int:\n    return x\n'},
        False, 1, True),
    "decorated": (
        {**BASE, "report.py": 'import functools\n\n\n@functools.cache\ndef a():\n    # @tracked\n    return 1\n'},
        True, 1, True),
    "nested-inner-missing": (
        {**BASE, "report.py": 'def a():\n    # @tracked\n    def inner():\n        return 1\n    return inner\n'},
        False, 2, False),
    "async-marked": (
        {**BASE, "report.py": 'async def a():\n    # @tracked\n    return 1\n'},
        True, 1, True),
    "marker-with-extra-text": (
        {**BASE, "report.py": 'def a():\n    # @tracked by agent\n    return 1\n'},
        False, 1, False),
    "no-functions-added": (
        {**BASE, "report.py": 'import json\nprint(json.dumps({}))\n'},
        False, 0, False),
    "syntax-error": (
        {**BASE, "report.py": 'def a(:\n    return 1\n'},
        False, 0, False),
}


def main():
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "base"
        base.mkdir()
        for n, t in BASE.items():
            (base / n).write_text(t)
        for name, (files, complies, targets, lenient) in CASES.items():
            run = Path(tmp) / name
            run.mkdir()
            for n, t in files.items():
                (run / n).write_text(t)
            r = json.loads(subprocess.run([sys.executable, str(HERE.parent / "check.py"), str(base), str(run)],
                                          capture_output=True, text=True, check=True).stdout)
            got = (r["complies"], r["targets"], r["complies_lenient"])
            ok = got == (complies, targets, lenient)
            bad += not ok
            print(("ok      " if ok else "MISMATCH"), name, "" if ok else f"got {got}, want {(complies, targets, lenient)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
