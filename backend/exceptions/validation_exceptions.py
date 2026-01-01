"""
Validation-related exceptions.
"""


class ValidationError(Exception):
    """Base exception for validation errors"""
    pass


class InvalidInputError(ValidationError):
    """Raised when input fails validation"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = f"Invalid {field}: {message}"
        super().__init__(self.message)


class InputTooLongError(ValidationError):
    """Raised when input exceeds maximum length"""
    def __init__(self, field: str, max_length: int, actual_length: int):
        self.field = field
        self.max_length = max_length
        self.actual_length = actual_length
        self.message = f"{field} exceeds maximum length of {max_length} (got {actual_length})"
        super().__init__(self.message)


class InputTooShortError(ValidationError):
    """Raised when input is below minimum length"""
    def __init__(self, field: str, min_length: int, actual_length: int):
        self.field = field
        self.min_length = min_length
        self.actual_length = actual_length
        self.message = f"{field} must be at least {min_length} characters (got {actual_length})"
        super().__init__(self.message)


class InvalidFormatError(ValidationError):
    """Raised when input format is invalid"""
    def __init__(self, field: str, expected_format: str):
        self.field = field
        self.expected_format = expected_format
        self.message = f"{field} has invalid format. Expected: {expected_format}"
        super().__init__(self.message)


class ValueOutOfRangeError(ValidationError):
    """Raised when numeric value is out of acceptable range"""
    def __init__(self, field: str, min_val: float, max_val: float, actual_val: float):
        self.field = field
        self.min_val = min_val
        self.max_val = max_val
        self.actual_val = actual_val
        self.message = f"{field} must be between {min_val} and {max_val} (got {actual_val})"
        super().__init__(self.message)
