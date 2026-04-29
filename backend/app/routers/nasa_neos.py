from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.nasa_neo import NasaNeoCloseApproachRead
from app.services.nasa_neo_service import NasaNeoService

router = APIRouter(prefix="/api/nasa/neos", tags=["nasa"])


@router.get("", response_model=list[NasaNeoCloseApproachRead])
def get_neos(
    days: int = Query(default=7, ge=1, le=31),
    notable_only: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    start = datetime.utcnow().date()
    end = start + timedelta(days=days)

    service = NasaNeoService(db)

    if notable_only:
        return service.list_notable_between(start=start, end=end)

    return service.list_between(start=start, end=end)