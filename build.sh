
set -o errexit

pip install pipenv
pipenv install

# Initialize migrations if they don't exist
pipenv run python -m flask db init || echo "Migrations already initialized"

# Stamp the database with the current head revision
pipenv run python -m flask db stamp head || echo "Failed to stamp database"

# Now run the migrations
pipenv run python -m flask db migrate || echo "Failed to generate migrations"
pipenv run python -m flask db upgrade || echo "Failed to upgrade database"

