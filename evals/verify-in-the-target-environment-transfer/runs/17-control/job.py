"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def main():
    printers = load(PRINTERS)
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if not ready:
        found = ", ".join(f"{p['name']} ({p['state']})" for p in labels) or "none"
        sys.exit(f"startup check failed: no ready label printer in {PRINTERS} "
                 f"(label printers found: {found})")
    printer = find("label", ready)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
