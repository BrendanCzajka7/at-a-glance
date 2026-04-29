from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class UsgsEarthquake(Base):
    __tablename__ = "usgs_earthquakes"

    __table_args__ = (
        UniqueConstraint("usgs_event_id", name="uq_usgs_earthquake_event_id"),
    )

    id = Column(Integer, primary_key=True)

    usgs_event_id = Column(String, nullable=False)

    title = Column(String, nullable=False)
    place = Column(String, nullable=True)

    magnitude = Column(Float, nullable=True)
    event_time = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    depth_km = Column(Float, nullable=True)

    tsunami = Column(Integer, nullable=True)
    significance = Column(Integer, nullable=True)
    alert = Column(String, nullable=True)
    status = Column(String, nullable=True)

    event_type = Column(String, nullable=True)
    magnitude_type = Column(String, nullable=True)

    source_url = Column(Text, nullable=True)
    detail_url = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)