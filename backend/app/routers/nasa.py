from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.nasa_apod import NasaApodRead
from app.services.nasa_apod_service import NasaApodService

router = APIRouter(prefix="/api/nasa", tags=["nasa"])


@router.get("/apod/latest", response_model=NasaApodRead)
def get_latest_apod(db: Session = Depends(get_db)):
    apod = NasaApodService(db).get_latest()

    if not apod:
        raise HTTPException(
            status_code=404,
            detail="No NASA APOD data found. Run the ingest job first.",
        )

    return apod