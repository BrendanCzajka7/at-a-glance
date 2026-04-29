from datetime import date

from pydantic import BaseModel, ConfigDict


class NaturePhotoCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    photo_date: date
    theme: str

    photographer: str | None = None
    photographer_url: str | None = None

    pexels_url: str | None = None
    image_url: str

    alt: str | None = None
    avg_color: str | None = None


class NatureSection(BaseModel):
    today: list[NaturePhotoCard]