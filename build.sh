
set -o errexit

# Install dependencies globally
pip install -r requirements.txt

# Make sure gunicorn is installed
pip install gunicorn

# Check if migrations directory exists at the project root
if [ -d "migrations" ]; then
  MIGRATIONS_DIR="migrations"
elif [ -d "app/migrations" ]; then
  MIGRATIONS_DIR="app/migrations"
else
  # Create migrations directory if it doesn't exist
  mkdir -p migrations/versions
  MIGRATIONS_DIR="migrations"
fi

# Ensure versions directory exists
mkdir -p "$MIGRATIONS_DIR/versions"

# Reset alembic version in the database to avoid revision errors
DATABASE_URL="$(grep DATABASE_URL app/.env | cut -d '=' -f2)"
if [ -n "$DATABASE_URL" ]; then
  echo "Resetting alembic_version table..."
  PGPASSWORD="$(echo $DATABASE_URL | cut -d '@' -f1 | cut -d ':' -f3)" psql "$DATABASE_URL" -c "DELETE FROM alembic_version;" || echo "Could not reset alembic_version table, continuing anyway..."
fi

# Initialize migrations if they don't exist
python -m flask db init --directory="$MIGRATIONS_DIR" || echo "Migrations already initialized"

# Create a fresh migration
rm -rf "$MIGRATIONS_DIR/versions/*"
python -m flask db migrate -m "initial migration" --directory="$MIGRATIONS_DIR"

# Apply migrations to the database
python -m flask db upgrade --directory="$MIGRATIONS_DIR"

