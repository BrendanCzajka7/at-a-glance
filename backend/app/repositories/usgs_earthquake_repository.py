from datetime import datetime

from app.models.usgs_earthquake import UsgsEarthquake


class UsgsEarthquakeRepository:
    def __init__(self, db):
        self.db = db

    def upsert_many(
        self,
        earthquakes: list[UsgsEarthquake],
    ) -> list[UsgsEarthquake]:
        saved: list[UsgsEarthquake] = []

        for earthquake in earthquakes:
            existing = (
                self.db.query(UsgsEarthquake)
                .filter(UsgsEarthquake.usgs_event_id == earthquake.usgs_event_id)
                .first()
            )

            if existing:
                existing.title = earthquake.title
                existing.place = earthquake.place
                existing.magnitude = earthquake.magnitude
                existing.event_time = earthquake.event_time
                existing.updated_at = earthquake.updated_at
                existing.longitude = earthquake.longitude
                existing.latitude = earthquake.latitude
                existing.depth_km = earthquake.depth_km
                existing.tsunami = earthquake.tsunami
                existing.significance = earthquake.significance
                existing.alert = earthquake.alert
                existing.status = earthquake.status
                existing.event_type = earthquake.event_type
                existing.magnitude_type = earthquake.magnitude_type
                existing.source_url = earthquake.source_url
                existing.detail_url = earthquake.detail_url
                existing.fetched_at = datetime.utcnow()
                saved.append(existing)
            else:
                self.db.add(earthquake)
                saved.append(earthquake)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_since(self, since: datetime) -> list[UsgsEarthquake]:
        return (
            self.db.query(UsgsEarthquake)
            .filter(UsgsEarthquake.event_time >= since)
            .order_by(UsgsEarthquake.event_time.desc())
            .all()
        )