from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.pipelines.ingest_weather_forecast import WeatherForecastIngestPipeline
from app.schemas.weather_forecast import WeatherForecastRead
from app.pipelines.ingest_nasa_apod import NasaApodIngestPipeline
from app.schemas.nasa_apod import NasaApodRead
from app.pipelines.ingest_nasa_space_weather import NasaSpaceWeatherIngestPipeline
from app.schemas.nasa_space_weather import NasaSpaceWeatherNotificationRead
from app.pipelines.ingest_nasa_epic import NasaEpicIngestPipeline
from app.pipelines.ingest_nasa_neos import NasaNeoIngestPipeline
from app.schemas.nasa_epic import NasaEpicImageRead
from app.schemas.nasa_neo import NasaNeoCloseApproachRead
from app.pipelines.ingest_music_releases import MusicReleaseIngestPipeline
from app.schemas.music import MusicReleaseRead

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("/ingest-weather-forecast", response_model=list[WeatherForecastRead])
async def ingest_weather_forecast(
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    pipeline = WeatherForecastIngestPipeline(db)
    return await pipeline.run_for_location(location_key)

@router.post("/ingest-weather-forecast-all")
async def ingest_weather_forecast_all(db: Session = Depends(get_db)):
    pipeline = WeatherForecastIngestPipeline(db)
    return await pipeline.run_for_all_active_locations()

@router.post("/ingest-nasa-apod", response_model=NasaApodRead)
async def ingest_nasa_apod(db: Session = Depends(get_db)):
    pipeline = NasaApodIngestPipeline(db)
    return await pipeline.run()

@router.post(
    "/ingest-nasa-space-weather",
    response_model=list[NasaSpaceWeatherNotificationRead],
)
async def ingest_nasa_space_weather(db: Session = Depends(get_db)):
    pipeline = NasaSpaceWeatherIngestPipeline(db)
    return await pipeline.run()

@router.post("/ingest-nasa-neos", response_model=list[NasaNeoCloseApproachRead])
async def ingest_nasa_neos(db: Session = Depends(get_db)):
    pipeline = NasaNeoIngestPipeline(db)
    return await pipeline.run()


@router.post("/ingest-nasa-epic", response_model=NasaEpicImageRead | None)
async def ingest_nasa_epic(db: Session = Depends(get_db)):
    pipeline = NasaEpicIngestPipeline(db)
    return await pipeline.run()

@router.post("/ingest-music-releases", response_model=list[MusicReleaseRead])
async def ingest_music_releases(db: Session = Depends(get_db)):
    pipeline = MusicReleaseIngestPipeline(db)
    return await pipeline.run_for_all_artists()