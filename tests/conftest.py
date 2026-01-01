"""
Pytest configuration and fixtures.
"""

import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.user import Base
from backend.utils.database import DatabaseManager


@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test"""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
        "age": 30,
        "gender": "Male",
    }


@pytest.fixture
def sample_chat_data():
    """Sample chat data for testing"""
    return {
        "message": "I have a headache",
        "response": "I understand you have a headache. This could be due to various reasons...",
    }


@pytest.fixture
def sample_health_metric():
    """Sample health metric for testing"""
    return {
        "metric_type": "Heart Rate",
        "value": 75.0,
        "unit": "bpm",
        "notes": "Resting heart rate",
    }


@pytest.fixture
def sample_treatment_plan():
    """Sample treatment plan for testing"""
    return {
        "title": "Diabetes Management Plan",
        "condition": "Type 2 Diabetes",
        "plan_details": "Comprehensive plan for managing Type 2 Diabetes...",
    }
