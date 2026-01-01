"""
Dependency injection for FastAPI.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.utils.database import get_db_manager
from backend.utils.jwt import verify_token
from backend.utils.logger import get_logger

logger = get_logger(__name__)
security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database session.

    Yields:
        Database session
    """
    db_manager = get_db_manager()
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> dict:
    """
    Dependency for getting current authenticated user.

    Args:
        credentials: HTTP authorization credentials
        db: Database session

    Returns:
        User data dictionary

    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        logger.warning("Invalid token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"id": int(user_id), "username": payload.get("username")}


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency for getting current active user.
    Can be extended to check if user is active/verified.

    Args:
        current_user: Current user from token

    Returns:
        User data dictionary
    """
    return current_user
