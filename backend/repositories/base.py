"""
Base repository with common CRUD operations.
"""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from backend.models.user import Base
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Generic type for models
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common database operations"""

    def __init__(self, model: Type[ModelType], session: Session):
        """
        Initialize repository.

        Args:
            model: SQLAlchemy model class
            session: Database session
        """
        self.model = model
        self.session = session

    def create(self, **kwargs) -> ModelType:
        """
        Create a new record.

        Args:
            **kwargs: Model attributes

        Returns:
            Created model instance
        """
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)
            logger.info(f"Created {self.model.__name__} with id={instance.id}")
            return instance
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get record by ID.

        Args:
            id: Record ID

        Returns:
            Model instance or None
        """
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """
        Get all records with pagination.

        Args:
            limit: Maximum number of records
            offset: Number of records to skip

        Returns:
            List of model instances
        """
        return self.session.query(self.model).limit(limit).offset(offset).all()

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """
        Update a record.

        Args:
            id: Record ID
            **kwargs: Attributes to update

        Returns:
            Updated model instance or None
        """
        try:
            instance = self.get_by_id(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                self.session.commit()
                self.session.refresh(instance)
                logger.info(f"Updated {self.model.__name__} with id={id}")
            return instance
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            raise

    def delete(self, id: int) -> bool:
        """
        Delete a record.

        Args:
            id: Record ID

        Returns:
            True if deleted, False if not found
        """
        try:
            instance = self.get_by_id(id)
            if instance:
                self.session.delete(instance)
                self.session.commit()
                logger.info(f"Deleted {self.model.__name__} with id={id}")
                return True
            return False
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting {self.model.__name__}: {str(e)}")
            raise

    def count(self) -> int:
        """
        Count total records.

        Returns:
            Total count
        """
        return self.session.query(self.model).count()
