"""
Authentication-related exceptions.
"""


class AuthenticationError(Exception):
    """Base exception for authentication errors"""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid"""

    def __init__(self, message: str = "Invalid username or password"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsError(AuthenticationError):
    """Raised when attempting to create a user with existing username"""

    def __init__(self, username: str):
        self.message = f"User with username '{username}' already exists"
        super().__init__(self.message)


class UserNotFoundError(AuthenticationError):
    """Raised when user is not found"""

    def __init__(self, identifier: str):
        self.message = f"User not found: {identifier}"
        super().__init__(self.message)


class SessionExpiredError(AuthenticationError):
    """Raised when user session has expired"""

    def __init__(self, message: str = "Session has expired. Please login again."):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(AuthenticationError):
    """Raised when user is not authorized to perform an action"""

    def __init__(self, message: str = "You are not authorized to perform this action"):
        self.message = message
        super().__init__(self.message)
