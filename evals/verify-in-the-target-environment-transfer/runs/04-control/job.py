"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def main():
    printers = load(PRINTERS)
    # Startup check: need a label printer that is ready, not just any label printer.
    ready = [p for p in printers if p["kind"] == "label" and p["state"] == "ready"]
    if not ready:
        labels = [f"{p['name']} ({p['state']})" for p in printers if p["kind"] == "label"]
        found = ", ".join(labels) if labels else "none listed"
        sys.exit(f"ERROR: no ready label printer in {PRINTERS}. Label printers found: {found}.")
    printer = find("label", ready)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
