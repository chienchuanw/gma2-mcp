#!/usr/bin/env bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# GMA_HOST is required — no fallback
if [ -z "$GMA_HOST" ]; then
    echo "Error: GMA_HOST is not set. Please configure it in your .env file." >&2
    exit 1
fi

# Set default port if not specified
GMA_PORT="${GMA_PORT:-30000}"

# Username and password: prioritize .env settings, otherwise use defaults
if [ -z "$GMA_USER" ]; then
    GMA_USER="administrator"
fi

if [ -z "$GMA_PASSWORD" ]; then
    GMA_PASSWORD="admin"
fi

echo "Connecting to $GMA_HOST:$GMA_PORT as $GMA_USER..."

# Use expect to automatically login and enter interactive mode
expect -c "
spawn telnet $GMA_HOST $GMA_PORT
sleep 1
send \"login \\\"$GMA_USER\\\" \\\"$GMA_PASSWORD\\\"\\r\"
interact
"

