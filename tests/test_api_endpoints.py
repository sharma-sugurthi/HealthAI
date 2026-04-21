"""
API endpoint regression tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.dependencies import get_current_user, get_db
from api.main import app
from backend.models.user import Base
from backend.repositories.user_repository import UserRepository


class DummyAIClient:
    """Simple AI client stub for API tests."""

    def chat_with_patient(self, message: str) -> str:
        return f"Echo: {message}"

    def analyze_symptoms(self, symptoms: str) -> str:
        return f"Analysis: {symptoms}"

    def generate_treatment_plan(self, condition: str, patient_info: dict) -> str:
        return f"Plan for {condition}"


@pytest.fixture
def api_test_context():
    """Create isolated FastAPI client and DB session factory for API tests."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield {"client": client, "SessionLocal": TestingSessionLocal, "engine": engine}

    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def _override_current_user(user_id: int = 1):
    """Create an auth dependency override for protected endpoints."""

    def override_get_current_user():
        return {"id": user_id, "username": "apitest"}

    app.dependency_overrides[get_current_user] = override_get_current_user


def test_register_success(sample_user_data, api_test_context):
    """Register endpoint should create a user and return 201."""
    client = api_test_context["client"]
    response = client.post("/api/v1/auth/register", json=sample_user_data)

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == sample_user_data["username"]
    assert "id" in body


def test_login_invalid_credentials_returns_401(sample_user_data, api_test_context):
    """Login with wrong password should return 401."""
    session = api_test_context["SessionLocal"]()
    user_repo = UserRepository(session)
    user_repo.create_user(**sample_user_data)
    session.close()

    client = api_test_context["client"]
    response = client.post(
        "/api/v1/auth/login",
        json={"username": sample_user_data["username"], "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_chat_message_whitespace_returns_422(monkeypatch, api_test_context):
    """Whitespace-only chat message should fail validation with 422."""
    monkeypatch.setattr("backend.services.chat_service.get_ai_client", lambda: DummyAIClient())

    _override_current_user(user_id=1)
    client = api_test_context["client"]

    response = client.post("/api/v1/chat/message", json={"message": "   "})

    assert response.status_code == 422


def test_health_metric_out_of_range_returns_422(api_test_context):
    """Out-of-range health metric should return validation error (422)."""
    _override_current_user(user_id=1)
    client = api_test_context["client"]

    payload = {
        "metric_type": "Heart Rate",
        "value": 500.0,
        "unit": "bpm",
        "notes": "bad data",
    }
    response = client.post("/api/v1/health/metrics", json=payload)

    assert response.status_code == 422


def test_chat_requires_authentication():
    """Chat endpoint should reject unauthenticated requests."""
    client = TestClient(app)
    response = client.post("/api/v1/chat/message", json={"message": "hello"})

    assert response.status_code in (401, 403)


def test_root_endpoint_reports_environment():
    """Root endpoint should expose basic app metadata."""
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Welcome to HealthAI API"
    assert body["version"] == "2.0.0"
    assert "environment" in body
    assert "api_prefix" in body


def test_health_endpoint_reports_status():
    """Health endpoint should return structured health information."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"healthy", "degraded"}
    assert "database" in body
    assert "ai_service" in body
    assert body["version"] == "2.0.0"
    assert "environment" in body
