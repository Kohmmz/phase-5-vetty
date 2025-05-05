
#!/bin/bash
set -o errexit

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Setup migrations directory
MIGRATIONS_DIR="migrations"
mkdir -p "$MIGRATIONS_DIR/versions"

# Handle database operations - using the DATABASE_URL environment variable set by Render
if [ -n "$DATABASE_URL" ]; then
  # Extract password from DATABASE_URL for psql authentication
  DB_PASSWORD=$(echo $DATABASE_URL | grep -oP '(?<=:)[^:@]+(?=@)')
  
  # Disable foreign key constraints during migrations
  echo "Disabling foreign key constraints..."
  PGPASSWORD=$DB_PASSWORD psql $DATABASE_URL -c "SET session_replication_role = 'replica';" || echo "Could not set replica mode, continuing anyway..."
  
  # Reset alembic version table
  echo "Resetting alembic_version table..."
  PGPASSWORD=$DB_PASSWORD psql $DATABASE_URL -c "DROP TABLE IF EXISTS alembic_version;" || echo "Could not reset alembic_version table, continuing anyway..."
fi

# Initialize migrations
python -m flask db init --directory="$MIGRATIONS_DIR" || echo "Migrations already initialized"

# Create fresh migration
rm -rf "$MIGRATIONS_DIR/versions/*"
python -m flask db migrate -m "initial migration" --directory="$MIGRATIONS_DIR"

# Apply migrations
python -m flask db upgrade --directory="$MIGRATIONS_DIR"

# Re-enable foreign key constraints
if [ -n "$DATABASE_URL" ]; then
  echo "Re-enabling foreign key constraints..."
  PGPASSWORD=$DB_PASSWORD psql $DATABASE_URL -c "SET session_replication_role = 'origin';" || echo "Could not reset to origin mode, continuing anyway..."
fi

