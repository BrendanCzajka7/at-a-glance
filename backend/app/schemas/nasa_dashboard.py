from datetime import date, datetime

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


class NasaEpicCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    identifier: str
    caption: str | None = None
    image_date: datetime
    image_url: str


class NasaNeoCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    neo_reference_id: str
    name: str
    nasa_jpl_url: str | None = None
    close_approach_date: date
    close_approach_time: str | None = None
    estimated_diameter_max_m: float | None = None
    miss_distance_lunar: float | None = None
    relative_velocity_kph: float | None = None
    is_potentially_hazardous: bool


class NasaNeoSection(BaseModel):
    today: list[NasaNeoCard]
    week: list[NasaNeoCard]
    month: list[NasaNeoCard]


class NasaSection(BaseModel):
    apod: NasaApodCard | None = None
    epic: NasaEpicCard | None = None
    neos: NasaNeoSection