from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.weather_snapshot import WeatherSnapshotRead
from app.services.weather_service import WeatherService

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/latest", response_model=list[WeatherSnapshotRead])
def get_latest_weather(db: Session = Depends(get_db)):
    service = WeatherService(db)
    return service.get_latest_weather(limit=20)