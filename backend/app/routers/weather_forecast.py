from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.locations import get_location
from app.core.time import now_for_timezone
from app.schemas.weather_forecast import WeatherForecastRead
from app.services.weather_forecast_service import WeatherForecastService

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/forecast", response_model=list[WeatherForecastRead])
def get_weather_forecast(
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    location = get_location(location_key)

    if start is None:
        start = now_for_timezone(location.timezone)

    if end is None:
        end = start + timedelta(days=7)

    service = WeatherForecastService(db)

    return service.list_forecasts_between(
        start=start,
        end=end,
        location_key=location.key,
    )