from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.pipelines.ingest_usgs_earthquakes import UsgsEarthquakeIngestPipeline
from app.schemas.usgs import UsgsEarthquakeRead
from app.services.usgs_earthquake_service import UsgsEarthquakeService

router = APIRouter(prefix="/api/usgs", tags=["usgs"])


@router.post("/ingest-earthquakes", response_model=list[UsgsEarthquakeRead])
async def ingest_earthquakes(db: Session = Depends(get_db)):
    pipeline = UsgsEarthquakeIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="usgs",
        event_type="ingest_usgs_earthquakes_failed",
        message="USGS earthquake ingest failed",
        action=pipeline.run(),
    )


@router.get("/earthquakes/recent", response_model=list[UsgsEarthquakeRead])
def list_recent_earthquakes(db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(hours=24)
    return UsgsEarthquakeService(db).list_since(since=since)