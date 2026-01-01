"""
Tests for validation module.
"""
import pytest
from validation import InputValidator, ValidationError


class TestInputValidator:
    """Tests for InputValidator class"""
    
    def test_validate_username_valid(self):
        """Test valid username validation"""
        username = InputValidator.validate_username("testuser123")
        assert username == "testuser123"
    
    def test_validate_username_too_short(self):
        """Test username too short"""
        with pytest.raises(ValidationError):
            InputValidator.validate_username("ab")
    
    def test_validate_username_invalid_chars(self):
        """Test username with invalid characters"""
        with pytest.raises(ValidationError):
            InputValidator.validate_username("test@user")
    
    def test_validate_password_valid(self):
        """Test valid password validation"""
        password = InputValidator.validate_password("password123")
        assert password == "password123"
    
    def test_validate_password_too_short(self):
        """Test password too short"""
        with pytest.raises(ValidationError):
            InputValidator.validate_password("12345")
    
    def test_validate_name_valid(self):
        """Test valid name validation"""
        name = InputValidator.validate_name("John Doe")
        assert name == "John Doe"
    
    def test_validate_name_with_hyphen(self):
        """Test name with hyphen"""
        name = InputValidator.validate_name("Mary-Jane Smith")
        assert name == "Mary-Jane Smith"
    
    def test_validate_age_valid(self):
        """Test valid age validation"""
        age = InputValidator.validate_age(30)
        assert age == 30
    
    def test_validate_age_out_of_range(self):
        """Test age out of range"""
        with pytest.raises(ValidationError):
            InputValidator.validate_age(200)
    
    def test_validate_message_valid(self):
        """Test valid message validation"""
        message = "I have a headache"
        validated = InputValidator.validate_message(message)
        assert validated == message
    
    def test_validate_message_empty(self):
        """Test empty message"""
        with pytest.raises(ValidationError):
            InputValidator.validate_message("")
    
    def test_validate_metric_value_heart_rate(self):
        """Test heart rate validation"""
        value = InputValidator.validate_metric_value(75.0, "Heart Rate")
        assert value == 75.0
    
    def test_validate_metric_value_out_of_range(self):
        """Test metric value out of range"""
        with pytest.raises(ValidationError):
            InputValidator.validate_metric_value(500.0, "Heart Rate")
    
    def test_sanitize_text_removes_control_chars(self):
        """Test that control characters are removed"""
        text = "Hello\x00World"
        sanitized = InputValidator.sanitize_text(text, 100)
        assert "\x00" not in sanitized
    
    def test_sanitize_text_enforces_max_length(self):
        """Test max length enforcement"""
        text = "a" * 200
        with pytest.raises(ValidationError):
            InputValidator.sanitize_text(text, 100)
