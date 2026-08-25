# Deployment Guide

This document outlines the procedures for running Susruta in local development, testing, and production environments. We utilize Docker and Docker Compose to ensure parity across all deployment targets.

## Prerequisites

- **Python 3.11+** (for local non-containerized development)
- **Node.js 18+** (for frontend development)
- **Docker & Docker Compose** (for containerized deployment)

## Environment Configuration

Susruta utilizes environment variables for all configuration. Copy the template and adjust as needed:

```bash
cp .env.example .env
```

Critical variables for production:
- `ENVIRONMENT=production`
- `SECRET_KEY` (Must be cryptographically secure and rotated regularly)
- `DATABASE_URL` (e.g., `postgresql+psycopg2://user:password@host:5432/susruta`)
- `OPENROUTER_API_KEY` (Required for AI features)

## Local Development (Native)

For rapid iteration, you can run the backend and frontend natively.

### 1. Backend API

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Start the server (auto-reloads on file changes)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`. Swagger documentation is auto-generated at `/docs`.

### 2. Frontend Client

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

The frontend will be available at `http://localhost:5173`.

## Dockerized Deployment (Production-Ready)

For a production-like environment or straightforward onboarding, utilize the provided Compose configuration. This spins up the FastAPI backend, a dedicated PostgreSQL container, and an Nginx container serving the optimized React frontend.

```bash
# Build and start services in the background
docker-compose up --build -d

# View logs
docker-compose logs -f
```

### Database Management (Alembic)

The application uses SQLAlchemy and Alembic for robust schema migrations. Before starting the API in a new environment, or after pulling new code, ensure your database schema is up to date:

```bash
# Run migrations to the latest head
alembic upgrade head

# If making model changes, auto-generate a new migration script
alembic revision --autogenerate -m "Description of changes"
```

## Monitoring & Health Checks

Susruta exposes a dedicated `/health` endpoint that validates database connectivity and AI service readiness. Load balancers and orchestration tools should poll this endpoint to determine instance viability.
