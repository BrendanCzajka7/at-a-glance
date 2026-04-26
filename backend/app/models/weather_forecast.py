from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint

from app.core.db import Base


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "location_key",
            "forecast_for",
            "granularity",
            name="uq_weather_forecast_unique_time",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String, nullable=False, default="open_meteo")
    location_key = Column(String, nullable=False)
    location_name = Column(String, nullable=False)

    granularity = Column(String, nullable=False)  # current, hourly, daily
    forecast_for = Column(DateTime, nullable=False)

    temperature_f = Column(Float, nullable=True)
    temperature_max_f = Column(Float, nullable=True)
    temperature_min_f = Column(Float, nullable=True)
    apparent_temperature_f = Column(Float, nullable=True)

    precipitation_probability = Column(Integer, nullable=True)
    precipitation_inches = Column(Float, nullable=True)

    wind_speed_mph = Column(Float, nullable=True)
    wind_gust_mph = Column(Float, nullable=True)

    uv_index = Column(Float, nullable=True)
    weather_code = Column(Integer, nullable=True)

    sunrise = Column(DateTime, nullable=True)
    sunset = Column(DateTime, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)