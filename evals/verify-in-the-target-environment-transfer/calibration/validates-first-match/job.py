"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"

def main():
    printers = load(PRINTERS)
    if not [p for p in printers if p["kind"] == "label"]:
        sys.exit("startup check failed: no label printer")
    printer = find("label", printers)
    if printer["state"] != "ready":
        sys.exit(f"startup check failed: {printer['name']} is {printer['state']}")
    print(f"printing on {printer['name']} ({printer['state']})")


if __name__ == "__main__":
    main()

