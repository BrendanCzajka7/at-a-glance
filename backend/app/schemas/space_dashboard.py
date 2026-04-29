from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SpaceLaunchCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    net: datetime

    status_name: str | None = None
    mission_name: str | None = None

    provider_name: str | None = None
    rocket_name: str | None = None

    pad_name: str | None = None
    location_name: str | None = None

    image_url: str | None = None
    webcast_url: str | None = None
    source_url: str | None = None

    is_crewed: bool | None = None


class SpaceSection(BaseModel):
    today: list[SpaceLaunchCard]
    week: list[SpaceLaunchCard]
    month: list[SpaceLaunchCard]