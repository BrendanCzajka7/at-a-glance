# backend/app/models/music_artist.py

from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from app.core.db import Base


class MusicArtist(Base):
    __tablename__ = "music_artists"

    __table_args__ = (
        UniqueConstraint("musicbrainz_artist_id", name="uq_music_artist_mbid"),
    )

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    musicbrainz_artist_id = Column(String, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)