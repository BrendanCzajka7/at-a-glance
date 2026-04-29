from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OceanConditionsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    location_key: str
    station_id: str

    observed_at: datetime

    water_temperature_f: float | None = None
    wave_height_ft: float | None = None

    fetched_at: datetime