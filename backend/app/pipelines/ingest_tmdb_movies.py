from datetime import date, timedelta

from app.external.tmdb_client import TmdbClient
from app.services.tmdb_movie_release_service import TmdbMovieReleaseService
from app.services.tmdb_watch_item_service import TmdbWatchItemService


class TmdbMovieIngestPipeline:
    def __init__(self, db):
        self.client = TmdbClient()
        self.watch_item_service = TmdbWatchItemService(db)
        self.movie_release_service = TmdbMovieReleaseService(db)

    async def run_for_all_watch_items(self):
        start = date.today()
        end = start + timedelta(days=31)

        saved = []

        for item in self.watch_item_service.list_active():
            if item.kind == "genre":
                raw_movies = await self.client.discover_movies_for_genre(
                    genre_id=item.tmdb_id,
                    start_date=start.isoformat(),
                    end_date=end.isoformat(),
                )
            elif item.kind == "director":
                raw_movies = await self.client.discover_movies_for_director(
                    director_id=item.tmdb_id,
                    start_date=start.isoformat(),
                    end_date=end.isoformat(),
                )
            else:
                continue

            saved.extend(
                self.movie_release_service.save_from_raw_movies(
                    matched_kind=item.kind,
                    matched_tmdb_id=item.tmdb_id,
                    matched_name=item.name,
                    raw_movies=raw_movies,
                )
            )

        return saved

    async def run_for_watch_item(
        self,
        kind: str,
        tmdb_id: int,
        name: str,
    ):
        start = date.today()
        end = start + timedelta(days=31)

        if kind == "genre":
            raw_movies = await self.client.discover_movies_for_genre(
                genre_id=tmdb_id,
                start_date=start.isoformat(),
                end_date=end.isoformat(),
            )
        elif kind == "director":
            raw_movies = await self.client.discover_movies_for_director(
                director_id=tmdb_id,
                start_date=start.isoformat(),
                end_date=end.isoformat(),
            )
        else:
            raise ValueError(f"Unsupported TMDB watch kind: {kind}")

        return self.movie_release_service.save_from_raw_movies(
            matched_kind=kind,
            matched_tmdb_id=tmdb_id,
            matched_name=name,
            raw_movies=raw_movies,
        )