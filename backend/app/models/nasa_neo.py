from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class NasaNeoCloseApproach(Base):
    __tablename__ = "nasa_neo_close_approaches"

    __table_args__ = (
        UniqueConstraint(
            "neo_reference_id",
            "close_approach_date",
            name="uq_nasa_neo_close_approach",
        ),
    )

    id = Column(Integer, primary_key=True)

    neo_reference_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    nasa_jpl_url = Column(Text, nullable=True)

    close_approach_date = Column(Date, nullable=False)
    close_approach_time = Column(String, nullable=True)

    estimated_diameter_min_m = Column(Float, nullable=True)
    estimated_diameter_max_m = Column(Float, nullable=True)

    miss_distance_km = Column(Float, nullable=True)
    miss_distance_lunar = Column(Float, nullable=True)
    relative_velocity_kph = Column(Float, nullable=True)

    is_potentially_hazardous = Column(Boolean, nullable=False, default=False)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)