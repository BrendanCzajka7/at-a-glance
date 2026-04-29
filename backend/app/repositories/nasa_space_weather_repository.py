from datetime import datetime

from sqlalchemy.orm import Session

from app.models.nasa_space_weather_notification import (
    NasaSpaceWeatherNotification,
)


class NasaSpaceWeatherRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_many(
        self,
        notifications: list[NasaSpaceWeatherNotification],
    ) -> list[NasaSpaceWeatherNotification]:
        saved: list[NasaSpaceWeatherNotification] = []

        for notification in notifications:
            existing = (
                self.db.query(NasaSpaceWeatherNotification)
                .filter(
                    NasaSpaceWeatherNotification.message_id
                    == notification.message_id
                )
                .first()
            )

            if existing:
                existing.message_type = notification.message_type
                existing.message_issue_time = notification.message_issue_time
                existing.message_url = notification.message_url
                existing.title = notification.title
                existing.summary = notification.summary
                existing.raw_message_body = notification.raw_message_body
                existing.fetched_at = datetime.utcnow()

                saved.append(existing)
            else:
                self.db.add(notification)
                saved.append(notification)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_between(
        self,
        start: datetime,
        end: datetime,
        limit: int = 20,
    ) -> list[NasaSpaceWeatherNotification]:
        return (
            self.db.query(NasaSpaceWeatherNotification)
            .filter(
                NasaSpaceWeatherNotification.message_issue_time >= start,
                NasaSpaceWeatherNotification.message_issue_time < end,
            )
            .order_by(NasaSpaceWeatherNotification.message_issue_time.desc())
            .limit(limit)
            .all()
        )