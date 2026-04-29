from datetime import datetime

from pydantic import BaseModel


class NasaEpicImageRead(BaseModel):
    id: int
    identifier: str
    caption: str | None = None
    image_name: str
    image_date: datetime
    image_url: str
    fetched_at: datetime

    model_config = {"from_attributes": True}