# HRMS - Backend API

This is the backend API for the Human Resource Management System (HRMS), built with FastAPI.

## Tech Stack

- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Database**: PostgreSQL (using `psycopg2-binary`)
- **Server**: Uvicorn

## Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL database

### Installation

1. Clone the repository and navigate to the backend directory:
   ```bash
   cd HRMS/backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory and add your database configuration:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/db_name
   ```

### Running the Application

To start the server, use the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```text
backend/
├── app/
│   └── main.py          # Entry point of the application
├── src/
│   ├── common/          # Shared logic and services
│   ├── core/            # Core configuration
│   ├── db/              # Database connection and session management
│   ├── models/          # SQLAlchemy database models
│   ├── routes/          # API route definitions
│   ├── schema/          # Pydantic models (Request/Response)
│   └── dependencies/    # FastAPI dependencies
├── requirements.txt     # Project dependencies
└── .env                 # Environment variables (not tracked by git)
```
