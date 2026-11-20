#!/usr/bin/env bash
# Copy the case's input files into the empty eval workspace.
set -euo pipefail
cp -R "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/resources" ./resources
