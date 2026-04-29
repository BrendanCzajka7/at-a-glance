# backend/app/models/app_event.py

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.db import Base


class AppEvent(Base):
    __tablename__ = "app_events"

    id = Column(Integer, primary_key=True)

    level = Column(String, nullable=False)  # info, warning, error
    source = Column(String, nullable=False)  # tmdb, musicbrainz, nasa, weather, dashboard
    event_type = Column(String, nullable=False)  # ingest_success, ingest_failed, fetch_failed

    message = Column(Text, nullable=False)
    details = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)