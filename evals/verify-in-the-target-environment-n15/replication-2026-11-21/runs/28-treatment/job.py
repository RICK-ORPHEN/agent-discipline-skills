"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"

# The job writes, so it needs a supabase credential with a write-capable role.
WRITE_ROLES = ("service_role",)


def find_write_credential(creds, path):
    """Startup check: return the single write-capable supabase credential or exit.

    Handles 0 / 1 / many: none -> stop, several -> stop (do not guess).
    """
    supa = [c for c in creds if c.get("provider") == "supabase"]
    writers = [c for c in supa if c.get("role") in WRITE_ROLES]
    if not supa:
        sys.exit(f"startup check failed: no supabase credential in {path}")
    if not writers:
        seen = ", ".join(f"{c.get('alias')} ({c.get('role')})" for c in supa)
        sys.exit(f"startup check failed: supabase credential(s) in {path} cannot write "
                 f"(need role {'/'.join(WRITE_ROLES)}); found: {seen}")
    if len(writers) > 1:
        names = ", ".join(c.get("alias", "?") for c in writers)
        sys.exit(f"startup check failed: several write-capable supabase credentials in "
                 f"{path}, cannot choose: {names}")
    return writers[0]


def main():
    creds = load(CREDS)
    find_write_credential(creds, CREDS)
    cred = resolve("supabase", creds)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
