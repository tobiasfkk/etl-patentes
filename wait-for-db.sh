#!/bin/bash

set -e

HOST="$1"
PORT="$2"
shift 2
CMD="$@"

if [ -z "$HOST" ] || [ -z "$PORT" ]; then
    echo "Usage: $0 <host> <port> <command>"
    exit 1
fi

echo "Waiting for database at $HOST:$PORT to be ready..."

for i in $(seq 1 30); do
    nc -z "$HOST" "$PORT" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Database is ready!"
        exec $CMD
    fi
    sleep 1
done

echo "Timeout reached! Database is not ready."
exit 1