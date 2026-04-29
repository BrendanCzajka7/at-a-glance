from datetime import datetime

from app.models.noaa_weather_alert import NoaaWeatherAlert
from app.repositories.noaa_weather_alert_repository import (
    NoaaWeatherAlertRepository,
)


class NoaaWeatherAlertService:
    def __init__(self, db):
        self.repo = NoaaWeatherAlertRepository(db)

    def save_from_raw_alerts(
        self,
        location_key: str,
        raw_alerts: list[dict],
    ) -> list[NoaaWeatherAlert]:
        rows: list[NoaaWeatherAlert] = []
        seen_ids: set[str] = set()

        for feature in raw_alerts:
            properties = feature.get("properties") or {}
            alert_id = properties.get("id") or feature.get("id")

            event = properties.get("event")

            if not alert_id or not event:
                continue

            if alert_id in seen_ids:
                continue

            seen_ids.add(alert_id)

            rows.append(
                NoaaWeatherAlert(
                    location_key=location_key,
                    nws_alert_id=alert_id,
                    event=event,
                    headline=properties.get("headline"),
                    severity=properties.get("severity"),
                    urgency=properties.get("urgency"),
                    certainty=properties.get("certainty"),
                    effective=_parse_datetime(properties.get("effective")),
                    expires=_parse_datetime(properties.get("expires")),
                    description=properties.get("description"),
                    instruction=properties.get("instruction"),
                    source_url=properties.get("@id") or properties.get("id"),
                )
            )

        return self.repo.upsert_many(rows)

    def list_active_for_location(
        self,
        location_key: str,
        now: datetime,
    ) -> list[NoaaWeatherAlert]:
        return self.repo.list_active_for_location(
            location_key=location_key,
            now=now,
        )


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(
            tzinfo=None
        )
    except ValueError:
        return None