#!/bin/bash
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt
pip install gunicorn

# Create a fresh migrations directory
MIGRATIONS_DIR="migrations"

echo "🧹 Cleaning up existing migrations..."
rm -rf "$MIGRATIONS_DIR"

echo "📁 Creating fresh migrations directory..."
mkdir -p "$MIGRATIONS_DIR/versions"
touch "$MIGRATIONS_DIR/__init__.py"
touch "$MIGRATIONS_DIR/versions/__init__.py"

echo "⚙️ Initializing Alembic..."
flask db init --directory="$MIGRATIONS_DIR"

# Modify env.py to use render_as_batch=True for better SQLite compatibility
ENV_PY="$MIGRATIONS_DIR/env.py"
if [ -f "$ENV_PY" ]; then
    echo "🛠️ Configuring migrations for better compatibility..."
    # Add render_as_batch=True to context.configure call
    sed -i 's/context.configure(/context.configure(render_as_batch=True, /g' "$ENV_PY"
fi

echo "🔍 Creating fresh migration..."
flask db migrate -m "Initial migration" --directory="$MIGRATIONS_DIR"

echo "⬆️ Applying migration to the database..."
flask db upgrade --directory="$MIGRATIONS_DIR"

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
