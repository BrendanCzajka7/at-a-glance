from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsgsEarthquakeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usgs_event_id: str

    title: str
    place: str | None = None

    magnitude: float | None = None
    event_time: datetime
    updated_at: datetime | None = None

    longitude: float | None = None
    latitude: float | None = None
    depth_km: float | None = None

    tsunami: int | None = None
    significance: int | None = None
    alert: str | None = None
    status: str | None = None

    event_type: str | None = None
    magnitude_type: str | None = None

    source_url: str | None = None
    detail_url: str | None = None

    fetched_at: datetime