"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def stop(msg):
    print(f"STOP: {msg}", file=sys.stderr)
    sys.exit(1)


def check_label_printer(printers):
    """Startup check: exactly one label printer must be ready (0 / 1 / many)."""
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    if not ready:
        seen = ", ".join(f"{p['name']}={p['state']}" for p in labels) or "none listed"
        stop(f"no ready label printer in {PRINTERS} (label printers: {seen}). Nothing was printed.")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        stop(f"several ready label printers in {PRINTERS}, cannot choose: {names}. Nothing was printed.")
    return ready[0]


def main():
    printers = load(PRINTERS)
    printer = check_label_printer(printers)
    print(f"  printer list: {PRINTERS}; label printer chosen: {printer['name']}", file=sys.stderr)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
