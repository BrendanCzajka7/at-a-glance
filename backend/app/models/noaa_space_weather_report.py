from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text

from app.core.db import Base


class NoaaSpaceWeatherReport(Base):
    __tablename__ = "noaa_space_weather_reports"

    id = Column(Integer, primary_key=True)

    scales_json = Column(Text, nullable=True)
    alerts_json = Column(Text, nullable=True)
    three_day_forecast_text = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)