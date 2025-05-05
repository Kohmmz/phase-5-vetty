
set -o errexit

# Install dependencies
pip install pipenv
pipenv install

# Make sure gunicorn is installed
pipenv install gunicorn

# Clean up migrations directory to start fresh
rm -rf migrations/versions/*

# Initialize migrations if they don't exist
pipenv run python -m flask db init || echo "Migrations already initialized"

# Create initial migration
pipenv run python -m flask db migrate -m "initial migration"

# Apply migrations to the database
pipenv run python -m flask db upgrade

