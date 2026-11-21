"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"

def main():
    printers = load(PRINTERS)
    labels = [p for p in printers if p["kind"] == "label"]
    if not labels:
        sys.exit("startup check failed: no label printer")
    if len(labels) > 1:
        sys.exit("startup check failed: several label printers, cannot choose: "
                 + ", ".join(p["name"] for p in labels))
    printer = labels[0]
    print(f"printing on {printer['name']} ({printer['state']})")


if __name__ == "__main__":
    main()

