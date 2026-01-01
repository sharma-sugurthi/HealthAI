"""
Health service for managing health metrics.
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from backend.repositories.health_repository import HealthRepository
from backend.utils.logger import get_logger
from validation import InputValidator

logger = get_logger(__name__)


class HealthService:
    """Service for health metric operations"""

    def __init__(self, session: Session):
        """
        Initialize health service.

        Args:
            session: Database session
        """
        self.session = session
        self.health_repo = HealthRepository(session)

    def record_metric(
        self, user_id: int, metric_type: str, value: float, unit: str, notes: Optional[str] = None
    ) -> Dict:
        """
        Record a health metric.

        Args:
            user_id: User ID
            metric_type: Type of metric
            value: Metric value
            unit: Unit of measurement
            notes: Optional notes

        Returns:
            Dictionary with metric information

        Raises:
            ValidationError: If validation fails
        """
        try:
            # Validate value
            value = InputValidator.validate_metric_value(value, metric_type)

            # Validate notes
            if notes:
                notes = InputValidator.validate_notes(notes)

            # Save metric
            metric = self.health_repo.add_metric(
                user_id=user_id, metric_type=metric_type, value=value, unit=unit, notes=notes
            )

            logger.info(f"Recorded {metric_type} for user_id={user_id}")

            return {
                "id": metric.id,
                "metric_type": metric.metric_type,
                "value": metric.value,
                "unit": metric.unit,
                "notes": metric.notes,
                "recorded_at": metric.recorded_at,
            }

        except Exception as e:
            logger.error(f"Error recording metric: {str(e)}")
            raise

    def get_metrics(
        self, user_id: int, metric_type: Optional[str] = None, limit: int = 100
    ) -> List[Dict]:
        """
        Get health metrics for a user.

        Args:
            user_id: User ID
            metric_type: Optional filter by type
            limit: Maximum number of records

        Returns:
            List of metrics
        """
        metrics = self.health_repo.get_user_metrics(user_id, metric_type, limit)

        return [
            {
                "id": m.id,
                "metric_type": m.metric_type,
                "value": m.value,
                "unit": m.unit,
                "notes": m.notes,
                "recorded_at": m.recorded_at,
            }
            for m in metrics
        ]

    def get_statistics(self, user_id: int, metric_type: str) -> Optional[Dict]:
        """
        Get statistics for a specific metric type.

        Args:
            user_id: User ID
            metric_type: Type of metric

        Returns:
            Dictionary with statistics or None if no data
        """
        metrics = self.health_repo.get_user_metrics(user_id, metric_type)

        if not metrics:
            return None

        values = [m.value for m in metrics]

        return {
            "metric_type": metric_type,
            "count": len(values),
            "latest": values[0],  # First is most recent
            "average": sum(values) / len(values),
            "minimum": min(values),
            "maximum": max(values),
            "unit": metrics[0].unit,
        }

    def get_latest_metric(self, user_id: int, metric_type: str) -> Optional[Dict]:
        """
        Get the most recent metric of a specific type.

        Args:
            user_id: User ID
            metric_type: Type of metric

        Returns:
            Dictionary with metric or None
        """
        metric = self.health_repo.get_latest_metric(user_id, metric_type)

        if not metric:
            return None

        return {
            "id": metric.id,
            "metric_type": metric.metric_type,
            "value": metric.value,
            "unit": metric.unit,
            "notes": metric.notes,
            "recorded_at": metric.recorded_at,
        }

    def get_metric_types(self, user_id: int) -> List[str]:
        """
        Get all metric types for a user.

        Args:
            user_id: User ID

        Returns:
            List of metric type names
        """
        return self.health_repo.get_metric_types(user_id)

    def delete_metric(self, user_id: int, metric_id: int) -> bool:
        """
        Delete a health metric.

        Args:
            user_id: User ID
            metric_id: Metric ID

        Returns:
            True if deleted, False otherwise
        """
        deleted = self.health_repo.delete_metric(metric_id, user_id)

        if deleted:
            logger.info(f"Deleted metric id={metric_id} for user_id={user_id}")

        return deleted
