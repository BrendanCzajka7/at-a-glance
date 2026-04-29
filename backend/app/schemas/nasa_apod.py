from datetime import date, datetime

from pydantic import BaseModel


class NasaApodRead(BaseModel):
    id: int
    apod_date: date

    title: str
    explanation: str

    image_url: str | None = None
    hd_image_url: str | None = None

    media_type: str
    copyright: str | None = None
    source_url: str | None = None

    fetched_at: datetime

    model_config = {"from_attributes": True}