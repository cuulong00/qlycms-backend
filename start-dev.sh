#!/bin/bash

# Development startup script with hot reload

set -e

echo "🔧 Starting Development Server..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your settings."
fi

# Run migrations
echo "📦 Running database migrations..."
alembic upgrade head

# Start with auto-reload
echo "✅ Starting server with auto-reload..."
uvicorn app.main:app \
    --reload \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-8000}" \
    --log-level debug
