from datetime import datetime

from app.models.noaa_weather_alert import NoaaWeatherAlert


class NoaaWeatherAlertRepository:
    def __init__(self, db):
        self.db = db

    def upsert_many(
        self,
        rows: list[NoaaWeatherAlert],
    ) -> list[NoaaWeatherAlert]:
        saved: list[NoaaWeatherAlert] = []

        for row in rows:
            existing = (
                self.db.query(NoaaWeatherAlert)
                .filter(
                    NoaaWeatherAlert.location_key == row.location_key,
                    NoaaWeatherAlert.nws_alert_id == row.nws_alert_id,
                )
                .first()
            )

            if existing:
                existing.event = row.event
                existing.headline = row.headline
                existing.severity = row.severity
                existing.urgency = row.urgency
                existing.certainty = row.certainty
                existing.effective = row.effective
                existing.expires = row.expires
                existing.description = row.description
                existing.instruction = row.instruction
                existing.source_url = row.source_url
                existing.fetched_at = datetime.utcnow()
                saved.append(existing)
            else:
                self.db.add(row)
                saved.append(row)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_active_for_location(
        self,
        location_key: str,
        now: datetime,
    ) -> list[NoaaWeatherAlert]:
        return (
            self.db.query(NoaaWeatherAlert)
            .filter(
                NoaaWeatherAlert.location_key == location_key,
                NoaaWeatherAlert.expires >= now,
            )
            .order_by(
                NoaaWeatherAlert.severity.asc(),
                NoaaWeatherAlert.effective.desc(),
            )
            .all()
        )