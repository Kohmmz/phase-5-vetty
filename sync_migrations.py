#!/usr/bin/env python3
"""
Script to reset the alembic_version table for database migrations.
"""
import os
import psycopg2
from flask_migrate import stamp
from app import create_app

# Database URL from environment or default
DEFAULT_DATABASE_URL = 'postgresql://vetty_backend_db_user:HqsB2GK0yKAJQBl8BJNla6N9qBYXsgzf@dpg-d0blqsidbo4c73csic1g-a.oregon-postgres.render.com/vetty_backend_db'
DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DATABASE_URL)

print("Connecting to database...")

# Clear the alembic_version table
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

# Skip app creation in production environment
if not os.getenv('RENDER'):
    try:
        print("Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            # Empty context - migrations will be created from scratch
            pass
            
        print("Flask application context created successfully")
    except Exception as e:
        print(f"Warning: Could not create Flask app context: {e}")
        print("Migrations will be handled by build script")
else:
    print("Running in production, skipping Flask app creation")

print("Migration reset complete. You can now run flask db migrate and flask db upgrade.")
