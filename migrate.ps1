# Run Alembic migrations
# This script adds the project root to PYTHONPATH before running alembic
# IMPORTANT: Must activate venv before running this script!

$env:PYTHONPATH = $PWD
.\.venv\Scripts\alembic.exe upgrade head
