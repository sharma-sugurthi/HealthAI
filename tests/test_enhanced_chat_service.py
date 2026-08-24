"""Regression tests for enhanced medical chat safety behavior."""

from api.schemas.medical_history import ContextualMessageResponse, SymptomAnalysisResponse
from backend.models.user import User
from backend.services.enhanced_chat_service import EnhancedChatService


def _create_user(test_db):
    user = User(username="safetyuser", full_name="Safety User", age=40, gender="Other")
    user.set_password("secret123")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


def test_contextual_message_detects_emergency_without_ai_client(test_db, monkeypatch):
    """Emergency detection must not depend on an AI provider being configured."""
    monkeypatch.setattr("backend.services.enhanced_chat_service.get_ai_client", lambda: None)
    user = _create_user(test_db)

    result = EnhancedChatService(test_db).send_contextual_message(
        user.id, "I have severe chest pain and cannot breathe"
    )

    assert result["has_emergency"] is True
    assert result["safety_flags"] == ["EMERGENCY_DETECTED"]
    assert result["severity"] == "high"
    ContextualMessageResponse(**result)


def test_symptom_analysis_detects_emergency_without_ai_client(test_db, monkeypatch):
    """Emergency symptom analysis should return the declared response shape."""
    monkeypatch.setattr("backend.services.enhanced_chat_service.get_ai_client", lambda: None)
    user = _create_user(test_db)

    result = EnhancedChatService(test_db).analyze_symptoms_with_context(
        user.id, "I have severe chest pain and cannot breathe"
    )

    assert result["has_emergency"] is True
    assert result["safety_flags"] == ["EMERGENCY_DETECTED"]
    assert result["symptoms"] == "I have severe chest pain and cannot breathe"
    assert "SEEK IMMEDIATE MEDICAL ATTENTION" in result["analysis"]
    SymptomAnalysisResponse(**result)
