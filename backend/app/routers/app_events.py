# backend/app/routers/app_events.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.app_event import AppEventRead
from app.services.app_event_service import AppEventService

router = APIRouter(prefix="/api/app-events", tags=["app-events"])


@router.get("", response_model=list[AppEventRead])
def list_app_events(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return AppEventService(db).list_recent(limit=limit)