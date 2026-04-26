from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.pipelines.ingest_weather_forecast import WeatherForecastIngestPipeline
from app.schemas.weather_forecast import WeatherForecastRead

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("/ingest-weather-forecast", response_model=list[WeatherForecastRead])
async def ingest_weather_forecast(
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    pipeline = WeatherForecastIngestPipeline(db)
    return await pipeline.run_for_location(location_key)