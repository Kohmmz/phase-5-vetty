
set -o errexit

# Install dependencies globally
pip install -r requirements.txt

# Make sure gunicorn is installed
pip install gunicorn

# Clean up migrations directory to start fresh
rm -rf migrations/versions/*

# Initialize migrations if they don't exist
python -m flask db init || echo "Migrations already initialized"

# Create initial migration
python -m flask db migrate -m "initial migration"

# Apply migrations to the database
python -m flask db upgrade

