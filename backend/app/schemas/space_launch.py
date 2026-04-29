from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SpaceLaunchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    launch_library_id: str

    name: str
    net: datetime

    status_name: str | None = None
    mission_name: str | None = None
    mission_description: str | None = None

    provider_name: str | None = None
    rocket_name: str | None = None

    pad_name: str | None = None
    location_name: str | None = None

    image_url: str | None = None
    webcast_url: str | None = None
    source_url: str | None = None

    is_crewed: bool | None = None

    fetched_at: datetime