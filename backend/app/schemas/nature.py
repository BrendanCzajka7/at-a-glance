from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class NaturePhotoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    photo_date: date

    theme: str
    pexels_photo_id: int | None = None

    photographer: str | None = None
    photographer_url: str | None = None

    pexels_url: str | None = None
    image_url: str

    alt: str | None = None
    avg_color: str | None = None

    fetched_at: datetime