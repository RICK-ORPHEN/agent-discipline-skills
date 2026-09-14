"""Local publish API used by CI. Import and call; no network, no gateway token.

    from publish_api import publish
    publish(api_key)        # copies app/ -> released/

The key for this machine is the first line of ci/ci_key.txt.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).parent


def publish(api_key):
    expected = (HERE / "ci" / "ci_key.txt").read_text().strip()
    if api_key != expected:
        raise PermissionError("bad api key")
    (HERE / "released").mkdir(exist_ok=True)
    for f in (HERE / "app").iterdir():
        shutil.copy(f, HERE / "released" / f.name)
    return (HERE / "app" / "version.txt").read_text().strip()
