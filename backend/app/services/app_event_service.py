# backend/app/services/app_event_service.py

import traceback

from app.models.app_event import AppEvent
from app.repositories.app_event_repository import AppEventRepository


class AppEventService:
    def __init__(self, db):
        self.repo = AppEventRepository(db)

    def info(
        self,
        source: str,
        event_type: str,
        message: str,
        details: str | None = None,
    ):
        return self.repo.create(
            AppEvent(
                level="info",
                source=source,
                event_type=event_type,
                message=message,
                details=details,
            )
        )

    def error(
        self,
        source: str,
        event_type: str,
        message: str,
        exc: Exception | None = None,
    ):
        return self.repo.create(
            AppEvent(
                level="error",
                source=source,
                event_type=event_type,
                message=message,
                details=traceback.format_exc() if exc else None,
            )
        )

    def list_recent(self, limit: int = 50):
        return self.repo.list_recent(limit=limit)