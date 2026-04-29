from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class TmdbMovieRelease(Base):
    __tablename__ = "tmdb_movie_releases"

    __table_args__ = (
        UniqueConstraint("tmdb_movie_id", "matched_kind", "matched_tmdb_id", name="uq_tmdb_movie_release_match"),
    )

    id = Column(Integer, primary_key=True)

    tmdb_movie_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    overview = Column(Text, nullable=True)
    poster_path = Column(String, nullable=True)

    release_date = Column(Date, nullable=False)
    vote_average = Column(Float, nullable=True)
    popularity = Column(Float, nullable=True)

    matched_kind = Column(String, nullable=False)  # genre, director
    matched_tmdb_id = Column(Integer, nullable=False)
    matched_name = Column(String, nullable=False)

    source_url = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)