# backend/app/repositories/app_event_repository.py

from app.models.app_event import AppEvent


class AppEventRepository:
    def __init__(self, db):
        self.db = db

    def create(self, event: AppEvent) -> AppEvent:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def list_recent(self, limit: int = 50) -> list[AppEvent]:
        return (
            self.db.query(AppEvent)
            .order_by(AppEvent.created_at.desc())
            .limit(limit)
            .all()
        )