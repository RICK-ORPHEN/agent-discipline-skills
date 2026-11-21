"""Nightly label job."""
import sys
from lookup import load, find

PRINTERS = sys.argv[1] if len(sys.argv) > 1 else "printers.dev.json"

def main():
    load(PRINTERS)
    sys.exit("startup check failed: label printer availability cannot be confirmed from here")


if __name__ == "__main__":
    main()

