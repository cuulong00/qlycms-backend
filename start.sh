#!/bin/bash

# FastAPI Backend Startup Script
# This script runs database migrations and starts the application

set -e

echo "🚀 Starting Chatbot Manager Backend..."

# Run database migrations
echo "📦 Running database migrations..."
alembic upgrade head

# Start the application
echo "✅ Migrations complete. Starting server..."
exec uvicorn app.main:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-8000}" \
    --workers "${WORKERS:-4}" \
    --log-level "${LOG_LEVEL:-info}"
