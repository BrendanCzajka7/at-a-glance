from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsgsEarthquakeCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    place: str | None = None

    magnitude: float | None = None
    event_time: datetime

    longitude: float | None = None
    latitude: float | None = None
    depth_km: float | None = None

    tsunami: int | None = None
    significance: int | None = None
    alert: str | None = None
    status: str | None = None

    source_url: str | None = None


class UsgsSection(BaseModel):
    largest_today: UsgsEarthquakeCard | None = None
    most_significant_today: UsgsEarthquakeCard | None = None
    tsunami_events_today: list[UsgsEarthquakeCard]
    alert_events_today: list[UsgsEarthquakeCard]