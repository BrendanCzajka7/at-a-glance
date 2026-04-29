from app.external.nasa_client import NasaClient
from app.services.nasa_apod_service import NasaApodService


class NasaApodIngestPipeline:
    def __init__(self, db):
        self.client = NasaClient()
        self.service = NasaApodService(db)

    async def run(self):
        raw = await self.client.fetch_apod()
        return self.service.save_from_raw(raw)