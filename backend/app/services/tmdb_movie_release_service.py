from datetime import date

from app.models.tmdb_movie_release import TmdbMovieRelease
from app.repositories.tmdb_movie_release_repository import TmdbMovieReleaseRepository


class TmdbMovieReleaseService:
    def __init__(self, db):
        self.repo = TmdbMovieReleaseRepository(db)

    def save_from_raw_movies(
        self,
        matched_kind: str,
        matched_tmdb_id: int,
        matched_name: str,
        raw_movies: list[dict],
    ) -> list[TmdbMovieRelease]:
        rows: list[TmdbMovieRelease] = []
        seen_movie_ids: set[int] = set()

        for raw in raw_movies:
            tmdb_movie_id = raw.get("id")
            title = raw.get("title") or raw.get("name")
            release_date_raw = raw.get("release_date")

            if not tmdb_movie_id or not title or not release_date_raw:
                continue

            try:
                release_date = date.fromisoformat(release_date_raw)
            except ValueError:
                continue

            if tmdb_movie_id in seen_movie_ids:
                continue

            seen_movie_ids.add(tmdb_movie_id)

            rows.append(
                TmdbMovieRelease(
                    tmdb_movie_id=tmdb_movie_id,
                    title=title,
                    overview=raw.get("overview"),
                    poster_path=raw.get("poster_path"),
                    release_date=release_date,
                    vote_average=raw.get("vote_average"),
                    popularity=raw.get("popularity"),
                    matched_kind=matched_kind,
                    matched_tmdb_id=matched_tmdb_id,
                    matched_name=matched_name,
                    source_url=f"https://www.themoviedb.org/movie/{tmdb_movie_id}",
                )
            )

        return self.repo.upsert_many(rows)

    def list_between(
        self,
        start: date,
        end: date,
    ) -> list[TmdbMovieRelease]:
        return self.repo.list_between(start=start, end=end)