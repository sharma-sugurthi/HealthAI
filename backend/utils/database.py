"""
Database utility for managing database connections and sessions.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import backend.models  # noqa: F401 - ensures all models are registered in Base metadata
from backend.models.user import Base
from config import config


class DatabaseManager:
    """Manages database connections and session lifecycle"""

    def __init__(self, database_url: str = None):
        """
        Initialize database manager.

        Args:
            database_url: Database connection string. If None, uses config.DATABASE_URL
        """
        self.database_url = database_url or config.DATABASE_URL

        # Configure engine based on database type
        if "sqlite" in self.database_url:
            # SQLite-specific configuration
            self.engine = create_engine(
                self.database_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
            )
        else:
            # PostgreSQL/MySQL configuration with connection pooling
            self.engine = create_engine(
                self.database_url,
                pool_size=config.DB_POOL_SIZE,
                max_overflow=config.DB_MAX_OVERFLOW,
                pool_pre_ping=config.DB_POOL_PRE_PING,
                pool_recycle=config.DB_POOL_RECYCLE,
            )

        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy Session instance
        """
        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope for database operations.

        Usage:
            with db_manager.session_scope() as session:
                user = session.query(User).first()

        Yields:
            SQLAlchemy Session instance
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def close(self):
        """Close all database connections"""
        self.engine.dispose()


# Global database manager instance
_db_manager = None


def get_db_manager() -> DatabaseManager:
    """
    Get the global database manager instance.

    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def get_db_session() -> Session:
    """
    Get a new database session.

    Returns:
        SQLAlchemy Session instance
    """
    return get_db_manager().get_session()
