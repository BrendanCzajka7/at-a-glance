from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.core.time import now_for_timezone
from app.nature_themes import NATURE_THEMES
from app.pipelines.ingest_nature_photo import NaturePhotoIngestPipeline
from app.schemas.nature import NaturePhotoRead
from app.services.nature_photo_service import NaturePhotoService

router = APIRouter(prefix="/api/nature", tags=["nature"])


@router.get("/themes", response_model=list[str])
def list_nature_themes():
    return NATURE_THEMES


@router.post("/ingest-photo", response_model=NaturePhotoRead | None)
async def ingest_nature_photo(
    theme: str = Query(...),
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


@router.post("/ingest-all", response_model=list[NaturePhotoRead])
async def ingest_all_nature_photos(db: Session = Depends(get_db)):
    pipeline = NaturePhotoIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="pexels",
        event_type="ingest_nature_photos_failed",
        message="Pexels nature photo ingest failed for all themes",
        action=pipeline.run_all_for_today(),
    )


@router.get("/photos/today", response_model=list[NaturePhotoRead])
def list_today_nature_photos(db: Session = Depends(get_db)):
    today = now_for_timezone("UTC").date()
    return NaturePhotoService(db).list_for_date(photo_date=today)