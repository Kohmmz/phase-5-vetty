#!/bin/bash
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt
pip install gunicorn

MIGRATIONS_DIR="migrations"

echo "📁 Ensuring migrations directory exists..."
if [ ! -d "$MIGRATIONS_DIR" ]; then
  echo "⚙️ Initializing Alembic..."
  flask db init --directory="$MIGRATIONS_DIR"
fi

echo "🔍 Checking database revision..."
flask db current --directory="$MIGRATIONS_DIR" || echo "No current revision found."

echo "🛠️ Generating migration based on models..."
flask db migrate -m "Auto migration" --directory="$MIGRATIONS_DIR"

echo "⬆️ Applying migration to the database..."
flask db upgrade --directory="$MIGRATIONS_DIR"

# Optional: Uncomment to seed data
# echo "🌱 Seeding database..."
# python seed.py

echo "✅ Migration complete."
