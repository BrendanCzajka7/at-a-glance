from datetime import datetime

from sqlalchemy.orm import Session

from app.schemas.weather_dashboard import (
    WeatherCurrent,
    WeatherDaily,
    WeatherHourly,
    WeatherSection,
)
from app.services.weather_forecast_service import WeatherForecastService


class WeatherDashboardSection:
    def __init__(self, db: Session):
        self.weather_service = WeatherForecastService(db)

    def build(
        self,
        start: datetime,
        end: datetime,
        location_key: str,
    ) -> WeatherSection:
        forecasts = self.weather_service.list_forecasts_between(
            start=start,
            end=end,
            location_key=location_key,
        )

        current: WeatherCurrent | None = None
        hourly: list[WeatherHourly] = []
        daily: list[WeatherDaily] = []

        for forecast in forecasts:
            if forecast.granularity == "current":
                current = WeatherCurrent.model_validate(forecast)

            elif forecast.granularity == "hourly":
                hourly.append(WeatherHourly.model_validate(forecast))

            elif forecast.granularity == "daily":
                daily.append(WeatherDaily.model_validate(forecast))

        return WeatherSection(
            current=current,
            hourly=hourly,
            daily=daily,
        )