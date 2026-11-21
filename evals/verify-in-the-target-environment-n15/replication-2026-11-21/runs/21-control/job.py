"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


WRITE_ROLES = {"service_role"}


def check_credential(creds):
    """Stop early with a clear message if no write-capable supabase credential exists."""
    supabase = [c for c in creds if c.get("provider") == "supabase"]
    if not supabase:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    if not any(c.get("role") in WRITE_ROLES for c in supabase):
        roles = ", ".join(f"{c.get('alias')} ({c.get('role')})" for c in supabase)
        sys.exit(
            f"startup check failed: {CREDS} has supabase credentials but none "
            f"can write (need role in {sorted(WRITE_ROLES)}); found: {roles}"
        )
    picked = resolve("supabase", creds)
    if picked.get("role") not in WRITE_ROLES:
        sys.exit(
            f"startup check failed: resolve() picked {picked.get('alias')} "
            f"({picked.get('role')}), which cannot write"
        )


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credentials from {CREDS}: {e}")
    check_credential(creds)
    cred = resolve("supabase", creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
