from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from app.core.db import Base


class NasaApod(Base):
    __tablename__ = "nasa_apod"

    id = Column(Integer, primary_key=True)

    apod_date = Column(Date, unique=True, nullable=False)

    title = Column(String, nullable=False)
    explanation = Column(Text, nullable=False)

    image_url = Column(Text, nullable=True)
    hd_image_url = Column(Text, nullable=True)

    media_type = Column(String, nullable=False)
    copyright = Column(String, nullable=True)

    source_url = Column(Text, nullable=True)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)