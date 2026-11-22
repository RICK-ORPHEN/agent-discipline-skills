"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"


def main():
    printers = load(PRINTERS)
    printer = find("label", printers)
    print(f"printing on {printer['name']} ({printer['state']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
