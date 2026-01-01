"""
Health repository for health metric operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.models.health_metric import HealthMetric
from backend.repositories.base import BaseRepository
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class HealthRepository(BaseRepository[HealthMetric]):
    """Repository for HealthMetric model operations"""
    
    def __init__(self, session: Session):
        super().__init__(HealthMetric, session)
    
    def add_metric(self, user_id: int, metric_type: str, value: float,
                  unit: str, notes: Optional[str] = None) -> HealthMetric:
        """
        Add a health metric.
        
        Args:
            user_id: User ID
            metric_type: Type of metric (e.g., "Heart Rate")
            value: Metric value
            unit: Unit of measurement
            notes: Optional notes
        
        Returns:
            Created HealthMetric instance
        """
        try:
            metric = HealthMetric(
                user_id=user_id,
                metric_type=metric_type,
                value=value,
                unit=unit,
                notes=notes
            )
            self.session.add(metric)
            self.session.commit()
            self.session.refresh(metric)
            
            logger.info(f"Added {metric_type} metric for user_id={user_id}")
            return metric
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding health metric: {str(e)}")
            raise
    
    def get_user_metrics(self, user_id: int, metric_type: Optional[str] = None,
                        limit: int = 100) -> List[HealthMetric]:
        """
        Get health metrics for a user.
        
        Args:
            user_id: User ID
            metric_type: Optional filter by metric type
            limit: Maximum number of records
        
        Returns:
            List of HealthMetric instances, ordered by recorded_at descending
        """
        query = self.session.query(HealthMetric).filter(HealthMetric.user_id == user_id)
        
        if metric_type:
            query = query.filter(HealthMetric.metric_type == metric_type)
        
        return query.order_by(desc(HealthMetric.recorded_at)).limit(limit).all()
    
    def get_latest_metric(self, user_id: int, metric_type: str) -> Optional[HealthMetric]:
        """
        Get the most recent metric of a specific type.
        
        Args:
            user_id: User ID
            metric_type: Type of metric
        
        Returns:
            Latest HealthMetric instance or None
        """
        return (
            self.session.query(HealthMetric)
            .filter(
                HealthMetric.user_id == user_id,
                HealthMetric.metric_type == metric_type
            )
            .order_by(desc(HealthMetric.recorded_at))
            .first()
        )
    
    def get_metric_types(self, user_id: int) -> List[str]:
        """
        Get all unique metric types for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of metric type names
        """
        results = (
            self.session.query(HealthMetric.metric_type)
            .filter(HealthMetric.user_id == user_id)
            .distinct()
            .all()
        )
        return [r[0] for r in results]
    
    def delete_metric(self, metric_id: int, user_id: int) -> bool:
        """
        Delete a health metric (with user ownership check).
        
        Args:
            metric_id: Metric ID
            user_id: User ID (for ownership verification)
        
        Returns:
            True if deleted, False if not found or not owned by user
        """
        try:
            metric = (
                self.session.query(HealthMetric)
                .filter(
                    HealthMetric.id == metric_id,
                    HealthMetric.user_id == user_id
                )
                .first()
            )
            
            if metric:
                self.session.delete(metric)
                self.session.commit()
                logger.info(f"Deleted health metric id={metric_id}")
                return True
            
            return False
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting health metric: {str(e)}")
            raise
