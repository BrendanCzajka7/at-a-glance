from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class NaturePhoto(Base):
    __tablename__ = "nature_photos"

    __table_args__ = (
        UniqueConstraint("photo_date", "theme", name="uq_nature_photo_date_theme"),
    )

    id = Column(Integer, primary_key=True)

    photo_date = Column(Date, nullable=False)
    theme = Column(String, nullable=False)

    pexels_photo_id = Column(Integer, nullable=True)

    photographer = Column(String, nullable=True)
    photographer_url = Column(Text, nullable=True)

    pexels_url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=False)

    alt = Column(Text, nullable=True)
    avg_color = Column(String, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)