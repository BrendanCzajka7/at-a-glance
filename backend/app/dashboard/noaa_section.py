from datetime import datetime, time, timedelta

from app.schemas.noaa_dashboard import (
    NoaaSection,
    NoaaSpaceWeatherCard,
    NoaaTidePredictionCard,
    NoaaWeatherAlertCard,
)
from app.services.noaa_space_weather_service import NoaaSpaceWeatherService
from app.services.noaa_tide_service import NoaaTideService
from app.services.noaa_weather_alert_service import NoaaWeatherAlertService


class NoaaDashboardSection:
    def __init__(self, db):
        self.tide_service = NoaaTideService(db)
        self.alert_service = NoaaWeatherAlertService(db)
        self.space_weather_service = NoaaSpaceWeatherService(db)

    def build(
        self,
        now: datetime,
        location_key: str,
    ) -> NoaaSection:
        today_start = datetime.combine(now.date(), time.min)
        tomorrow_start = today_start + timedelta(days=1)

        tides_today = self.tide_service.list_between(
            location_key=location_key,
            start=today_start,
            end=tomorrow_start,
        )

        weather_alerts = self.alert_service.list_active_for_location(
            location_key=location_key,
            now=now,
        )

        latest_space_weather = self.space_weather_service.get_latest()

        if latest_space_weather:
            space_weather = NoaaSpaceWeatherCard(
                fetched_at=latest_space_weather.fetched_at,
                current_scales_summary=self.space_weather_service.summarize_scales(
                    latest_space_weather
                ),
                forecast_summary=self.space_weather_service.summarize_forecast_text(
                    latest_space_weather
                ),
                alert_titles=self.space_weather_service.summarize_alert_titles(
                    latest_space_weather
                ),
            )
        else:
            space_weather = None

        return NoaaSection(
            tides_today=[
                NoaaTidePredictionCard.model_validate(item)
                for item in tides_today
            ],
            weather_alerts=[
                NoaaWeatherAlertCard.model_validate(item)
                for item in weather_alerts
            ],
            space_weather=space_weather,
        )