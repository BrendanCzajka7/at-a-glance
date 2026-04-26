from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.pipelines.ingest_weather import WeatherIngestPipeline
from app.schemas.weather_snapshot import WeatherSnapshotRead

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("/ingest-weather", response_model=WeatherSnapshotRead)
async def ingest_weather(db: Session = Depends(get_db)):
    pipeline = WeatherIngestPipeline(db)
    return await pipeline.run_for_okaloosa_island()