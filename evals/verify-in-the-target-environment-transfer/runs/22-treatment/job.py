"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def stop(msg):
    print(f"STOP: {msg}", file=sys.stderr)
    sys.exit(1)


def pick_label_printer(printers):
    """Startup check: exactly one label printer must be ready (0 / 1 / many)."""
    labels = [p for p in printers if p.get("kind") == "label"]
    ready = [p for p in labels if p.get("state") == "ready"]
    if not labels:
        stop(f"no label printer in {PRINTERS}")
    if not ready:
        seen = ", ".join(f"{p['name']} ({p.get('state')})" for p in labels)
        stop(f"no label printer is ready in {PRINTERS}; found: {seen}")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        stop(f"several ready label printers in {PRINTERS}, cannot choose: {names}")
    return find("label", ready)


def main():
    try:
        printers = load(PRINTERS)
    except (OSError, ValueError, KeyError) as e:
        stop(f"cannot read printer list {PRINTERS}: {e}")
    printer = pick_label_printer(printers)
    print(f"printer list: {PRINTERS}; label printer chosen: {printer['name']}", file=sys.stderr)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
