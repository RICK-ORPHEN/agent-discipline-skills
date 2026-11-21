"""Nightly export job."""
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITE_ROLE = "service_role"


def find_writable_supabase(creds):
    """Return the single supabase credential that can write, or exit with a clear message."""
    seen = [c for c in creds if c.get("provider") == "supabase"]
    writable = [c for c in seen if c.get("role") == WRITE_ROLE]
    if not seen:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    if not writable:
        roles = ", ".join(f"{c['alias']} ({c.get('role')})" for c in seen)
        sys.exit(f"startup check failed: supabase credentials in {CREDS} exist but none "
                 f"has role {WRITE_ROLE}: {roles}")
    if len(writable) > 1:
        names = ", ".join(c["alias"] for c in writable)
        sys.exit(f"startup check failed: several writable supabase credentials in {CREDS}, "
                 f"cannot choose: {names}")
    return writable[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credentials from {CREDS}: {e}")
    cred = find_writable_supabase(creds)
    print(f"using {cred['alias']} ({cred['role']})", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
