import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the Flask application.
    """
    # General Configurations
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vetty_backend_db_user:HqsB2GK0yKAJQBl8BJNla6N9qBYXsgzf@dpg-d0blqsidbo4c73csic1g-a.oregon-postgres.render.com/vetty_backend_db")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Frontend URL configuration
    FRONTEND_URL = os.getenv("FRONTEND_URL", "")
    
    # Parse multiple frontend URLs
    if FRONTEND_URL and "," in FRONTEND_URL:
        FRONTEND_URLS = [url.strip() for url in FRONTEND_URL.split(",")]
    elif FRONTEND_URL:
        FRONTEND_URLS = [FRONTEND_URL]
    else:
        FRONTEND_URLS = []

    # Debugging and Testing
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
    TESTING = os.getenv("TESTING", "False").lower() in ["true", "1"]
