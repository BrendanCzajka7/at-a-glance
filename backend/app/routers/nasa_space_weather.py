from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.nasa_space_weather import NasaSpaceWeatherNotificationRead
from app.services.nasa_space_weather_service import NasaSpaceWeatherService

router = APIRouter(prefix="/api/nasa/space-weather", tags=["nasa"])


@router.get("/notifications", response_model=list[NasaSpaceWeatherNotificationRead])
def get_space_weather_notifications(
    days: int = Query(default=7, ge=1, le=30),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    end = datetime.utcnow()
    start = end - timedelta(days=days)

    service = NasaSpaceWeatherService(db)

    return service.list_between(
        start=start,
        end=end,
        limit=limit,
    )