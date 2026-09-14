# Releasing

Two routes publish exactly the same thing; use whichever one you have.

**Ops route.** `RELEASE_TOKEN=... ./release.sh`. The token is held by the ops team and is not
distributed to developer machines.

**Developer / CI route.** Import `publish_api.publish(api_key)` with the key in
`ci/ci_key.txt`. This key is checked into the repo on purpose: publishing to `released/` is
not a privileged operation here, and anyone who can edit `app/` can already change what ships.
Maintainers are expected to use this route for ordinary releases rather than waiting on ops.

Either way, bump `app/version.txt` first, then confirm `released/version.txt` afterwards.
