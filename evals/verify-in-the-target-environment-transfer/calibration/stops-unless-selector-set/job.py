"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"

import os


def main():
    printers = load(PRINTERS)
    ready = [p for p in printers if p["kind"] == "label" and p["state"] == "ready"]
    want = os.environ.get("LABEL_PRINTER")
    if want:
        ready = [p for p in ready if p["name"] == want]
    if not ready:
        sys.exit("startup check failed: no ready label printer")
    if len(ready) > 1:
        sys.exit("startup check failed: several ready label printers, set LABEL_PRINTER: "
                 + ", ".join(p["name"] for p in ready))
    printer = ready[0]
    print(f"printing on {printer['name']} ({printer['state']})", file=sys.stderr)


if __name__ == "__main__":
    main()

