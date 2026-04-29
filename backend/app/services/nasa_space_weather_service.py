import re
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.nasa_space_weather_notification import (
    NasaSpaceWeatherNotification,
)
from app.repositories.nasa_space_weather_repository import (
    NasaSpaceWeatherRepository,
)


def clean_summary(message_body: str) -> str:
    match = re.search(
        r"## Summary:\s*(.*?)(?:## Notes:|##Events:|$)",
        message_body,
        re.DOTALL,
    )

    if match:
        summary = match.group(1)
    else:
        summary = message_body

    summary = re.sub(r"https?://\S+", "", summary)
    summary = re.sub(r"\n+", " ", summary)
    summary = re.sub(r"\s+", " ", summary)

    return summary.strip()


def clean_title(message_body: str, fallback_type: str | None) -> str:
    match = re.search(r"## Message Type:\s*(.*)", message_body)

    if not match:
        return fallback_type or "Space Weather"

    title = match.group(1).strip()
    title = title.replace("Space Weather Notification - ", "")
    title = title.replace("Auto-generated Space Weather Notification - ", "")

    return title


class NasaSpaceWeatherService:
    def __init__(self, db: Session):
        self.repo = NasaSpaceWeatherRepository(db)

    def save_notifications_from_raw(
        self,
        raw_items: list[dict],
    ) -> list[NasaSpaceWeatherNotification]:
        notifications: list[NasaSpaceWeatherNotification] = []

        for raw in raw_items:
            message_id = raw.get("messageID") or raw.get("messageId")
            issue_time = raw.get("messageIssueTime")
            message_body = raw.get("messageBody")

            if not message_id or not issue_time or not message_body:
                continue

            message_type = raw.get("messageType")

            notifications.append(
                NasaSpaceWeatherNotification(
                    message_id=message_id,
                    message_type=message_type,
                    message_issue_time=datetime.fromisoformat(
                        issue_time.replace("Z", "+00:00")
                    ).replace(tzinfo=None),
                    message_url=raw.get("messageURL"),
                    title=clean_title(message_body, message_type),
                    summary=clean_summary(message_body),
                    raw_message_body=message_body,
                )
            )

        return self.repo.upsert_many(notifications)

    def list_between(
        self,
        start: datetime,
        end: datetime,
        limit: int = 20,
    ) -> list[NasaSpaceWeatherNotification]:
        return self.repo.list_between(
            start=start,
            end=end,
            limit=limit,
        )