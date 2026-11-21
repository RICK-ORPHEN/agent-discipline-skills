"""Nightly label job."""
import os
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def stop(msg):
    print(f"STOP: {msg}", file=sys.stderr)
    sys.exit(1)


def pick_label_printer(printers):
    """Return the one ready label printer, or stop with a clear message.

    0 ready -> stop; several ready -> stop unless LABEL_PRINTER names one.
    """
    labels = [p for p in printers if p["kind"] == "label"]
    ready = [p for p in labels if p["state"] == "ready"]
    wanted = os.environ.get("LABEL_PRINTER")
    if wanted:
        ready = [p for p in ready if p["name"] == wanted]
        if not ready:
            stop(f"LABEL_PRINTER={wanted!r} is not a ready label printer in {PRINTERS} "
                 f"(label printers: {[(p['name'], p['state']) for p in labels]})")
    if not ready:
        seen = ", ".join(f"{p['name']}={p['state']}" for p in labels) or "none"
        stop(f"no ready label printer in {PRINTERS} (label printers: {seen})")
    if len(ready) > 1:
        stop(f"several ready label printers in {PRINTERS}, cannot choose: "
             f"{', '.join(p['name'] for p in ready)}. Set LABEL_PRINTER to one of them.")
    return find("label", ready)


def main():
    printers = load(PRINTERS)
    printer = pick_label_printer(printers)
    print(f"printer list: {PRINTERS}; chosen: {printer['name']}", file=sys.stderr)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
