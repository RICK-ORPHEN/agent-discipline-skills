"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def stop(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def pick_label_printer(printers):
    """Startup check: exactly one label printer must be ready (0 / 1 / many)."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if not ready:
        seen = ", ".join(f"{p['name']} ({p['state']})" for p in labels) or "none listed"
        stop(f"no ready label printer in {PRINTERS}. Label printers: {seen}")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        stop(f"several ready label printers in {PRINTERS}, cannot choose: {names}")
    return find("label", ready)


def main():
    printers = load(PRINTERS)
    printer = pick_label_printer(printers)
    print(f"  printer list used: {PRINTERS}", file=sys.stderr)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
