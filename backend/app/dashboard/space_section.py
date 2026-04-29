from datetime import datetime, time, timedelta

from app.schemas.space_dashboard import SpaceLaunchCard, SpaceSection
from app.services.space_launch_service import SpaceLaunchService


class SpaceDashboardSection:
    def __init__(self, db):
        self.launch_service = SpaceLaunchService(db)

    def build(self, start: datetime) -> SpaceSection:
        today_start = datetime.combine(start.date(), time.min)
        tomorrow_start = today_start + timedelta(days=1)
        week_end = today_start + timedelta(days=7)
        month_end = today_start + timedelta(days=31)

        month_launches = self.launch_service.list_between(
            start=today_start,
            end=month_end,
        )

        today_launches = [
            launch for launch in month_launches
            if today_start <= launch.net < tomorrow_start
        ]

        week_launches = [
            launch for launch in month_launches
            if today_start <= launch.net <= week_end
        ]

        return SpaceSection(
            today=[
                SpaceLaunchCard.model_validate(launch)
                for launch in today_launches
            ],
            week=[
                SpaceLaunchCard.model_validate(launch)
                for launch in week_launches
            ],
            month=[
                SpaceLaunchCard.model_validate(launch)
                for launch in month_launches
            ],
        )