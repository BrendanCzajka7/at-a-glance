from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class SpaceLaunch(Base):
    __tablename__ = "space_launches"

    __table_args__ = (
        UniqueConstraint("launch_library_id", name="uq_space_launch_library_id"),
    )

    id = Column(Integer, primary_key=True)

    launch_library_id = Column(String, nullable=False)

    name = Column(String, nullable=False)
    net = Column(DateTime, nullable=False)

    status_name = Column(String, nullable=True)
    mission_name = Column(String, nullable=True)
    mission_description = Column(Text, nullable=True)

    provider_name = Column(String, nullable=True)
    rocket_name = Column(String, nullable=True)

    pad_name = Column(String, nullable=True)
    location_name = Column(String, nullable=True)

    image_url = Column(Text, nullable=True)
    webcast_url = Column(Text, nullable=True)
    source_url = Column(Text, nullable=True)

    is_crewed = Column(Boolean, nullable=True)
    flightclub_url = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)

assert "flightclub_url" in SpaceLaunch.__table__.columns.keys()