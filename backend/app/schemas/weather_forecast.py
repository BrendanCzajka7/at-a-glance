from datetime import datetime

from pydantic import BaseModel


class WeatherForecastRead(BaseModel):
    id: int

    source: str
    location_key: str
    location_name: str

    granularity: str
    forecast_for: datetime

    temperature_f: float | None = None
    temperature_max_f: float | None = None
    temperature_min_f: float | None = None
    apparent_temperature_f: float | None = None

    precipitation_probability: int | None = None
    precipitation_inches: float | None = None

    wind_speed_mph: float | None = None
    wind_gust_mph: float | None = None

    uv_index: float | None = None
    weather_code: int | None = None

    sunrise: datetime | None = None
    sunset: datetime | None = None

    fetched_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}