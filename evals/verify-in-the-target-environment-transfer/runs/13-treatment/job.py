"""Nightly label job."""
import sys
from lookup import load

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def pick_label_printer(printers):
    """Return the one ready label printer, or exit with a clear message."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if not labels:
        sys.exit(f"STARTUP CHECK FAILED: no label printer in {PRINTERS}")
    if not ready:
        seen = ", ".join(f"{p['name']} ({p['state']})" for p in labels)
        sys.exit(f"STARTUP CHECK FAILED: no label printer is ready in {PRINTERS}: {seen}")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        sys.exit(f"STARTUP CHECK FAILED: several ready label printers in {PRINTERS}, "
                 f"cannot choose: {names}")
    return ready[0]


def main():
    printers = load(PRINTERS)
    print(f"printer list used: {PRINTERS}", file=sys.stderr)
    printer = pick_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
