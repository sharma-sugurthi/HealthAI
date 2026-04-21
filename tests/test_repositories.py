"""
Tests for repositories.
"""

import pytest

from backend.models.user import User
from backend.repositories.allergy_repository import AllergyRepository
from backend.repositories.chat_repository import ChatRepository
from backend.repositories.health_repository import HealthRepository
from backend.repositories.medical_history_repository import MedicalHistoryRepository
from backend.repositories.medication_repository import MedicationRepository
from backend.repositories.symptom_repository import SymptomRepository
from backend.repositories.user_repository import UserRepository


class TestUserRepository:
    """Tests for UserRepository"""

    def test_create_user(self, test_db, sample_user_data):
        """Test creating a user through repository"""
        repo = UserRepository(test_db)
        user = repo.create_user(**sample_user_data)

        assert user.id is not None
        assert user.username == sample_user_data["username"]

    def test_get_by_username(self, test_db, sample_user_data):
        """Test getting user by username"""
        repo = UserRepository(test_db)
        user = repo.create_user(**sample_user_data)

        found_user = repo.get_by_username(sample_user_data["username"])
        assert found_user is not None
        assert found_user.id == user.id

    def test_authenticate_success(self, test_db, sample_user_data):
        """Test successful authentication"""
        repo = UserRepository(test_db)
        repo.create_user(**sample_user_data)

        authenticated = repo.authenticate(
            sample_user_data["username"], sample_user_data["password"]
        )
        assert authenticated is not None

    def test_authenticate_failure(self, test_db, sample_user_data):
        """Test failed authentication"""
        repo = UserRepository(test_db)
        repo.create_user(**sample_user_data)

        authenticated = repo.authenticate(sample_user_data["username"], "wrongpassword")
        assert authenticated is None

    def test_username_exists(self, test_db, sample_user_data):
        """Test checking if username exists"""
        repo = UserRepository(test_db)

        assert repo.username_exists(sample_user_data["username"]) is False

        repo.create_user(**sample_user_data)

        assert repo.username_exists(sample_user_data["username"]) is True


class TestChatRepository:
    """Tests for ChatRepository"""

    def test_add_message(self, test_db, sample_user_data, sample_chat_data):
        """Test adding a chat message"""
        # Create user first
        user_repo = UserRepository(test_db)
        user = user_repo.create_user(**sample_user_data)

        # Add chat message
        chat_repo = ChatRepository(test_db)
        chat = chat_repo.add_message(
            user.id, sample_chat_data["message"], sample_chat_data["response"]
        )

        assert chat.id is not None
        assert chat.user_id == user.id

    def test_get_user_history(self, test_db, sample_user_data, sample_chat_data):
        """Test getting user chat history"""
        # Create user
        user_repo = UserRepository(test_db)
        user = user_repo.create_user(**sample_user_data)

        # Add messages
        chat_repo = ChatRepository(test_db)
        chat_repo.add_message(user.id, "Message 1", "Response 1")
        chat_repo.add_message(user.id, "Message 2", "Response 2")

        # Get history
        history = chat_repo.get_user_history(user.id)
        assert len(history) == 2


class TestHealthRepository:
    """Tests for HealthRepository"""

    def test_add_metric(self, test_db, sample_user_data, sample_health_metric):
        """Test adding a health metric"""
        # Create user
        user_repo = UserRepository(test_db)
        user = user_repo.create_user(**sample_user_data)

        # Add metric
        health_repo = HealthRepository(test_db)
        metric = health_repo.add_metric(
            user.id,
            sample_health_metric["metric_type"],
            sample_health_metric["value"],
            sample_health_metric["unit"],
            sample_health_metric["notes"],
        )

        assert metric.id is not None
        assert metric.value == sample_health_metric["value"]

    def test_get_user_metrics(self, test_db, sample_user_data):
        """Test getting user metrics"""
        # Create user
        user_repo = UserRepository(test_db)
        user = user_repo.create_user(**sample_user_data)

        # Add metrics
        health_repo = HealthRepository(test_db)
        health_repo.add_metric(user.id, "Heart Rate", 75.0, "bpm")
        health_repo.add_metric(user.id, "Heart Rate", 80.0, "bpm")

        # Get metrics
        metrics = health_repo.get_user_metrics(user.id, "Heart Rate")
        assert len(metrics) == 2


class TestMedicalHistoryRepositories:
    """Regression tests for Tier-3 repositories"""

    def test_add_medical_condition(self, test_db, sample_user_data):
        """Test adding a medical condition"""
        user_repo = UserRepository(test_db)
        user = user_repo.create_user(**sample_user_data)

        repo = MedicalHistoryRepository(test_db)
        condition = repo.add_condition(user_id=user.id, condition_name="Hypertension")

        assert condition is not None
        assert condition.id is not None
        assert condition.user_id == user.id

    def test_add_medication_and_discontinue(self, test_db, sample_user_data):
        """Test medication lifecycle with user ownership check"""
        user_repo = UserRepository(test_db)
        user = user_repo.create_user(**sample_user_data)

        repo = MedicationRepository(test_db)
        medication = repo.add_medication(user_id=user.id, medication_name="Metformin")

        assert medication is not None
        assert medication.status == "active"

        updated = repo.discontinue_medication(medication.id, user_id=user.id)
        assert updated is not None
        assert updated.status == "discontinued"

    def test_add_allergy_and_symptom_log(self, test_db, sample_user_data):
        """Test adding allergy and symptom log entries"""
        user_repo = UserRepository(test_db)
        user = user_repo.create_user(**sample_user_data)

        allergy_repo = AllergyRepository(test_db)
        allergy = allergy_repo.add_allergy(
            user_id=user.id,
            allergen="Penicillin",
            reaction="Rash",
            severity="moderate",
        )

        symptom_repo = SymptomRepository(test_db)
        symptom = symptom_repo.log_symptom(
            user_id=user.id,
            symptom_description="Mild headache",
            severity=3,
        )

        assert allergy is not None
        assert allergy.user_id == user.id
        assert symptom is not None
        assert symptom.user_id == user.id
