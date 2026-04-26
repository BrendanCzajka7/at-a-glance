from sqlalchemy.orm import Session

from app.external.open_meteo_client import OpenMeteoClient
from app.models.weather_snapshot import WeatherSnapshot
from app.services.weather_service import WeatherService


class WeatherIngestPipeline:
    def __init__(self, db: Session):
        self.client = OpenMeteoClient()
        self.service = WeatherService(db)

    async def run_for_okaloosa_island(self) -> WeatherSnapshot:
        latitude = 30.3914
        longitude = -86.5932
        location_name = "Okaloosa Island, FL"

        raw = await self.client.fetch_current_weather(
            latitude=latitude,
            longitude=longitude,
        )

        return self.service.save_current_weather(
            raw=raw,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
        )