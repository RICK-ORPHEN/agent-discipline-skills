"""Printer lookup."""
import json


def load(path):
    with open(path) as f:
        return json.load(f)["printers"]


def find(kind, printers):
    """Return the printer of a kind."""
    matches = [p for p in printers if p["kind"] == kind]
    return matches[0]
