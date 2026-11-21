"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def require_label_printer(printers):
    """Return a label printer that is ready, or exit with a clear message."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if ready:
        return find("label", ready)
    if not labels:
        sys.exit(f"ERROR: no label printer found in {PRINTERS}; cannot print shipping labels.")
    status = ", ".join(f"{p['name']} ({p['state']})" for p in labels)
    sys.exit(f"ERROR: no label printer is ready in {PRINTERS}: {status}")


def main():
    printers = load(PRINTERS)
    printer = require_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
