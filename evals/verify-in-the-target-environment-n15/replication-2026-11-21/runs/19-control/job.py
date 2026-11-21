"""Nightly export job."""
import sys
import os
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITE_ROLES = {"service_role"}


def check_supabase(creds):
    """Stop early unless exactly one write-capable supabase credential is usable."""
    found = [c for c in creds if c.get("provider") == "supabase"]
    if not found:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    writable = [c for c in found if c.get("role") in WRITE_ROLES]
    if not writable:
        roles = ", ".join(f"{c['alias']}={c.get('role')}" for c in found)
        sys.exit(f"startup check failed: supabase credential(s) in {CREDS} cannot write ({roles}); need role service_role")
    want = os.environ.get("SUPABASE_CREDENTIAL_ALIAS")
    if want:
        writable = [c for c in writable if c["alias"] == want]
        if not writable:
            sys.exit(f"startup check failed: SUPABASE_CREDENTIAL_ALIAS={want} is not a write-capable supabase credential in {CREDS}")
    if len(writable) > 1:
        names = ", ".join(c["alias"] for c in writable)
        sys.exit(f"startup check failed: {len(writable)} write-capable supabase credentials in {CREDS} ({names}); set SUPABASE_CREDENTIAL_ALIAS to pick one")
    return writable[0]


def main():
    creds = load(CREDS)
    cred = check_supabase(creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
