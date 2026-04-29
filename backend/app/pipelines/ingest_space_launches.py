from datetime import datetime, time, timedelta

from app.external.launch_library_client import LaunchLibraryClient
from app.services.space_launch_service import SpaceLaunchService


class SpaceLaunchIngestPipeline:
    def __init__(self, db):
        self.client = LaunchLibraryClient()
        self.launch_service = SpaceLaunchService(db)

    async def run(self):
        today_start = datetime.combine(datetime.utcnow().date(), time.min)
        month_end = today_start + timedelta(days=31)

        raw_launches = await self.client.fetch_upcoming_launches(
            start=today_start,
            end=month_end,
        )

        return self.launch_service.save_from_raw_launches(raw_launches)