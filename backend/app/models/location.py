from sqlalchemy import Boolean, Column, Float, Integer, String, UniqueConstraint

from app.core.db import Base


class Location(Base):
    __tablename__ = "locations"

    __table_args__ = (
        UniqueConstraint("key", name="uq_locations_key"),
    )

    id = Column(Integer, primary_key=True, index=True)

    key = Column(String, nullable=False)
    name = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String, nullable=False)
    noaa_tide_station_id = Column(String, nullable=True)
    ndbc_station_id = Column(String, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
