from datetime import datetime, timedelta

from app.schemas.ticketmaster_dashboard import (
    TicketmasterConcertCard,
    TicketmasterSection,
)
from app.services.ticketmaster_concert_service import TicketmasterConcertService


class TicketmasterDashboardSection:
    def __init__(self, db):
        self.concert_service = TicketmasterConcertService(db)

    def build(
        self,
        start: datetime,
        location_key: str,
    ) -> TicketmasterSection:
        today = start.date()
        week_end = today + timedelta(days=7)
        month_end = today + timedelta(days=31)

        month_concerts = self.concert_service.list_between(
            location_key=location_key,
            start=today,
            end=month_end,
        )

        today_concerts = [
            concert for concert in month_concerts
            if concert.event_date == today
        ]

        week_concerts = [
            concert for concert in month_concerts
            if today <= concert.event_date <= week_end
        ]

        return TicketmasterSection(
            today=[
                TicketmasterConcertCard.model_validate(concert)
                for concert in today_concerts
            ],
            week=[
                TicketmasterConcertCard.model_validate(concert)
                for concert in week_concerts
            ],
            month=[
                TicketmasterConcertCard.model_validate(concert)
                for concert in month_concerts
            ],
        )