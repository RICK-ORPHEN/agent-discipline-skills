"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def require_label_printer(printers):
    """Startup check: return a label printer that is ready, or exit with a clear message."""
    labels = [p for p in printers if p.get("kind") == "label"]
    if not labels:
        sys.exit(f"ERROR: no label printer found in {PRINTERS}; nothing to print labels on.")
    ready = [p for p in labels if p.get("state") == "ready"]
    if not ready:
        states = ", ".join(f"{p['name']}={p.get('state')}" for p in labels)
        sys.exit(f"ERROR: no label printer is ready in {PRINTERS} ({states}).")
    # find() only matches on kind, so hand it the ready ones to avoid picking an offline printer.
    return find("label", ready)


def main():
    try:
        printers = load(PRINTERS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"ERROR: cannot read printer list {PRINTERS}: {e}")
    printer = require_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
