from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TicketmasterConcertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticketmaster_event_id: str
    location_key: str

    name: str
    event_date: date
    event_time: str | None = None

    venue_name: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    genre: str | None = None
    sub_genre: str | None = None

    image_url: str | None = None
    source_url: str | None = None

    fetched_at: datetime