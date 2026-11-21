"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"

def main():
    printers = load(PRINTERS)
    ready = [p for p in printers if p["kind"] == "label" and p["state"] == "ready"]
    if not ready:
        sys.exit("startup check failed: no ready label printer")
    if len(ready) > 1:
        print("warning: several ready label printers: " + ", ".join(p["name"] for p in ready),
              file=sys.stderr)
    printer = ready[0]
    print(f"printing on {printer['name']} ({printer['state']})")


if __name__ == "__main__":
    main()

