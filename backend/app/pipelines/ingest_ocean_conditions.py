from app.external.ndbc_client import NdbcClient
from app.services.location_service import LocationService
from app.services.ocean_conditions_service import OceanConditionsService


class OceanConditionsIngestPipeline:
    def __init__(self, db):
        self.client = NdbcClient()
        self.location_service = LocationService(db)
        self.ocean_service = OceanConditionsService(db)

    async def run_for_location(self, location_key: str):
        location = self.location_service.get_required(location_key)

        if not location.ndbc_station_id:
            return None

        raw = await self.client.fetch_latest_conditions(location.ndbc_station_id)

        if not raw:
            return None

        return self.ocean_service.save_latest_from_raw(
            location_key=location.key,
            station_id=location.ndbc_station_id,
            raw=raw,
        )

    async def run_for_all_active_locations(self) -> dict:
        locations = self.location_service.list_active()
        results = {}

        for location in locations:
            row = await self.run_for_location(location.key)

            results[location.key] = {
                "station_id": location.ndbc_station_id,
                "saved": row is not None,
            }

        return results