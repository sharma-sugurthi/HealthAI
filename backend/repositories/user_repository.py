"""
User repository for user-related database operations.
"""

from typing import Optional
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class UserRepository(BaseRepository[User]):
    """Repository for User model operations"""

    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username to search for

        Returns:
            User instance or None
        """
        return self.session.query(User).filter(User.username == username).first()

    def create_user(
        self, username: str, password: str, full_name: str, age: int, gender: str
    ) -> User:
        """
        Create a new user with hashed password.

        Args:
            username: Unique username
            password: Plain text password (will be hashed)
            full_name: User's full name
            age: User's age
            gender: User's gender

        Returns:
            Created User instance

        Raises:
            Exception: If username already exists or creation fails
        """
        try:
            # Check if username exists
            existing_user = self.get_by_username(username)
            if existing_user:
                raise ValueError(f"Username '{username}' already exists")

            # Create user
            user = User(username=username, full_name=full_name, age=age, gender=gender)
            user.set_password(password)

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            logger.info(f"Created user: {username}")
            return user

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating user {username}: {str(e)}")
            raise

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password.

        Args:
            username: Username
            password: Plain text password

        Returns:
            User instance if authenticated, None otherwise
        """
        user = self.get_by_username(username)
        if user and user.check_password(password):
            logger.info(f"User authenticated: {username}")
            return user

        logger.warning(f"Authentication failed for username: {username}")
        return None

    def username_exists(self, username: str) -> bool:
        """
        Check if username exists.

        Args:
            username: Username to check

        Returns:
            True if exists, False otherwise
        """
        return self.get_by_username(username) is not None
