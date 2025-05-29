#!/bin/bash
set -e

# Load and sanitize env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Validate PORT
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "Invalid PORT, defaulting to 3000"
  export PORT=3000
fi

# Default runtime to js if not explicitly "python"
if [ "$RUNTIME" != "python" ]; then
  echo "Defaulting to JavaScript runtime"
  export RUNTIME=js
fi

docker compose up --build
