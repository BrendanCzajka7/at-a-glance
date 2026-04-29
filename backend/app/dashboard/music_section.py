# backend/app/dashboard/music_section.py

from datetime import datetime, timedelta

from app.schemas.music_dashboard import MusicReleaseCard, MusicSection
from app.services.music_release_service import MusicReleaseService


class MusicDashboardSection:
    def __init__(self, db):
        self.release_service = MusicReleaseService(db)

    def build(self, start: datetime) -> MusicSection:
        today = start.date()
        week_end = today + timedelta(days=7)
        month_end = today + timedelta(days=31)

        month_releases = self.release_service.list_between(
            start=today,
            end=month_end,
        )

        today_releases = [
            release for release in month_releases
            if release.release_date == today
        ]

        week_releases = [
            release for release in month_releases
            if today <= release.release_date <= week_end
        ]

        return MusicSection(
            today=[
                MusicReleaseCard.model_validate(release)
                for release in today_releases
            ],
            week=[
                MusicReleaseCard.model_validate(release)
                for release in week_releases
            ],
            month=[
                MusicReleaseCard.model_validate(release)
                for release in month_releases
            ],
        )