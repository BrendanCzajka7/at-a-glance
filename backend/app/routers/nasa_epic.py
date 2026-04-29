from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.nasa_epic import NasaEpicImageRead
from app.services.nasa_epic_service import NasaEpicService

router = APIRouter(prefix="/api/nasa/epic", tags=["nasa"])


@router.get("/latest", response_model=NasaEpicImageRead)
def get_latest_epic(db: Session = Depends(get_db)):
    image = NasaEpicService(db).get_latest()

    if not image:
        raise HTTPException(status_code=404, detail="No EPIC image found.")

    return image