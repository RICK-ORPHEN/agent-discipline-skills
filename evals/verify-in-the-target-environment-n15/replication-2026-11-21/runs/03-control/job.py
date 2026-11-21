"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


WRITE_ROLES = {"service_role"}


def check_supabase(creds):
    """Stop early unless a supabase credential that can write is available."""
    sb = [c for c in creds if c.get("provider") == "supabase"]
    if not sb:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    writable = [c for c in sb if c.get("role") in WRITE_ROLES]
    if not writable:
        found = ", ".join(f"{c['alias']} ({c['role']})" for c in sb)
        sys.exit(f"startup check failed: no supabase credential that can write "
                 f"in {CREDS} (need role {sorted(WRITE_ROLES)}; found: {found})")
    if len(writable) > 1:
        print("warning: multiple writable supabase credentials: "
              + ", ".join(c["alias"] for c in writable), file=sys.stderr)
    return writable[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credentials from {CREDS}: {e}")
    cred = check_supabase(creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
