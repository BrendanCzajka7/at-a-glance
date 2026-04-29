from app.external.nasa_client import NasaClient
from app.services.nasa_epic_service import NasaEpicService


class NasaEpicIngestPipeline:
    def __init__(self, db):
        self.client = NasaClient()
        self.service = NasaEpicService(db)

    async def run(self):
        raw = await self.client.fetch_epic_latest_natural()
        return self.service.save_latest_from_raw(raw)