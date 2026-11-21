"""Nightly label job."""
import sys
from lookup import load

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"
# Optional: name of the label printer to use when several are ready.
WANTED = sys.argv[2] if len(sys.argv) > 2 else None


def stop(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def pick_label_printer(printers):
    """Startup check: exactly one usable (ready) label printer, or stop."""
    labels = [p for p in printers if p.get("kind") == "label"]
    ready = [p for p in labels if p.get("state") == "ready"]
    print(f"  printer list: {PRINTERS}", file=sys.stderr)
    print("  label printers: "
          + (", ".join(f"{p['name']}={p['state']}" for p in labels) or "(none)"),
          file=sys.stderr)
    if WANTED:
        chosen = [p for p in labels if p["name"] == WANTED]
        if not chosen:
            stop(f"requested label printer '{WANTED}' is not in {PRINTERS}")
        if chosen[0]["state"] != "ready":
            stop(f"requested label printer '{WANTED}' is {chosen[0]['state']}, not ready")
        return chosen[0]
    if not labels:
        stop(f"no label printer in {PRINTERS}; nothing was printed")
    if not ready:
        stop(f"label printer(s) exist but none is ready in {PRINTERS}; nothing was printed")
    if len(ready) > 1:
        stop("several ready label printers, cannot choose: "
             + ", ".join(p["name"] for p in ready)
             + ". Pass the printer name as the second argument.")
    return ready[0]


def main():
    printers = load(PRINTERS)
    printer = pick_label_printer(printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
