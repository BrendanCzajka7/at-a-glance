from datetime import datetime

from pydantic import BaseModel


class WeatherSnapshotRead(BaseModel):
    id: int
    location_name: str
    latitude: float
    longitude: float
    temperature_f: float
    wind_speed_mph: float | None
    weather_code: int | None
    observed_at: datetime
    ingested_at: datetime

    model_config = {"from_attributes": True}