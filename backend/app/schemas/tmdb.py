from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TmdbWatchItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kind: str
    tmdb_id: int
    name: str
    is_active: bool


class TmdbMovieReleaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    tmdb_movie_id: int
    title: str
    overview: str | None = None
    poster_path: str | None = None

    release_date: date
    vote_average: float | None = None
    popularity: float | None = None

    matched_kind: str
    matched_tmdb_id: int
    matched_name: str

    source_url: str | None = None

    fetched_at: datetime


class TmdbGenreSearchResult(BaseModel):
    tmdb_id: int
    name: str


class TmdbDirectorSearchResult(BaseModel):
    tmdb_id: int
    name: str
    known_for_department: str | None = None
    profile_path: str | None = None
    popularity: float | None = None