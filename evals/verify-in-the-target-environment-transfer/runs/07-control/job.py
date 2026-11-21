"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def main():
    try:
        printers = load(PRINTERS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read printer list {PRINTERS!r}: {e}")

    # find() returns the first printer of a kind regardless of state, so only
    # hand it printers that are ready; otherwise an offline/paused label printer
    # listed first would be picked.
    ready = [p for p in printers if p.get("state") == "ready"]
    labels = [p for p in printers if p.get("kind") == "label"]
    if not any(p.get("kind") == "label" for p in ready):
        if labels:
            states = ", ".join(f"{p['name']}={p['state']}" for p in labels)
            sys.exit(f"startup check failed: no label printer is ready in {PRINTERS} ({states})")
        sys.exit(f"startup check failed: no label printer found in {PRINTERS}")

    printer = find("label", ready)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
