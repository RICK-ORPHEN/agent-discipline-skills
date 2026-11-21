"""Nightly label job."""
import sys
from lookup import load

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def require_label_printer(printers):
    """Stop with a clear message unless a label printer is ready."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if ready:
        return ready[0]
    if not labels:
        sys.exit(f"startup check failed: no label printer in {PRINTERS}")
    seen = ", ".join(f"{p['name']} ({p['state']})" for p in labels)
    sys.exit(f"startup check failed: no label printer is ready in {PRINTERS}: {seen}")


def main():
    printers = load(PRINTERS)
    printer = require_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
