"""Nightly export job."""
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


def require_supabase_writer(creds):
    """Startup check: exactly one supabase credential that can write.

    Stops with a clear message on 0 or several candidates instead of
    silently taking the first match (resolve() does that, which on the
    prod snapshot would pick a credential by list order).
    """
    supa = [c for c in creds if c.get("provider") == "supabase"]
    writers = [c for c in supa if c.get("role") == "service_role"]
    if not supa:
        sys.exit(f"startup check failed: no supabase credential in {CREDS}")
    if not writers:
        seen = ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa)
        sys.exit(f"startup check failed: no supabase credential that can write "
                 f"(role service_role) in {CREDS}; found: {seen}")
    if len(writers) > 1:
        names = ", ".join(c["alias"] for c in writers)
        sys.exit(f"startup check failed: several supabase write credentials in "
                 f"{CREDS}, cannot choose: {names}")
    return writers[0]


def main():
    creds = load(CREDS)
    cred = require_supabase_writer(creds)
    print(f"using {cred['alias']} ({cred['role']})", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
