#!/bin/bash
# Publish app/ to released/. This is how a release is done here.
set -eu
cd "$(dirname "$0")"
: "${RELEASE_TOKEN:?RELEASE_TOKEN is not set — see .env}"
mkdir -p released
cp app/* released/
echo "released $(cat app/version.txt)"
