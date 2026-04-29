from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoaaTidePredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    location_key: str
    station_id: str
    prediction_time: datetime
    tide_type: str | None = None
    height_ft: float | None = None
    fetched_at: datetime


class NoaaWeatherAlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    location_key: str
    nws_alert_id: str

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

    fetched_at: datetime


class NoaaSpaceWeatherReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scales_json: str | None = None
    alerts_json: str | None = None
    three_day_forecast_text: str | None = None
    fetched_at: datetime