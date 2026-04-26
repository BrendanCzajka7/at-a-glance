from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, text

from app.core.db import Base


class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    location_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    temperature_f = Column(Float, nullable=False)
    wind_speed_mph = Column(Float, nullable=True)
    weather_code = Column(Integer, nullable=True)

    observed_at = Column(DateTime, nullable=False)
    ingested_at = Column(
    DateTime(timezone=True),
    server_default=text("CURRENT_TIMESTAMP"),
    nullable=False,
)