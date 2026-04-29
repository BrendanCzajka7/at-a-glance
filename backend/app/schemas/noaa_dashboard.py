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


class NoaaSpaceWeatherCard(BaseModel):
    fetched_at: datetime | None = None
    current_scales_summary: str | None = None
    forecast_summary: str | None = None
    alert_titles: list[str]


class NoaaSection(BaseModel):
    tides_today: list[NoaaTidePredictionCard]
    weather_alerts: list[NoaaWeatherAlertCard]
    space_weather: NoaaSpaceWeatherCard | None = None