"""
Tests for database models.
"""

import pytest
from backend.models.user import User
from backend.models.chat import ChatHistory
from backend.models.treatment import TreatmentPlan
from backend.models.health_metric import HealthMetric


class TestUserModel:
    """Tests for User model"""

    def test_create_user(self, test_db, sample_user_data):
        """Test creating a user"""
        user = User(
            username=sample_user_data["username"],
            full_name=sample_user_data["full_name"],
            age=sample_user_data["age"],
            gender=sample_user_data["gender"],
        )
        user.set_password(sample_user_data["password"])

        test_db.add(user)
        test_db.commit()

        assert user.id is not None
        assert user.username == sample_user_data["username"]
        assert user.full_name == sample_user_data["full_name"]

    def test_password_hashing(self, test_db, sample_user_data):
        """Test password hashing and verification"""
        user = User(
            username=sample_user_data["username"],
            full_name=sample_user_data["full_name"],
            age=sample_user_data["age"],
            gender=sample_user_data["gender"],
        )
        user.set_password(sample_user_data["password"])

        # Password should be hashed
        assert user.password_hash != sample_user_data["password"]

        # Should verify correct password
        assert user.check_password(sample_user_data["password"]) is True

        # Should reject incorrect password
        assert user.check_password("wrongpassword") is False

    def test_user_repr(self, test_db, sample_user_data):
        """Test user string representation"""
        user = User(
            username=sample_user_data["username"],
            full_name=sample_user_data["full_name"],
            age=sample_user_data["age"],
            gender=sample_user_data["gender"],
        )
        test_db.add(user)
        test_db.commit()

        repr_str = repr(user)
        assert "User" in repr_str
        assert sample_user_data["username"] in repr_str


class TestChatHistoryModel:
    """Tests for ChatHistory model"""

    def test_create_chat(self, test_db, sample_user_data, sample_chat_data):
        """Test creating a chat history entry"""
        # Create user first
        user = User(
            username=sample_user_data["username"],
            full_name=sample_user_data["full_name"],
            age=sample_user_data["age"],
            gender=sample_user_data["gender"],
        )
        test_db.add(user)
        test_db.commit()

        # Create chat
        chat = ChatHistory(
            user_id=user.id,
            message=sample_chat_data["message"],
            response=sample_chat_data["response"],
        )
        test_db.add(chat)
        test_db.commit()

        assert chat.id is not None
        assert chat.user_id == user.id
        assert chat.message == sample_chat_data["message"]
        assert chat.timestamp is not None


class TestTreatmentPlanModel:
    """Tests for TreatmentPlan model"""

    def test_create_treatment_plan(self, test_db, sample_user_data, sample_treatment_plan):
        """Test creating a treatment plan"""
        # Create user first
        user = User(
            username=sample_user_data["username"],
            full_name=sample_user_data["full_name"],
            age=sample_user_data["age"],
            gender=sample_user_data["gender"],
        )
        test_db.add(user)
        test_db.commit()

        # Create treatment plan
        plan = TreatmentPlan(
            user_id=user.id,
            title=sample_treatment_plan["title"],
            condition=sample_treatment_plan["condition"],
            plan_details=sample_treatment_plan["plan_details"],
        )
        test_db.add(plan)
        test_db.commit()

        assert plan.id is not None
        assert plan.user_id == user.id
        assert plan.title == sample_treatment_plan["title"]


class TestHealthMetricModel:
    """Tests for HealthMetric model"""

    def test_create_health_metric(self, test_db, sample_user_data, sample_health_metric):
        """Test creating a health metric"""
        # Create user first
        user = User(
            username=sample_user_data["username"],
            full_name=sample_user_data["full_name"],
            age=sample_user_data["age"],
            gender=sample_user_data["gender"],
        )
        test_db.add(user)
        test_db.commit()

        # Create health metric
        metric = HealthMetric(
            user_id=user.id,
            metric_type=sample_health_metric["metric_type"],
            value=sample_health_metric["value"],
            unit=sample_health_metric["unit"],
            notes=sample_health_metric["notes"],
        )
        test_db.add(metric)
        test_db.commit()

        assert metric.id is not None
        assert metric.user_id == user.id
        assert metric.value == sample_health_metric["value"]
