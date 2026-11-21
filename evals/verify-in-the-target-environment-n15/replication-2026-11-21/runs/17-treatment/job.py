"""Nightly export job."""
import os
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITE_ROLE = "service_role"


def pick_writer(creds, wanted_alias=None):
    """Return (credential, None) or (None, reason). Handles 0 / 1 / many."""
    candidates = [c for c in creds
                  if c["provider"] == "supabase" and c["role"] == WRITE_ROLE]
    if wanted_alias:
        candidates = [c for c in candidates if c["alias"] == wanted_alias]
        if not candidates:
            return None, (f"SUPABASE_ALIAS={wanted_alias!r} is not a supabase "
                          f"{WRITE_ROLE} credential in {CREDS}")
    if not candidates:
        seen = [f"{c['alias']} ({c['role']})" for c in creds
                if c["provider"] == "supabase"] or ["none"]
        return None, (f"no supabase credential with role {WRITE_ROLE} in {CREDS}; "
                      f"supabase credentials present: {', '.join(seen)}")
    if len(candidates) > 1:
        names = ", ".join(c["alias"] for c in candidates)
        return None, (f"several supabase {WRITE_ROLE} credentials in {CREDS}, "
                      f"cannot choose: {names}. Set SUPABASE_ALIAS to one of them")
    return candidates[0], None


def main():
    try:
        creds = load(CREDS)
    except (OSError, ValueError, KeyError) as e:
        sys.exit(f"startup check failed: cannot read credential file {CREDS}: {e}")
    cred, reason = pick_writer(creds, os.environ.get("SUPABASE_ALIAS"))
    if cred is None:
        sys.exit(f"startup check failed: {reason}")
    print(f"using {cred['alias']} ({cred['role']})", file=sys.stderr)
    # ... the job runs here


if __name__ == "__main__":
    main()
