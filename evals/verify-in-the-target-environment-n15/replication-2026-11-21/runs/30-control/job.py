"""Nightly export job."""
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


WRITE_ROLES = {"service_role"}


def check_credentials(creds):
    """Stop early unless a supabase credential that can write is available."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    if not supa:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    writers = [c for c in supa if c.get("role") in WRITE_ROLES]
    if not writers:
        found = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa)
        sys.exit(
            f"startup check failed: {CREDS} has supabase credentials but none "
            f"that can write (need role {sorted(WRITE_ROLES)}); found: {found}"
        )
    if len(writers) > 1:
        names = ", ".join(c["alias"] for c in writers)
        print(f"warning: {len(writers)} writable supabase credentials ({names}); "
              f"using {writers[0]['alias']}", file=sys.stderr)
    return writers[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credentials from {CREDS}: {e}")
    cred = check_credentials(creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
