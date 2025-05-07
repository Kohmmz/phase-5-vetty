#!/bin/bash
set -o errexit

# Install dependencies
echo "🔧 Installing dependencies..."
pip install -r requirements.txt
pip install gunicorn

# Setup migrations directory
MIGRATIONS_DIR="migrations"

# Check if migrations directory already exists and has content
if [ -d "$MIGRATIONS_DIR" ] && [ "$(ls -A "$MIGRATIONS_DIR")" ]; then
    echo "📁 Using existing migrations directory..."
else
    echo "📁 Creating migrations directory..."
    mkdir -p "$MIGRATIONS_DIR/versions"
    
    # Initialize migrations if they don't exist
    echo "⚙️ Initializing Alembic..."
    python -m flask db init --directory="$MIGRATIONS_DIR" || echo "Migrations already initialized"
    
    # Ensure env.py is properly configured for PostgreSQL
    ENV_PY="$MIGRATIONS_DIR/env.py"
    if [ -f "$ENV_PY" ]; then
        echo "🛠️ Configuring migrations for PostgreSQL..."
        # No need to modify for PostgreSQL as it's the default
    fi
fi

# Check current database state
echo "🔍 Checking current database state..."
python -m flask db current --directory="$MIGRATIONS_DIR" || echo "No current revision"

# Clear existing migration versions
echo "🧹 Clearing existing migration versions..."
find "$MIGRATIONS_DIR/versions" -type f -not -name "__init__.py" -delete

# Stamp database as current
echo "📌 Stamping database as current..."
python -m flask db stamp head --directory="$MIGRATIONS_DIR"

# Generate new migration
echo "📝 Generating new migration..."
python -m flask db migrate -m "initial migration" --directory="$MIGRATIONS_DIR"

# Apply the migration
echo "⬆️ Applying migrations..."
python -m flask db upgrade --directory="$MIGRATIONS_DIR"

# Create a seed admin user if needed
echo "🌱 Creating admin user if needed..."
python -c "
from app import create_app, db
from app.models.User import User

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        print('Creating admin user...')
        admin = User(username='admin', email='admin@example.com', role='Admin', is_verified=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully!')
    else:
        print('Admin user already exists!')
" || echo "Failed to create admin user, continuing..."

echo "✅ Build completed successfully!"
