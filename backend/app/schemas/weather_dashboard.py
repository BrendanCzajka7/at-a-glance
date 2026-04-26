from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WeatherCurrent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    location_name: str
    forecast_for: datetime
    temperature_f: float | None = None
    apparent_temperature_f: float | None = None
    precipitation_inches: float | None = None
    wind_speed_mph: float | None = None
    wind_gust_mph: float | None = None
    weather_code: int | None = None
    wind_direction_degrees: int | None = None
    cloud_cover: int | None = None
    is_day: int | None = None


class WeatherHourly(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    forecast_for: datetime
    temperature_f: float | None = None
    apparent_temperature_f: float | None = None
    precipitation_probability: int | None = None
    precipitation_inches: float | None = None
    wind_speed_mph: float | None = None
    uv_index: float | None = None
    weather_code: int | None = None
    wind_gust_mph: float | None = None
    wind_direction_degrees: int | None = None
    cloud_cover: int | None = None
    is_day: int | None = None


class WeatherDaily(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    forecast_for: datetime
    temperature_max_f: float | None = None
    temperature_min_f: float | None = None
    precipitation_probability: int | None = None
    precipitation_inches: float | None = None
    uv_index: float | None = None
    sunrise: datetime | None = None
    sunset: datetime | None = None
    weather_code: int | None = None


class WeatherSection(BaseModel):
    current: WeatherCurrent | None = None
    hourly: list[WeatherHourly]
    daily: list[WeatherDaily]