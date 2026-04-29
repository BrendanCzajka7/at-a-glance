from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OceanConditionsCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station_id: str
    observed_at: datetime

    water_temperature_f: float | None = None
    wave_height_ft: float | None = None


class OceanSection(BaseModel):
    current: OceanConditionsCard | None = None