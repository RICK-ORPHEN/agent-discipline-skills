"""Nightly label job."""
import sys
from lookup import load

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"
# Optional 2nd argument: name of the label printer to use when several are ready.
WANTED = sys.argv[2] if len(sys.argv) > 2 else None


def stop(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def pick_label_printer(printers, wanted=None):
    """Return the one ready label printer, or stop with a clear message."""
    labels = [p for p in printers if p.get("kind") == "label"]
    if not labels:
        stop(f"no label printer in {PRINTERS}")
    ready = [p for p in labels if p.get("state") == "ready"]
    if wanted:
        named = [p for p in labels if p.get("name") == wanted]
        if not named:
            stop(f"label printer '{wanted}' not in {PRINTERS}")
        if named[0].get("state") != "ready":
            stop(f"label printer '{wanted}' is {named[0].get('state')}, not ready")
        return named[0]
    if not ready:
        states = ", ".join(f"{p['name']}={p.get('state')}" for p in labels)
        stop(f"no label printer is ready in {PRINTERS} ({states})")
    if len(ready) > 1:
        names = ", ".join(p["name"] for p in ready)
        stop(f"several ready label printers, cannot choose: {names}. "
             "Pass the printer name as the 2nd argument.")
    return ready[0]


def main():
    printers = load(PRINTERS)
    printer = pick_label_printer(printers, WANTED)
    print(f"printer list: {PRINTERS}; chosen: {printer['name']}", file=sys.stderr)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
