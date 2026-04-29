from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.nature_themes import NATURE_THEMES
from app.pipelines.ingest_nature_photo import NaturePhotoIngestPipeline
from app.schemas.nature import NaturePhotoRead
from app.services.nature_photo_service import NaturePhotoService
from app.core.time import now_for_timezone

router = APIRouter(prefix="/api/nature", tags=["nature"])


@router.get("/themes", response_model=list[str])
def list_nature_themes():
    return NATURE_THEMES


@router.post("/ingest-photo", response_model=NaturePhotoRead | None)
async def ingest_nature_photo(
    theme: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    pipeline = NaturePhotoIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="pexels",
        event_type="ingest_nature_photo_failed",
        message=f"Pexels nature photo ingest failed for theme={theme}",
        action=pipeline.run_for_today(theme=theme),
    )


@router.get("/photo/today", response_model=NaturePhotoRead | None)
def get_today_nature_photo(db: Session = Depends(get_db)):
    today = now_for_timezone("UTC").date()
    return NaturePhotoService(db).get_for_date(photo_date=today)