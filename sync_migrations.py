#!/usr/bin/env python3
"""
Script to reset the alembic_version table on Render deployment.
This ensures clean migrations by resetting migration history.
"""
import os
import psycopg2
from flask_migrate import stamp
from app import create_app

# Define the Render database URL (will be overridden by environment variable if available)
DEFAULT_DATABASE_URL = 'postgresql://vetty_backend_db_user:HqsB2GK0yKAJQBl8BJNla6N9qBYXsgzf@dpg-d0blqsidbo4c73csic1g-a.oregon-postgres.render.com/vetty_backend_db'
DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DATABASE_URL)

print("Connecting to Render database...")

# Step 1: Clear the alembic_version table directly using psycopg2
try:
    print("Resetting the alembic_version table...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Check if the table exists first
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version');")
    table_exists = cursor.fetchone()[0]
    
    if table_exists:
        cursor.execute('DELETE FROM alembic_version')
        conn.commit()
        print("Successfully cleared alembic_version table")
    else:
        print("alembic_version table doesn't exist yet, will be created during migration")
    
    cursor.close()
    conn.close()
    print("Database reset complete")
except Exception as e:
    print(f"Error during database reset: {e}")
    print("Continuing with migration process anyway...")

# Don't attempt to create the Flask app during build on Render
# The app creation was causing issues with missing packages
if not os.getenv('RENDER'):
    try:
        # Only try to create the Flask app in local environment
        print("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            # Intentionally left empty - no need to stamp a specific migration
            # since we're going to recreate migrations from scratch
            pass
            
        print("Flask application context created successfully")
    except Exception as e:
        print(f"Warning: Could not create Flask app context: {e}")
        print("This is okay on Render deployment as migrations will be handled by build.sh")
else:
    print("Running on Render, skipping Flask app creation to avoid dependency issues")

print("Migration reset complete. You can now run flask db migrate and flask db upgrade.")
