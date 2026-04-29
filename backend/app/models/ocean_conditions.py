from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint

from app.core.db import Base


class OceanConditions(Base):
    __tablename__ = "ocean_conditions"

    __table_args__ = (
        UniqueConstraint(
            "location_key",
            "station_id",
            "observed_at",
            name="uq_ocean_conditions_location_station_time",
        ),
    )

    id = Column(Integer, primary_key=True)

    location_key = Column(String, nullable=False)
    station_id = Column(String, nullable=False)

    observed_at = Column(DateTime, nullable=False)

    water_temperature_f = Column(Float, nullable=True)
    wave_height_ft = Column(Float, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)