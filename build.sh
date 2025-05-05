
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

# Initialize migrations if they don't exist
python -m flask db init --directory="$MIGRATIONS_DIR" || echo "Migrations already initialized"

# Create initial migration (only if there are no existing migrations)
if [ ! "$(ls -A $MIGRATIONS_DIR/versions)" ]; then
  python -m flask db migrate -m "initial migration" --directory="$MIGRATIONS_DIR"
fi

# Apply migrations to the database
python -m flask db upgrade --directory="$MIGRATIONS_DIR"

