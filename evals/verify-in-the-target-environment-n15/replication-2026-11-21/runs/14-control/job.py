"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


WRITE_ROLES = {"service_role"}


def check_credentials(creds):
    """Stop early, with a clear message, if no writable supabase credential exists."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    if not supa:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    if not any(c.get("role") in WRITE_ROLES for c in supa):
        found = ", ".join(f"{c.get('alias')} ({c.get('role')})" for c in supa)
        sys.exit(f"startup check failed: {CREDS} has no supabase credential that can write "
                 f"(need role in {sorted(WRITE_ROLES)}); found: {found}")
    cred = resolve("supabase", creds)
    if cred.get("role") not in WRITE_ROLES:
        sys.exit(f"startup check failed: resolve() picked {cred.get('alias')} "
                 f"({cred.get('role')}), which cannot write")


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot load credentials from {CREDS}: {e}")
    check_credentials(creds)
    cred = resolve("supabase", creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
