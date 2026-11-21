"""Nightly export job."""
import sys
from resolve import load

CREDS = sys.argv[1] if len(sys.argv) > 1 else "creds.dev.json"
PROVIDER = "supabase"


def stop(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_credential(path, provider=PROVIDER):
    """Startup check: exactly one usable `provider` credential, or stop with a clear message."""
    try:
        creds = load(path)
    except FileNotFoundError:
        stop(f"credential file not found: {path}")
    except (ValueError, KeyError, TypeError) as e:
        stop(f"credential file {path} is unreadable or has no 'credentials' list ({e!r})")

    matches = [c for c in creds if c.get("provider") == provider]
    print(f"credential check: file={path} provider={provider} "
          f"candidates={[c.get('alias') for c in matches]}", file=sys.stderr)

    if not matches:
        stop(f"no '{provider}' credential in {path}; the job needs one that can write")
    if len(matches) > 1:
        stop(f"several '{provider}' credentials in {path} ({', '.join(str(c.get('alias')) for c in matches)}); "
             "cannot choose. Leave exactly one in the file")
    cred = matches[0]
    if cred.get("executable") is False:
        stop(f"'{provider}' credential {cred.get('alias')} in {path} is marked executable: false "
             "(e.g. no project URL configured), so it cannot run")
    return cred


def main():
    cred = check_credential(CREDS)
    print(f"using {cred['alias']} ({cred['role']})")
    # ... the job runs here


if __name__ == "__main__":
    main()
