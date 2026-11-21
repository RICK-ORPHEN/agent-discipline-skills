"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def require_label_printer(printers):
    """Return a label printer that is ready, or exit with a clear message."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if not ready:
        if labels:
            found = ", ".join(f"{p['name']} ({p['state']})" for p in labels)
            detail = f"label printers found but none ready: {found}"
        else:
            detail = "no label printer in the list"
        sys.exit(f"ERROR: cannot run label job with {PRINTERS}: {detail}")
    return find("label", ready)


def main():
    printers = load(PRINTERS)
    printer = require_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
