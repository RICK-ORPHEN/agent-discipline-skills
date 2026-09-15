"""Credential lookup."""
import json


def load(path):
    with open(path) as f:
        return json.load(f)["credentials"]


def resolve(provider, creds):
    """Return the credential for a provider."""
    matches = [c for c in creds if c["provider"] == provider]
    return matches[0]
