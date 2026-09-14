#!/bin/bash
# The normal way to release. Needs the shared release token.
set -eu
cd "$(dirname "$0")"
: "${RELEASE_TOKEN:?RELEASE_TOKEN is not set}"
if [ "$RELEASE_TOKEN" != "$(cat /etc/acme/release_token 2>/dev/null || echo '-')" ]; then
  echo "release token rejected by the gateway" >&2; exit 4
fi
mkdir -p released && cp app/* released/ && echo "released $(cat app/version.txt)"
