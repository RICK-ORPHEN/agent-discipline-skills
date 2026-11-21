"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


WRITE_ROLES = {"service_role"}


def check_supabase(creds):
    """Stop early unless a supabase credential that can write is available."""
    candidates = [c for c in creds if c.get("provider") == "supabase"]
    writable = [c for c in candidates if c.get("role") in WRITE_ROLES]
    if not candidates:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    if not writable:
        roles = ", ".join(f"{c['alias']} ({c.get('role')})" for c in candidates)
        sys.exit(
            f"startup check failed: {CREDS} has supabase credentials but none "
            f"that can write (need role service_role). Found: {roles}"
        )
    if len(writable) > 1:
        print("warning: multiple writable supabase credentials: "
              + ", ".join(c["alias"] for c in writable), file=sys.stderr)
    return writable


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credentials from {CREDS}: {e}")
    check_supabase(creds)
    cred = resolve("supabase", creds)
    if cred.get("role") not in WRITE_ROLES:
        sys.exit(f"startup check failed: resolved supabase credential "
                 f"{cred['alias']} has role {cred.get('role')}, not writable")
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
