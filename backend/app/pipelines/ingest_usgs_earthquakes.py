from app.external.usgs_client import UsgsClient
from app.services.usgs_earthquake_service import UsgsEarthquakeService


class UsgsEarthquakeIngestPipeline:
    def __init__(self, db):
        self.client = UsgsClient()
        self.earthquake_service = UsgsEarthquakeService(db)

    async def run(self):
        raw_features = await self.client.fetch_significant_recent_earthquakes()
        return self.earthquake_service.save_from_raw_features(raw_features)