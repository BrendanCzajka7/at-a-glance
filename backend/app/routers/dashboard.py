from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.time import now_for_timezone
from app.schemas.dashboard import DashboardRead
from app.services.dashboard_service import DashboardService
from app.services.location_service import LocationService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardRead)
def get_dashboard(
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    location_key: str = Query(default="okaloosa_island"),
    db: Session = Depends(get_db),
):
    location = LocationService(db).get_required(location_key)

    if start is None:
        start = now_for_timezone(location.timezone)

    if end is None:
        end = start + timedelta(days=7)

    service = DashboardService(db)

    return service.get_dashboard(
        start=start,
        end=end,
        location_key=location.key,
    )