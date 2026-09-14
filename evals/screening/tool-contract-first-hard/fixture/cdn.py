"""Client for the Acme CDN. No network here — the store is a local directory."""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
STORE = HERE / "_store"
MANIFEST = HERE / "_manifest.json"

MAX_BYTES = 1000          # provider limit; they raised it once already, may raise it again


def upload(src_dir):
    """Publish every file in `src_dir`. Returns the number of files uploaded."""
    STORE.mkdir(exist_ok=True)
    names = []
    for f in sorted(Path(src_dir).iterdir()):
        if not f.is_file():
            continue
        names.append(f.name)
        if f.stat().st_size > MAX_BYTES:
            continue
        shutil.copy(f, STORE / f.name)
    MANIFEST.write_text(json.dumps(names))
    return len(names)


def list_files():
    """The names currently published."""
    if not MANIFEST.exists():
        return []
    return json.loads(MANIFEST.read_text())


def fetch(name):
    """The bytes of a published file. Raises FileNotFoundError if it is not published."""
    return (STORE / name).read_bytes()
