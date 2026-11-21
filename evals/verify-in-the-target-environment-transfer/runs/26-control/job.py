"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def main():
    printers = load(PRINTERS)
    # Startup check: only consider label printers that are ready, and stop
    # with a clear message if there are none (find() ignores state).
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if not ready:
        seen = ", ".join(f"{p['name']} ({p['state']})" for p in labels) or "none listed"
        sys.exit(f"ERROR: no ready label printer in {PRINTERS}. Label printers: {seen}")
    printer = find("label", ready)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
