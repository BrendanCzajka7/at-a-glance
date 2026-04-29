from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class NasaSpaceWeatherNotification(Base):
    __tablename__ = "nasa_space_weather_notifications"

    __table_args__ = (
        UniqueConstraint("message_id", name="uq_nasa_space_weather_message_id"),
    )

    id = Column(Integer, primary_key=True)

    message_id = Column(String, nullable=False)
    message_type = Column(String, nullable=True)
    message_issue_time = Column(DateTime, nullable=False)
    message_url = Column(Text, nullable=True)

    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)

    raw_message_body = Column(Text, nullable=False)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)