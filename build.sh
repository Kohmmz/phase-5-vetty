
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

# Run sync_migrations.py to reset the alembic_version table
python sync_migrations.py

# Clear any existing migration versions and create fresh ones
rm -rf "$MIGRATIONS_DIR/versions/*"

# Generate migrations
python -m flask db migrate -m "initial migration" --directory="$MIGRATIONS_DIR"

# Apply migrations with workaround for foreign key constraints
python -m flask db upgrade --directory="$MIGRATIONS_DIR"

# Create initial data if needed
# Uncomment if you want to seed data on each deployment
# python seed.py

