from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from app.core.db import Base


class TmdbWatchItem(Base):
    __tablename__ = "tmdb_watch_items"

    __table_args__ = (
        UniqueConstraint("kind", "tmdb_id", name="uq_tmdb_watch_item_kind_id"),
    )

    id = Column(Integer, primary_key=True)

    kind = Column(String, nullable=False)  # genre, director
    tmdb_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)