from datetime import datetime, timedelta

from app.schemas.tmdb_dashboard import TmdbMovieReleaseCard, TmdbSection
from app.services.tmdb_movie_release_service import TmdbMovieReleaseService


class TmdbDashboardSection:
    def __init__(self, db):
        self.release_service = TmdbMovieReleaseService(db)

    def build(self, start: datetime) -> TmdbSection:
        today = start.date()
        week_end = today + timedelta(days=7)
        month_end = today + timedelta(days=31)

        month_releases = self.release_service.list_between(
            start=today,
            end=month_end,
        )


        by_movie_id = {}
        for release in month_releases:
            if release.tmdb_movie_id not in by_movie_id:
                by_movie_id[release.tmdb_movie_id] = release

        deduped_month_releases = list(by_movie_id.values())

        today_releases = [
            release
            for release in deduped_month_releases
            if release.release_date == today
        ]

        week_releases = [
            release
            for release in deduped_month_releases
            if today <= release.release_date <= week_end
        ]

        return TmdbSection(
            today=[
                TmdbMovieReleaseCard.model_validate(release)
                for release in today_releases
            ],
            week=[
                TmdbMovieReleaseCard.model_validate(release)
                for release in week_releases
            ],
            month=[
                TmdbMovieReleaseCard.model_validate(release)
                for release in deduped_month_releases
            ],
        )