"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


def check_credentials(creds):
    """Stop at startup, with a clear message, if no supabase credential exists."""
    if not any(c.get("provider") == "supabase" for c in creds):
        sys.exit(f"startup check failed: no supabase credential in {CREDS}; "
                 "the nightly export needs one. Aborting before doing any work.")


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credentials from {CREDS}: {e}")
    check_credentials(creds)
    cred = resolve("supabase", creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
