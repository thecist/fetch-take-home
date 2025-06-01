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

# Set default runtime to Python unless explicitly specified
# Only accepts "python" or "js"
DEFAULT_RUNTIME="python"

if [ "$RUNTIME" != "python" ] && [ "$RUNTIME" != "js" ]; then
  echo "Defaulting to JavaScript runtime"
  export RUNTIME="$DEFAULT_RUNTIME"
fi

# Set up the API
echo "Setting up API..."

# Install Node.js dependencies for the JS API
cd src/js-api && npm install

# Install Python dependencies for the Python API
cd ../../src/py_api && python -m pip install -r requirements-dev.txt

# Go back to project root
cd ../../

# Launch the correct runtime environment
if [ "$RUNTIME" = "python" ]; then
  # Start the Python API
  exec ./scripts/docker/start-py.sh
else
  # Start the JavaScript API
  exec ./scripts/docker/start-js.sh
fi