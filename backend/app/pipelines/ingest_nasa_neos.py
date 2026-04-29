from datetime import datetime, timedelta

from app.external.nasa_client import NasaClient
from app.services.nasa_neo_service import NasaNeoService


class NasaNeoIngestPipeline:
    def __init__(self, db):
        self.client = NasaClient()
        self.service = NasaNeoService(db)

    async def run(self):
        start = datetime.utcnow().date()
        end = start + timedelta(days=7)

        raw = await self.client.fetch_neows_feed(
            start_date=start.isoformat(),
            end_date=end.isoformat(),
        )

        return self.service.save_from_feed(raw)