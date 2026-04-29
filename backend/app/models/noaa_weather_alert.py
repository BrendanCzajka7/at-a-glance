from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class NoaaWeatherAlert(Base):
    __tablename__ = "noaa_weather_alerts"

    __table_args__ = (
        UniqueConstraint(
            "location_key",
            "nws_alert_id",
            name="uq_noaa_weather_alert_location_id",
        ),
    )

    id = Column(Integer, primary_key=True)

    location_key = Column(String, nullable=False)
    nws_alert_id = Column(String, nullable=False)

    event = Column(String, nullable=False)
    headline = Column(Text, nullable=True)

    severity = Column(String, nullable=True)
    urgency = Column(String, nullable=True)
    certainty = Column(String, nullable=True)

    effective = Column(DateTime, nullable=True)
    expires = Column(DateTime, nullable=True)

    description = Column(Text, nullable=True)
    instruction = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)