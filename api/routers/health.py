"""
Health metrics router.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from api.schemas.health import HealthMetricCreate, HealthMetricResponse, HealthStatisticsResponse
from api.dependencies import get_db, get_current_user
from backend.services.health_service import HealthService
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/metrics", response_model=HealthMetricResponse, status_code=status.HTTP_201_CREATED)
async def record_metric(
    metric_data: HealthMetricCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a health metric."""
    try:
        health_service = HealthService(db)
        metric = health_service.record_metric(
            user_id=current_user['id'],
            metric_type=metric_data.metric_type,
            value=metric_data.value,
            unit=metric_data.unit,
            notes=metric_data.notes
        )
        return HealthMetricResponse(**metric)
    except Exception as e:
        logger.error(f"Error recording metric: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to record metric")


@router.get("/metrics", response_model=List[HealthMetricResponse])
async def get_metrics(
    metric_type: Optional[str] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health metrics."""
    try:
        health_service = HealthService(db)
        metrics = health_service.get_metrics(current_user['id'], metric_type, limit)
        return [HealthMetricResponse(**m) for m in metrics]
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch metrics")


@router.get("/statistics/{metric_type}", response_model=HealthStatisticsResponse)
async def get_statistics(
    metric_type: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific metric type."""
    try:
        health_service = HealthService(db)
        stats = health_service.get_statistics(current_user['id'], metric_type)
        
        if not stats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data found for this metric type")
        
        return HealthStatisticsResponse(**stats)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch statistics")
