from datetime import datetime

from app.models.usgs_earthquake import UsgsEarthquake
from app.repositories.usgs_earthquake_repository import UsgsEarthquakeRepository


class UsgsEarthquakeService:
    def __init__(self, db):
        self.repo = UsgsEarthquakeRepository(db)

    def save_from_raw_features(
        self,
        raw_features: list[dict],
    ) -> list[UsgsEarthquake]:
        rows: list[UsgsEarthquake] = []
        seen_ids: set[str] = set()

        for feature in raw_features:
            event_id = feature.get("id")
            properties = feature.get("properties") or {}
            geometry = feature.get("geometry") or {}
            coordinates = geometry.get("coordinates") or []

            title = properties.get("title")
            event_time_raw = properties.get("time")

            if not event_id or not title or event_time_raw is None:
                continue

            if event_id in seen_ids:
                continue

            seen_ids.add(event_id)

            event_time = _millis_to_datetime(event_time_raw)
            updated_at = _millis_to_datetime(properties.get("updated"))

            longitude = _coordinate_at(coordinates, 0)
            latitude = _coordinate_at(coordinates, 1)
            depth_km = _coordinate_at(coordinates, 2)

            rows.append(
                UsgsEarthquake(
                    usgs_event_id=event_id,
                    title=title,
                    place=properties.get("place"),
                    magnitude=properties.get("mag"),
                    event_time=event_time,
                    updated_at=updated_at,
                    longitude=longitude,
                    latitude=latitude,
                    depth_km=depth_km,
                    tsunami=properties.get("tsunami"),
                    significance=properties.get("sig"),
                    alert=properties.get("alert"),
                    status=properties.get("status"),
                    event_type=properties.get("type"),
                    magnitude_type=properties.get("magType"),
                    source_url=properties.get("url"),
                    detail_url=properties.get("detail"),
                )
            )

        return self.repo.upsert_many(rows)

    def list_since(self, since: datetime) -> list[UsgsEarthquake]:
        return self.repo.list_since(since=since)


def _millis_to_datetime(value) -> datetime | None:
    if value is None:
        return None

    return datetime.utcfromtimestamp(value / 1000)


def _coordinate_at(coordinates: list, index: int) -> float | None:
    try:
        value = coordinates[index]
    except IndexError:
        return None

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None