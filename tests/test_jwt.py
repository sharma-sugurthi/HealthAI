"""
Tests for JWT utilities.
"""

from backend.utils.jwt import create_access_token, create_refresh_token, verify_token


def test_verify_access_token_with_expected_type():
    """Access token should validate when expected type is access."""
    token = create_access_token({"sub": "1", "username": "testuser"})

    payload = verify_token(token, expected_type="access")

    assert payload is not None
    assert payload.get("sub") == "1"
    assert payload.get("type") == "access"


def test_verify_refresh_token_rejected_for_access_expected_type():
    """Refresh token must not pass access-token verification."""
    token = create_refresh_token({"sub": "1", "username": "testuser"})

    payload = verify_token(token, expected_type="access")

    assert payload is None


def test_verify_token_without_expected_type_accepts_valid_token():
    """Valid token should decode when no expected type is specified."""
    token = create_refresh_token({"sub": "1", "username": "testuser"})

    payload = verify_token(token)

    assert payload is not None
    assert payload.get("type") == "refresh"
