"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def require_label_printer(printers):
    """Stop with a clear message unless exactly one label printer is ready."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    print(f"  printer list used: {PRINTERS}", file=sys.stderr)
    if not ready:
        seen = ", ".join(f"{p['name']} ({p['state']})" for p in labels) or "none"
        sys.exit(f"ERROR: no ready label printer in {PRINTERS}. Label printers seen: {seen}")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        sys.exit(f"ERROR: several ready label printers in {PRINTERS}, cannot choose: {names}")
    return ready[0]


def main():
    printers = load(PRINTERS)
    printer = require_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
