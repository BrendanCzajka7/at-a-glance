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


class NasaSpaceWeatherCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message_id: str
    message_type: str | None = None
    message_issue_time: datetime
    title: str
    summary: str
    message_url: str | None = None


class NasaSpaceWeatherSection(BaseModel):
    today: list[NasaSpaceWeatherCard]
    week: list[NasaSpaceWeatherCard]


class NasaSection(BaseModel):
    apod: NasaApodCard | None = None
    space_weather: NasaSpaceWeatherSection