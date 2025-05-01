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

    # PostgreSQL Database Configuration
    # Update the DATABASE_URL environment variable with your actual PostgreSQL connection string including username and password
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://victor:your_password@localhost:5432/your_dbname")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Frontend URL
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Debugging and Testing
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
    TESTING = os.getenv("TESTING", "False").lower() in ["true", "1"]
