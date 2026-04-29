from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class TicketmasterConcert(Base):
    __tablename__ = "ticketmaster_concerts"

    __table_args__ = (
        UniqueConstraint(
            "ticketmaster_event_id",
            "location_key",
            name="uq_ticketmaster_event_location",
        ),
    )

    id = Column(Integer, primary_key=True)

    ticketmaster_event_id = Column(String, nullable=False)
    location_key = Column(String, nullable=False)

    name = Column(String, nullable=False)
    event_date = Column(Date, nullable=False)
    event_time = Column(String, nullable=True)

    venue_name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    genre = Column(String, nullable=True)
    sub_genre = Column(String, nullable=True)

    image_url = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)