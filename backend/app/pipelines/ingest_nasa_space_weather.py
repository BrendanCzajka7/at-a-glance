from datetime import datetime, timedelta

from app.external.nasa_client import NasaClient
from app.services.nasa_space_weather_service import NasaSpaceWeatherService


class NasaSpaceWeatherIngestPipeline:
    def __init__(self, db):
        self.client = NasaClient()
        self.service = NasaSpaceWeatherService(db)

    async def run(self):
        start_date = datetime.utcnow().date()
        end_date = start_date + timedelta(days=7)

        raw_items = await self.client.fetch_space_weather_notifications(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )

        return self.service.save_notifications_from_raw(raw_items)