# backend/app/models/music_release.py

from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class MusicRelease(Base):
    __tablename__ = "music_releases"

    __table_args__ = (
        UniqueConstraint("musicbrainz_release_id", name="uq_music_release_mbid"),
    )

    id = Column(Integer, primary_key=True)

    musicbrainz_release_id = Column(String, nullable=False)
    musicbrainz_artist_id = Column(String, nullable=False)

    artist_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)

    status = Column(String, nullable=True)
    release_type = Column(String, nullable=True)
    country = Column(String, nullable=True)

    source_url = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)