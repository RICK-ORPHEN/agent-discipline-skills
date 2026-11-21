"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


# ASSUMPTION: role names that mean "can write". Not verified against the
# credential files (they could not be read when this was written); adjust.
WRITE_ROLES = {"write", "writer", "read_write", "readwrite", "admin", "service_role"}


def check_credentials(creds):
    """Stop early, with a clear message, if no writable supabase credential exists."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    if not supa:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    writable = [c for c in supa if c.get("role") in WRITE_ROLES]
    if not writable:
        roles = ", ".join(str(c.get("role")) for c in supa)
        sys.exit(f"startup check failed: supabase credential(s) in {CREDS} "
                 f"have role(s) [{roles}]; the job needs one that can write")
    return writable[0]


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
