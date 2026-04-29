from datetime import date, datetime

from app.models.tmdb_movie_release import TmdbMovieRelease


class TmdbMovieReleaseRepository:
    def __init__(self, db):
        self.db = db

    def upsert_many(
        self,
        releases: list[TmdbMovieRelease],
    ) -> list[TmdbMovieRelease]:
        saved: list[TmdbMovieRelease] = []

        for release in releases:
            existing = (
                self.db.query(TmdbMovieRelease)
                .filter(
                    TmdbMovieRelease.tmdb_movie_id == release.tmdb_movie_id,
                    TmdbMovieRelease.matched_kind == release.matched_kind,
                    TmdbMovieRelease.matched_tmdb_id == release.matched_tmdb_id,
                )
                .first()
            )

            if existing:
                existing.title = release.title
                existing.overview = release.overview
                existing.poster_path = release.poster_path
                existing.release_date = release.release_date
                existing.vote_average = release.vote_average
                existing.popularity = release.popularity
                existing.matched_name = release.matched_name
                existing.source_url = release.source_url
                existing.fetched_at = datetime.utcnow()
                saved.append(existing)
            else:
                self.db.add(release)
                saved.append(release)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_between(
        self,
        start: date,
        end: date,
    ) -> list[TmdbMovieRelease]:
        return (
            self.db.query(TmdbMovieRelease)
            .filter(
                TmdbMovieRelease.release_date >= start,
                TmdbMovieRelease.release_date <= end,
            )
            .order_by(
                TmdbMovieRelease.release_date.asc(),
                TmdbMovieRelease.title.asc(),
                TmdbMovieRelease.matched_kind.asc(),
            )
            .all()
        )