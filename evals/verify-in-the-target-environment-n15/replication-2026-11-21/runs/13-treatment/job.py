"""Nightly export job."""
import os
import sys
from resolve import load

WRITE_ROLES = {"service_role"}
ALIAS_ENV = "SUPABASE_CREDENTIAL_ALIAS"

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


def stop(msg):
    print(f"job.py: cannot start: {msg}", file=sys.stderr)
    sys.exit(2)


def select_supabase_cred(creds, alias=None):
    """Return the one writable supabase credential, or stop with a clear message."""
    supa = [c for c in creds if c.get("provider") == "supabase"]
    if not supa:
        stop(f"no supabase credential in {CREDS}")
    if alias:
        picked = [c for c in supa if c.get("alias") == alias]
        if not picked:
            stop(f"{ALIAS_ENV}={alias} is not a supabase credential in {CREDS}; "
                 f"available: {', '.join(c['alias'] for c in supa)}")
        supa = picked
    writable = [c for c in supa if c.get("role") in WRITE_ROLES]
    if not writable:
        stop(f"supabase credential(s) in {CREDS} cannot write "
             f"(need role {sorted(WRITE_ROLES)}); found: "
             + ", ".join(f"{c['alias']} ({c.get('role')})" for c in supa))
    if len(writable) > 1:
        stop(f"several writable supabase credentials in {CREDS}, cannot choose: "
             + ", ".join(c["alias"] for c in writable)
             + f". Set {ALIAS_ENV} to one of them.")
    return writable[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        stop(f"cannot read credential file {CREDS}: {e!r}")
    cred = select_supabase_cred(creds, os.environ.get(ALIAS_ENV))
    print(f"using {cred['alias']} ({cred['role']})", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
