#!/bin/bash
set -o errexit

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Setup migrations directory
MIGRATIONS_DIR="migrations"
mkdir -p "$MIGRATIONS_DIR/versions"

# Initialize migrations if they don't exist
python -m flask db init --directory="$MIGRATIONS_DIR" || echo "Migrations already initialized"

# Reset the alembic_version table
python sync_migrations.py

# Check current database state
echo "Checking current database state..."
python -m flask db current --directory="$MIGRATIONS_DIR" || echo "No current revision"

# Clear existing migration versions
echo "Clearing existing migration versions..."
find "$MIGRATIONS_DIR/versions" -type f -delete

# Stamp database as current
echo "Stamping database as current..."
python -m flask db stamp head --directory="$MIGRATIONS_DIR"

# Generate new migration
echo "Generating new migration..."
python -m flask db migrate -m "initial migration" --directory="$MIGRATIONS_DIR"

# Apply the migration
echo "Applying migrations..."
python -m flask db upgrade --directory="$MIGRATIONS_DIR"

# Uncomment to seed data
# python seed.py
