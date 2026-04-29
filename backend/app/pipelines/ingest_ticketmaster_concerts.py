from datetime import datetime, time, timedelta

from app.external.ticketmaster_client import TicketmasterClient
from app.services.location_service import LocationService
from app.services.ticketmaster_concert_service import TicketmasterConcertService


class TicketmasterConcertIngestPipeline:
    def __init__(self, db):
        self.client = TicketmasterClient()
        self.location_service = LocationService(db)
        self.concert_service = TicketmasterConcertService(db)

    async def run_for_location(
        self,
        location_key: str,
        radius_miles: int = 75,
    ):
        location = self.location_service.get_required(location_key)

        today_start = datetime.combine(datetime.utcnow().date(), time.min)
        month_end = today_start + timedelta(days=31)

        raw_events = await self.client.search_music_events_near_location(
            latitude=location.latitude,
            longitude=location.longitude,
            start=today_start,
            end=month_end,
            radius_miles=radius_miles,
        )

        return self.concert_service.save_from_raw_events(
            location_key=location.key,
            origin_latitude=location.latitude,
            origin_longitude=location.longitude,
            radius_miles=radius_miles,
            raw_events=raw_events,
        )

    async def run_for_all_active_locations(
        self,
        radius_miles: int = 75,
    ) -> dict:
        locations = self.location_service.list_active()
        results = {}

        for location in locations:
            rows = await self.run_for_location(
                location_key=location.key,
                radius_miles=radius_miles,
            )

            results[location.key] = {
                "saved_rows": len(rows),
                "radius_miles": radius_miles,
            }

        return results