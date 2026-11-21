"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def main():
    try:
        printers = load(PRINTERS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"ERROR: cannot read printer list {PRINTERS!r}: {e}")

    # Startup check: we need a label printer that is ready. Look only at
    # ready ones so an offline/paused label printer is never picked.
    ready = [p for p in printers if p.get("state") == "ready"]
    try:
        printer = find("label", ready)
    except IndexError:
        labels = [f"{p['name']} ({p['state']})" for p in printers if p.get("kind") == "label"]
        found = ", ".join(labels) if labels else "none listed"
        sys.exit(
            f"ERROR: no ready label printer in {PRINTERS}. "
            f"Label printers found: {found}. Nothing was printed."
        )

    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
