from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, UniqueConstraint

from app.core.db import Base


class NasaEpicImage(Base):
    __tablename__ = "nasa_epic_images"

    __table_args__ = (
        UniqueConstraint("identifier", name="uq_nasa_epic_identifier"),
    )

    id = Column(Integer, primary_key=True)

    identifier = Column(String, nullable=False)
    caption = Column(Text, nullable=True)
    image_name = Column(String, nullable=False)

    image_date = Column(DateTime, nullable=False)
    image_url = Column(Text, nullable=False)

    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)