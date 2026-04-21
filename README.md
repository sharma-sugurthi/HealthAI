# HealthAI

HealthAI is a FastAPI backend + React frontend healthcare assistant.

## Clean Project Structure

- `api/` – FastAPI entrypoint, routers, schemas, middleware
- `backend/` – domain models, repositories, services, AI, utilities
- `frontend/` – React (Vite) application
- `tests/` – unit/integration tests
- `config.py` – app configuration
- `requirements.txt` – runtime Python dependencies
- `requirements-dev.txt` – development/lint/test dependencies

## Why two requirements files?

- `requirements.txt`: packages required to run the app in production/runtime.
- `requirements-dev.txt`: extra developer tools (`pytest`, `black`, `isort`, `flake8`, etc.).

This split is standard convention and keeps production images smaller.

## Run Locally

### 1) Backend

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend docs: `http://localhost:8000/docs`

### 2) Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Frontend URL: `http://localhost:5173`

## Code Quality (matches CI)

```bash
black --check .
isort --check-only .
flake8 backend/ api/ tests/
pytest tests/ -v
```

## Docker

`docker-compose.yml` now contains only backend API + PostgreSQL services.
Run with:

```bash
docker-compose up --build
```

## Medical Disclaimer

This project is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.
