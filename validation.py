"""
Input validation utilities for HealthAI application.
Provides sanitization and validation for user inputs.
"""

import re
from typing import Optional


class ValidationError(Exception):
    """Custom exception for validation errors"""

    pass


class InputValidator:
    """Validates and sanitizes user inputs"""

    # Maximum lengths for various inputs
    MAX_USERNAME_LENGTH = 50
    MAX_PASSWORD_LENGTH = 128
    MAX_NAME_LENGTH = 100
    MAX_MESSAGE_LENGTH = 5000
    MAX_SYMPTOM_LENGTH = 2000
    MAX_CONDITION_LENGTH = 200
    MAX_NOTES_LENGTH = 1000

    # Minimum lengths
    MIN_USERNAME_LENGTH = 3
    MIN_PASSWORD_LENGTH = 6
    MIN_NAME_LENGTH = 2

    @staticmethod
    def sanitize_text(text: str, max_length: int) -> str:
        """
        Sanitize text input by removing potentially dangerous characters
        and enforcing length limits.
        """
        if not isinstance(text, str):
            raise ValidationError("Input must be a string")

        # Strip whitespace
        text = text.strip()

        # Enforce max length
        if len(text) > max_length:
            raise ValidationError(f"Input exceeds maximum length of {max_length} characters")

        # Remove null bytes and other control characters
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

        return text

    @classmethod
    def validate_username(cls, username: str) -> str:
        """Validate and sanitize username"""
        username = cls.sanitize_text(username, cls.MAX_USERNAME_LENGTH)

        if len(username) < cls.MIN_USERNAME_LENGTH:
            raise ValidationError(f"Username must be at least {cls.MIN_USERNAME_LENGTH} characters")

        # Only allow alphanumeric, underscore, and hyphen
        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            raise ValidationError(
                "Username can only contain letters, numbers, underscores, and hyphens"
            )

        return username

    @classmethod
    def validate_password(cls, password: str) -> str:
        """Validate password (don't sanitize - preserve all characters)"""
        if not isinstance(password, str):
            raise ValidationError("Password must be a string")

        if len(password) < cls.MIN_PASSWORD_LENGTH:
            raise ValidationError(f"Password must be at least {cls.MIN_PASSWORD_LENGTH} characters")

        if len(password) > cls.MAX_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password exceeds maximum length of {cls.MAX_PASSWORD_LENGTH} characters"
            )

        return password

    @classmethod
    def validate_name(cls, name: str) -> str:
        """Validate and sanitize full name"""
        name = cls.sanitize_text(name, cls.MAX_NAME_LENGTH)

        if len(name) < cls.MIN_NAME_LENGTH:
            raise ValidationError(f"Name must be at least {cls.MIN_NAME_LENGTH} characters")

        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s'-]+$", name):
            raise ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes")

        return name

    @classmethod
    def validate_age(cls, age: int) -> int:
        """Validate age"""
        if not isinstance(age, int):
            raise ValidationError("Age must be a number")

        if age < 1 or age > 150:
            raise ValidationError("Age must be between 1 and 150")

        return age

    @classmethod
    def validate_message(cls, message: str) -> str:
        """Validate and sanitize chat message"""
        message = cls.sanitize_text(message, cls.MAX_MESSAGE_LENGTH)

        if len(message) == 0:
            raise ValidationError("Message cannot be empty")

        return message

    @classmethod
    def validate_symptoms(cls, symptoms: str) -> str:
        """Validate and sanitize symptom description"""
        symptoms = cls.sanitize_text(symptoms, cls.MAX_SYMPTOM_LENGTH)

        if len(symptoms) == 0:
            raise ValidationError("Symptom description cannot be empty")

        return symptoms

    @classmethod
    def validate_condition(cls, condition: str) -> str:
        """Validate and sanitize medical condition"""
        condition = cls.sanitize_text(condition, cls.MAX_CONDITION_LENGTH)

        if len(condition) == 0:
            raise ValidationError("Condition cannot be empty")

        return condition

    @classmethod
    def validate_notes(cls, notes: Optional[str]) -> Optional[str]:
        """Validate and sanitize optional notes"""
        if notes is None or notes.strip() == "":
            return None

        return cls.sanitize_text(notes, cls.MAX_NOTES_LENGTH)

    @classmethod
    def validate_metric_value(cls, value: float, metric_type: str) -> float:
        """Validate health metric value based on type"""
        if not isinstance(value, (int, float)):
            raise ValidationError("Metric value must be a number")

        # Define reasonable ranges for different metrics
        ranges = {
            "Heart Rate": (20, 300),
            "Blood Pressure (Systolic)": (50, 300),
            "Blood Pressure (Diastolic)": (30, 200),
            "Blood Glucose": (20, 600),
            "Weight": (1, 500),
            "Temperature": (90, 110),
            "Oxygen Saturation": (50, 100),
        }

        if metric_type in ranges:
            min_val, max_val = ranges[metric_type]
            if value < min_val or value > max_val:
                raise ValidationError(f"{metric_type} must be between {min_val} and {max_val}")

        return float(value)
