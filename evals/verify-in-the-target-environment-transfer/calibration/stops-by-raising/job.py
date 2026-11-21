"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"

def main():
    printers = load(PRINTERS)
    ready = [p for p in printers if p["kind"] == "label" and p["state"] == "ready"]
    if len(ready) != 1:
        raise RuntimeError("expected exactly one ready label printer, found: "
                           + (", ".join(p["name"] for p in ready) or "none"))
    printer = ready[0]
    print(f"printing on {printer['name']} ({printer['state']})")


if __name__ == "__main__":
    main()

