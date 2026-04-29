# backend/app/core/pipeline_logging.py

from typing import Awaitable, TypeVar

from sqlalchemy.orm import Session

from app.services.app_event_service import AppEventService

T = TypeVar("T")


async def run_logged_pipeline(
    db: Session,
    source: str,
    event_type: str,
    message: str,
    action: Awaitable[T],
) -> T:
    try:
        return await action

    except Exception as exc:
        db.rollback()

        AppEventService(db).error(
            source=source,
            event_type=event_type,
            message=message,
            exc=exc,
        )

        raise