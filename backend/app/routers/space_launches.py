from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.pipelines.ingest_space_launches import SpaceLaunchIngestPipeline
from app.schemas.space_launch import SpaceLaunchRead
from app.services.space_launch_service import SpaceLaunchService

router = APIRouter(prefix="/api/space-launches", tags=["space-launches"])


@router.post("/ingest", response_model=list[SpaceLaunchRead])
async def ingest_space_launches(db: Session = Depends(get_db)):
    pipeline = SpaceLaunchIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="launch_library",
        event_type="ingest_space_launches_failed",
        message="Launch Library 2 space launch ingest failed",
        action=pipeline.run(),
    )


@router.get("", response_model=list[SpaceLaunchRead])
def list_space_launches(
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: Session = Depends(get_db),
):
    return SpaceLaunchService(db).list_between(
        start=start,
        end=end,
    )