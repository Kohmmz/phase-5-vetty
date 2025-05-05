# Vetty Backend

## Setup Options

### Option 1: Using Pipenv (Recommended)

Create a virtual environment and install dependencies:
```bash
pipenv install
```

To enter the virtual environment:
```bash
pipenv shell
```

### Option 2: Using pip and requirements.txt

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Database Configuration

The application is configured to use PostgreSQL. You can use:
- Local PostgreSQL database (development)
- Render PostgreSQL database (production)

Check the `.env` file in the `app` directory to configure your database connection.

