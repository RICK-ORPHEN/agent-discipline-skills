"""Nightly label job."""
import sys
from lookup import load

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def require_label_printer(printers):
    """Startup check: exactly one label printer must be ready, else stop with a clear message."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if not labels:
        sys.exit(f"STOP: no label printer in {PRINTERS}.")
    if not ready:
        states = ", ".join(f"{p['name']}={p['state']}" for p in labels)
        sys.exit(f"STOP: no label printer is ready in {PRINTERS} ({states}).")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        sys.exit(f"STOP: several ready label printers in {PRINTERS}, cannot choose: {names}.")
    print(f"  label printer chosen: {ready[0]['name']} (from {PRINTERS})", file=sys.stderr)
    return ready[0]


def main():
    printers = load(PRINTERS)
    printer = require_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
