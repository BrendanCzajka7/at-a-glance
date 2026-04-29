from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoaaTidePredictionCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station_id: str
    prediction_time: datetime
    tide_type: str | None = None
    height_ft: float | None = None


class NoaaWeatherAlertCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event: str
    headline: str | None = None

    severity: str | None = None
    urgency: str | None = None
    certainty: str | None = None

    effective: datetime | None = None
    expires: datetime | None = None

    description: str | None = None
    instruction: str | None = None
    source_url: str | None = None


class NoaaSpaceWeatherDayCard(BaseModel):
    label: str
    date: str | None = None

    radio_blackout_minor_prob: int | None = None
    radio_blackout_major_prob: int | None = None

    solar_radiation_storm_prob: int | None = None

    geomagnetic_scale: str | None = None
    geomagnetic_text: str | None = None


class NoaaSpaceWeatherCard(BaseModel):
    fetched_at: datetime | None = None

    current_radio_blackout_scale: str | None = None
    current_radio_blackout_text: str | None = None

    current_solar_radiation_scale: str | None = None
    current_solar_radiation_text: str | None = None

    current_geomagnetic_scale: str | None = None
    current_geomagnetic_text: str | None = None

    forecast_days: list[NoaaSpaceWeatherDayCard]

    alert_count: int
    recent_alert_titles: list[str]


class NoaaSection(BaseModel):
    tides_today: list[NoaaTidePredictionCard]
    weather_alerts: list[NoaaWeatherAlertCard]
    space_weather: NoaaSpaceWeatherCard | None = None