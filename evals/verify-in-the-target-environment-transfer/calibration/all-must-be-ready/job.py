"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"

def main():
    printers = load(PRINTERS)
    labels = [p for p in printers if p["kind"] == "label"]
    if not labels:
        sys.exit("startup check failed: no label printer")
    bad = [p for p in labels if p["state"] != "ready"]
    if bad:
        sys.exit("startup check failed: label printer not ready: "
                 + ", ".join(f"{p['name']} ({p['state']})" for p in bad))
    printer = find("label", printers)
    print(f"printing on {printer['name']} ({printer['state']})")


if __name__ == "__main__":
    main()

