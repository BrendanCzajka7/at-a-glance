# backend/app/schemas/music.py

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class MusicArtistRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    musicbrainz_artist_id: str
    is_active: bool


class MusicReleaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    musicbrainz_release_id: str
    musicbrainz_artist_id: str

    artist_name: str
    title: str
    release_date: date

    status: str | None = None
    release_type: str | None = None
    country: str | None = None
    source_url: str | None = None

    fetched_at: datetime