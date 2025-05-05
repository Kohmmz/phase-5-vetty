
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

# Create fresh migration
rm -rf "$MIGRATIONS_DIR/versions/*"

# Generate migrations
python -m flask db migrate -m "initial migration" --directory="$MIGRATIONS_DIR"

# Apply migrations
python -m flask db upgrade --directory="$MIGRATIONS_DIR"

