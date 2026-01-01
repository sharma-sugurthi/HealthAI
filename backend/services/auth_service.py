"""
Authentication service for user registration and login.
"""

from typing import Dict, Optional
from sqlalchemy.orm import Session
from backend.repositories.user_repository import UserRepository
from backend.exceptions.auth_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from backend.utils.logger import get_logger
from validation import InputValidator

logger = get_logger(__name__)


class AuthService:
    """Service for authentication and user management"""

    def __init__(self, session: Session):
        """
        Initialize auth service.

        Args:
            session: Database session
        """
        self.session = session
        self.user_repo = UserRepository(session)

    def register_user(
        self, username: str, password: str, full_name: str, age: int, gender: str
    ) -> Dict:
        """
        Register a new user.

        Args:
            username: Unique username
            password: Plain text password
            full_name: User's full name
            age: User's age
            gender: User's gender

        Returns:
            Dictionary with user information

        Raises:
            ValidationError: If input validation fails
            UserAlreadyExistsError: If username already exists
        """
        try:
            # Validate inputs
            username = InputValidator.validate_username(username)
            password = InputValidator.validate_password(password)
            full_name = InputValidator.validate_name(full_name)
            age = InputValidator.validate_age(age)

            # Check if user exists
            if self.user_repo.username_exists(username):
                raise UserAlreadyExistsError(username)

            # Create user
            user = self.user_repo.create_user(
                username=username, password=password, full_name=full_name, age=age, gender=gender
            )

            logger.info(f"User registered successfully: {username}")

            return {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "age": user.age,
                "gender": user.gender,
            }

        except Exception as e:
            logger.error(f"Registration failed for {username}: {str(e)}")
            raise

    def login_user(self, username: str, password: str) -> Dict:
        """
        Authenticate and login user.

        Args:
            username: Username
            password: Plain text password

        Returns:
            Dictionary with user information

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        try:
            # Validate inputs
            username = InputValidator.validate_username(username)
            password = InputValidator.validate_password(password)

            # Authenticate
            user = self.user_repo.authenticate(username, password)

            if not user:
                raise InvalidCredentialsError()

            logger.info(f"User logged in successfully: {username}")

            return {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "age": user.age,
                "gender": user.gender,
            }

        except InvalidCredentialsError:
            raise
        except Exception as e:
            logger.error(f"Login failed for {username}: {str(e)}")
            raise InvalidCredentialsError()

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Get user information by ID.

        Args:
            user_id: User ID

        Returns:
            Dictionary with user information or None
        """
        user = self.user_repo.get_by_id(user_id)

        if not user:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "age": user.age,
            "gender": user.gender,
        }

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Get user information by username.

        Args:
            username: Username

        Returns:
            Dictionary with user information or None
        """
        user = self.user_repo.get_by_username(username)

        if not user:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "age": user.age,
            "gender": user.gender,
        }
