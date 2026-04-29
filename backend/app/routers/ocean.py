from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.pipelines.ingest_ocean_conditions import OceanConditionsIngestPipeline
from app.schemas.ocean_conditions import OceanConditionsRead
from app.services.ocean_conditions_service import OceanConditionsService

router = APIRouter(prefix="/api/ocean", tags=["ocean"])


@router.post("/ingest", response_model=OceanConditionsRead | None)
async def ingest_ocean_conditions(
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    pipeline = OceanConditionsIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="ndbc",
        event_type="ingest_ocean_conditions_failed",
        message=f"NDBC ocean conditions ingest failed for location_key={location_key}",
        action=pipeline.run_for_location(location_key),
    )


@router.get("/conditions/latest", response_model=OceanConditionsRead | None)
def get_latest_ocean_conditions(
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    return OceanConditionsService(db).get_latest_for_location(
        location_key=location_key,
    )