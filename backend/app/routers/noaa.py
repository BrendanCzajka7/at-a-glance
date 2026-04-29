from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.pipelines.ingest_noaa import NoaaIngestPipeline

router = APIRouter(prefix="/api/noaa", tags=["noaa"])


@router.post("/ingest")
async def ingest_noaa(
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    pipeline = NoaaIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="noaa",
        event_type="ingest_noaa_failed",
        message=f"NOAA ingest failed for location_key={location_key}",
        action=pipeline.run_for_location(location_key),
    )


@router.post("/ingest-all")
async def ingest_noaa_all(db: Session = Depends(get_db)):
    pipeline = NoaaIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="noaa",
        event_type="ingest_noaa_all_failed",
        message="NOAA ingest failed",
        action=pipeline.run_all(),
    )


@router.post("/ingest-space-weather")
async def ingest_noaa_space_weather(db: Session = Depends(get_db)):
    pipeline = NoaaIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="noaa_space_weather",
        event_type="ingest_noaa_space_weather_failed",
        message="NOAA SWPC space weather ingest failed",
        action=pipeline.run_space_weather(),
    )