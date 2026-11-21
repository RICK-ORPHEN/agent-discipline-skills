"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


def check_credential(path):
    """Stop early with a clear message if the supabase credential is unavailable."""
    try:
        creds = load(path)
    except FileNotFoundError:
        sys.exit(f"startup check failed: credential file '{path}' not found")
    except (ValueError, KeyError, TypeError) as e:
        sys.exit(f"startup check failed: credential file '{path}' is unreadable or malformed ({type(e).__name__})")
    try:
        cred = resolve("supabase", creds)
    except (IndexError, KeyError, TypeError):
        sys.exit(f"startup check failed: no 'supabase' credential in '{path}'")
    for field in ("alias", "role"):
        if field not in cred:
            sys.exit(f"startup check failed: supabase credential in '{path}' has no '{field}'")
    return cred


def main():
    cred = check_credential(CREDS)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
