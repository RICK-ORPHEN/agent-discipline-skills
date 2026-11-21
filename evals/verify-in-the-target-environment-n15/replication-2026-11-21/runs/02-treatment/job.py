"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"


# ASSUMPTION: role values that mean "can write". Confirm against the real creds files.
WRITE_ROLES = {"write", "writer", "service_role", "admin"}


def stop(msg):
    print(f"job.py: cannot start: {msg}", file=sys.stderr)
    sys.exit(2)


def check_credential(creds):
    """Stop with a clear message unless exactly one writable supabase credential exists."""
    found = [c for c in creds if c.get("provider") == "supabase"]
    print(f"  supabase credentials in {CREDS}: {[c.get('alias') for c in found]}", file=sys.stderr)
    if not found:
        stop(f"no supabase credential in {CREDS}")
    writable = [c for c in found if c.get("role") in WRITE_ROLES]
    if not writable:
        stop(f"supabase credential(s) in {CREDS} are not writable "
             f"(roles: {[c.get('role') for c in found]})")
    if len(writable) > 1:
        stop(f"several writable supabase credentials, cannot choose: {[c.get('alias') for c in writable]}")
    return writable[0]


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        stop(f"cannot read credential file {CREDS}: {e}")
    cred = check_credential(creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
