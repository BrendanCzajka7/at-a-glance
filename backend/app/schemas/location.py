from pydantic import BaseModel


class LocationRead(BaseModel):
    key: str
    name: str
    latitude: float
    longitude: float
    timezone: str
    is_active: bool

    model_config = {"from_attributes": True}