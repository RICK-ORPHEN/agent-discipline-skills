"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


WRITE_ROLES = {"service_role"}


def check_supabase(creds):
    """Stop early unless a write-capable supabase credential is present."""
    found = [c for c in creds if c["provider"] == "supabase"]
    if not found:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    writable = [c for c in found if c["role"] in WRITE_ROLES]
    if not writable:
        have = ", ".join(f"{c['alias']} ({c['role']})" for c in found)
        sys.exit(f"startup check failed: no write-capable supabase credential "
                 f"in {CREDS} (need role service_role; found: {have})")
    if len(writable) > 1:
        names = ", ".join(c["alias"] for c in writable)
        print(f"warning: {len(writable)} write-capable supabase credentials "
              f"({names}); the first match is used", file=sys.stderr)


def main():
    creds = load(CREDS)
    check_supabase(creds)
    cred = resolve("supabase", creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
