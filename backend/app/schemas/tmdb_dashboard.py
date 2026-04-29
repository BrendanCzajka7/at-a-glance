from datetime import date

from pydantic import BaseModel, ConfigDict


class TmdbMovieReleaseCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tmdb_movie_id: int
    title: str
    overview: str | None = None
    poster_path: str | None = None

    release_date: date

    matched_kind: str
    matched_name: str

    source_url: str | None = None


class TmdbSection(BaseModel):
    today: list[TmdbMovieReleaseCard]
    week: list[TmdbMovieReleaseCard]
    month: list[TmdbMovieReleaseCard]