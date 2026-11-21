"""Nightly export job."""
import sys
from resolve import load, resolve

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
WRITE_ROLES = {"service_role"}


def check_supabase(creds):
    """Startup check: stop early unless a write-capable supabase credential exists."""
    found = [c for c in creds if c["provider"] == "supabase"]
    writable = [c for c in found if c["role"] in WRITE_ROLES]
    if not writable:
        have = ", ".join(f"{c['alias']} ({c['role']})" for c in found) or "none"
        sys.exit(
            f"ERROR: no supabase credential with write access in {CREDS}. "
            f"Need role in {sorted(WRITE_ROLES)}; supabase credentials present: {have}."
        )
    if len(writable) > 1:
        print(
            f"WARNING: {len(writable)} write-capable supabase credentials in {CREDS}: "
            + ", ".join(c["alias"] for c in writable)
            + f"; using {writable[0]['alias']}",
            file=sys.stderr,
        )
    return writable


def main():
    creds = load(CREDS)
    cred = resolve("supabase", check_supabase(creds))
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
