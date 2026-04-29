from datetime import date, datetime

from pydantic import BaseModel


class NasaNeoCloseApproachRead(BaseModel):
    id: int
    neo_reference_id: str
    name: str
    nasa_jpl_url: str | None = None

    close_approach_date: date
    close_approach_time: str | None = None

    estimated_diameter_min_m: float | None = None
    estimated_diameter_max_m: float | None = None

    miss_distance_km: float | None = None
    miss_distance_lunar: float | None = None
    relative_velocity_kph: float | None = None

    is_potentially_hazardous: bool

    fetched_at: datetime

    model_config = {"from_attributes": True}