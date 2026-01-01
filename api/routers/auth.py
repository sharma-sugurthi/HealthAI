"""
Authentication router for user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from api.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from api.dependencies import get_db, get_current_user
from backend.services.auth_service import AuthService
from backend.utils.jwt import create_access_token, create_refresh_token
from backend.utils.logger import get_logger
from backend.exceptions.auth_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from backend.exceptions.validation_exceptions import ValidationError

logger = get_logger(__name__)
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user data
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.register_user(
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name,
            age=user_data.age,
            gender=user_data.gender,
        )
        logger.info(f"User registered via API: {user['username']}")
        return UserResponse(**user)

    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login and get access token.

    Args:
        credentials: Login credentials
        db: Database session

    Returns:
        Access and refresh tokens
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.login_user(credentials.username, credentials.password)

        # Create tokens
        access_token = create_access_token(
            data={"sub": str(user["id"]), "username": user["username"]}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user["id"]), "username": user["username"]}
        )

        logger.info(f"User logged in via API: {user['username']}")

        return TokenResponse(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get current user information.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User information
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.get_user_by_id(current_user["id"])

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return UserResponse(**user)

    except Exception as e:
        logger.error(f"Error fetching user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch user info"
        )
