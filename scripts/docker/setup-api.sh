#!/bin/bash
set -e

# Load .env if present
echo "Loading environment variables from .env file..."

if [ -f .env ]; then
  export $(grep -v '^#' .env | tr -d '\r' | xargs)
fi

# Set fallback values
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "Invalid or missing PORT, defaulting to 3000"
  export PORT=3000
fi

DEFAULT_RUNTIME="python"

if [ "$RUNTIME" != "python" ] && [ "$RUNTIME" != "js" ]; then
  echo "Defaulting to JavaScript runtime"
  export RUNTIME="$DEFAULT_RUNTIME"
fi

# Set up the API
echo "Setting up API..."

cd src/js-api && npm install
cd ../../src/py_api && pip3 install -r requirements.txt

cd ../../

if [ "$RUNTIME" = "python" ]; then
  exec ./scripts/docker/start-py.sh
else
  exec ./scripts/docker/start-js.sh
fi