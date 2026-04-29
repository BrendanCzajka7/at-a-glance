from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline

from app.pipelines.ingest_weather_forecast import WeatherForecastIngestPipeline
from app.schemas.weather_forecast import WeatherForecastRead

from app.pipelines.ingest_nasa_apod import NasaApodIngestPipeline
from app.schemas.nasa_apod import NasaApodRead

from app.pipelines.ingest_nasa_space_weather import NasaSpaceWeatherIngestPipeline
from app.schemas.nasa_space_weather import NasaSpaceWeatherNotificationRead

from app.pipelines.ingest_nasa_epic import NasaEpicIngestPipeline
from app.schemas.nasa_epic import NasaEpicImageRead

from app.pipelines.ingest_nasa_neos import NasaNeoIngestPipeline
from app.schemas.nasa_neo import NasaNeoCloseApproachRead

from app.pipelines.ingest_music_releases import MusicReleaseIngestPipeline
from app.schemas.music import MusicReleaseRead

from app.pipelines.ingest_tmdb_movies import TmdbMovieIngestPipeline
from app.schemas.tmdb import TmdbMovieReleaseRead

from app.schemas.ticketmaster import TicketmasterConcertRead
from app.pipelines.ingest_ticketmaster_concerts import TicketmasterConcertIngestPipeline

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("/ingest-weather-forecast", response_model=list[WeatherForecastRead])
async def ingest_weather_forecast(
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    pipeline = WeatherForecastIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="weather",
        event_type="ingest_weather_forecast_failed",
        message=f"Weather forecast ingest failed for location_key={location_key}",
        action=pipeline.run_for_location(location_key),
    )


@router.post("/ingest-weather-forecast-all")
async def ingest_weather_forecast_all(db: Session = Depends(get_db)):
    pipeline = WeatherForecastIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="weather",
        event_type="ingest_weather_forecast_all_failed",
        message="Weather forecast ingest failed for all active locations",
        action=pipeline.run_for_all_active_locations(),
    )


@router.post("/ingest-nasa-apod", response_model=NasaApodRead)
async def ingest_nasa_apod(db: Session = Depends(get_db)):
    pipeline = NasaApodIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="nasa_apod",
        event_type="ingest_nasa_apod_failed",
        message="NASA APOD ingest failed",
        action=pipeline.run(),
    )


@router.post(
    "/ingest-nasa-space-weather",
    response_model=list[NasaSpaceWeatherNotificationRead],
)
async def ingest_nasa_space_weather(db: Session = Depends(get_db)):
    pipeline = NasaSpaceWeatherIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="nasa_space_weather",
        event_type="ingest_nasa_space_weather_failed",
        message="NASA space weather ingest failed",
        action=pipeline.run(),
    )


@router.post("/ingest-nasa-neos", response_model=list[NasaNeoCloseApproachRead])
async def ingest_nasa_neos(db: Session = Depends(get_db)):
    pipeline = NasaNeoIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="nasa_neos",
        event_type="ingest_nasa_neos_failed",
        message="NASA NEO ingest failed",
        action=pipeline.run(),
    )


@router.post("/ingest-nasa-epic", response_model=NasaEpicImageRead | None)
async def ingest_nasa_epic(db: Session = Depends(get_db)):
    pipeline = NasaEpicIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="nasa_epic",
        event_type="ingest_nasa_epic_failed",
        message="NASA EPIC ingest failed",
        action=pipeline.run(),
    )


@router.post("/ingest-music-releases", response_model=list[MusicReleaseRead])
async def ingest_music_releases(db: Session = Depends(get_db)):
    pipeline = MusicReleaseIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="musicbrainz",
        event_type="ingest_music_releases_failed",
        message="MusicBrainz release ingest failed",
        action=pipeline.run_for_all_artists(),
    )


@router.post("/ingest-tmdb-movies", response_model=list[TmdbMovieReleaseRead])
async def ingest_tmdb_movies(db: Session = Depends(get_db)):
    pipeline = TmdbMovieIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="tmdb",
        event_type="ingest_tmdb_movies_failed",
        message="TMDB movie ingest failed",
        action=pipeline.run_for_all_watch_items(),
    )

@router.post(
    "/ingest-ticketmaster-concerts",
    response_model=list[TicketmasterConcertRead],
)
async def ingest_ticketmaster_concerts(
    location_key: str = Query(default="okaloosa_island"),
    radius_miles: int = Query(default=75, ge=1, le=250),
    db: Session = Depends(get_db),
):
    pipeline = TicketmasterConcertIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="ticketmaster",
        event_type="ingest_ticketmaster_concerts_failed",
        message=(
            "Ticketmaster concert ingest failed "
            f"for location_key={location_key}, radius_miles={radius_miles}"
        ),
        action=pipeline.run_for_location(
            location_key=location_key,
            radius_miles=radius_miles,
        ),
    )


@router.post("/ingest-ticketmaster-concerts-all")
async def ingest_ticketmaster_concerts_all(
    radius_miles: int = Query(default=75, ge=1, le=250),
    db: Session = Depends(get_db),
):
    pipeline = TicketmasterConcertIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="ticketmaster",
        event_type="ingest_ticketmaster_concerts_all_failed",
        message="Ticketmaster concert ingest failed for all active locations",
        action=pipeline.run_for_all_active_locations(radius_miles=radius_miles),
    )