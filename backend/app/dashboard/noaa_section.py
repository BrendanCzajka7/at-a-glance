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
                current_radio_blackout_scale=self.space_weather_service.current_scale_value(
                    latest_space_weather,
                    "R",
                    "Scale",
                ),
                current_radio_blackout_text=self.space_weather_service.current_scale_value(
                    latest_space_weather,
                    "R",
                    "Text",
                ),
                current_solar_radiation_scale=self.space_weather_service.current_scale_value(
                    latest_space_weather,
                    "S",
                    "Scale",
                ),
                current_solar_radiation_text=self.space_weather_service.current_scale_value(
                    latest_space_weather,
                    "S",
                    "Text",
                ),
                current_geomagnetic_scale=self.space_weather_service.current_scale_value(
                    latest_space_weather,
                    "G",
                    "Scale",
                ),
                current_geomagnetic_text=self.space_weather_service.current_scale_value(
                    latest_space_weather,
                    "G",
                    "Text",
                ),
                forecast_days=self.space_weather_service.forecast_days(
                    latest_space_weather
                ),
                alert_count=self.space_weather_service.alert_count(latest_space_weather),
                recent_alert_titles=self.space_weather_service.recent_alert_titles(
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