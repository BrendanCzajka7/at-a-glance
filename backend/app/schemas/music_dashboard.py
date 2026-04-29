# backend/app/schemas/music_dashboard.py

from datetime import date

from pydantic import BaseModel, ConfigDict


class MusicReleaseCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    artist_name: str
    title: str
    release_date: date
    release_type: str | None = None
    source_url: str | None = None


class MusicSection(BaseModel):
    today: list[MusicReleaseCard]
    week: list[MusicReleaseCard]
    month: list[MusicReleaseCard]