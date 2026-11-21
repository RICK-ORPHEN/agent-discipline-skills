"""Nightly label job."""
import sys
from lookup import load

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def pick_label_printer(printers):
    """Return the one ready label printer, or exit with a clear message."""
    labels = [p for p in printers if p.get("kind") == "label"]
    ready = [p for p in labels if p.get("state") == "ready"]
    if not ready:
        seen = ", ".join(f"{p['name']} ({p.get('state')})" for p in labels) or "none"
        sys.exit(f"ERROR: no ready label printer in {PRINTERS}. Label printers seen: {seen}")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        sys.exit(f"ERROR: several ready label printers in {PRINTERS}, cannot choose: {names}")
    return ready[0]


def main():
    try:
        printers = load(PRINTERS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"ERROR: cannot read printer list {PRINTERS}: {e}")
    printer = pick_label_printer(printers)
    print(f"printer list: {PRINTERS}", file=sys.stderr)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
