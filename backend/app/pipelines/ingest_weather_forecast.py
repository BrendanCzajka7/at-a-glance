from sqlalchemy.orm import Session

from app.core.locations import get_location
from app.external.open_meteo_client import OpenMeteoClient
from app.models.weather_forecast import WeatherForecast
from app.services.weather_forecast_service import WeatherForecastService


class WeatherForecastIngestPipeline:
    def __init__(self, db: Session):
        self.client = OpenMeteoClient()
        self.service = WeatherForecastService(db)

    async def run_for_location(self, location_key: str) -> list[WeatherForecast]:
        location = get_location(location_key)

        raw = await self.client.fetch_forecast(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=location.timezone,
        )

        return self.service.save_forecast_response(
            raw=raw,
            location_key=location.key,
            location_name=location.name,
        )