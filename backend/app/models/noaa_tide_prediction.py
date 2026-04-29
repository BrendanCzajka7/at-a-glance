from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint

from app.core.db import Base


class NoaaTidePrediction(Base):
    __tablename__ = "noaa_tide_predictions"

    __table_args__ = (
        UniqueConstraint(
            "location_key",
            "station_id",
            "prediction_time",
            "tide_type",
            name="uq_noaa_tide_prediction",
        ),
    )

    id = Column(Integer, primary_key=True)

    location_key = Column(String, nullable=False)
    station_id = Column(String, nullable=False)

    prediction_time = Column(DateTime, nullable=False)
    tide_type = Column(String, nullable=True)  # H or L
    height_ft = Column(Float, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)