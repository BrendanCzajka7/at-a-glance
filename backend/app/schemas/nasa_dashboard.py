from datetime import date

from pydantic import BaseModel, ConfigDict


class NasaApodCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    apod_date: date
    title: str
    explanation: str
    image_url: str | None = None
    hd_image_url: str | None = None
    media_type: str
    copyright: str | None = None


class NasaSection(BaseModel):
    apod: NasaApodCard | None = None