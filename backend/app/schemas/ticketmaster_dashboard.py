from datetime import date

from pydantic import BaseModel, ConfigDict


class TicketmasterConcertCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    event_date: date
    event_time: str | None = None

    venue_name: str | None = None
    city: str | None = None
    state: str | None = None

    genre: str | None = None
    sub_genre: str | None = None

    image_url: str | None = None
    source_url: str | None = None


class TicketmasterSection(BaseModel):
    today: list[TicketmasterConcertCard]
    week: list[TicketmasterConcertCard]
    month: list[TicketmasterConcertCard]