from datetime import date, datetime

from app.models.ticketmaster_concert import TicketmasterConcert


class TicketmasterConcertRepository:
    def __init__(self, db):
        self.db = db

    def upsert_many(
        self,
        concerts: list[TicketmasterConcert],
    ) -> list[TicketmasterConcert]:
        saved: list[TicketmasterConcert] = []

        for concert in concerts:
            existing = (
                self.db.query(TicketmasterConcert)
                .filter(
                    TicketmasterConcert.ticketmaster_event_id
                    == concert.ticketmaster_event_id,
                    TicketmasterConcert.location_key == concert.location_key,
                )
                .first()
            )

            if existing:
                existing.name = concert.name
                existing.event_date = concert.event_date
                existing.event_time = concert.event_time
                existing.venue_name = concert.venue_name
                existing.city = concert.city
                existing.state = concert.state
                existing.country = concert.country
                existing.latitude = concert.latitude
                existing.longitude = concert.longitude
                existing.genre = concert.genre
                existing.sub_genre = concert.sub_genre
                existing.image_url = concert.image_url
                existing.source_url = concert.source_url
                existing.fetched_at = datetime.utcnow()
                saved.append(existing)
            else:
                self.db.add(concert)
                saved.append(concert)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_between(
        self,
        location_key: str,
        start: date,
        end: date,
    ) -> list[TicketmasterConcert]:
        return (
            self.db.query(TicketmasterConcert)
            .filter(
                TicketmasterConcert.location_key == location_key,
                TicketmasterConcert.event_date >= start,
                TicketmasterConcert.event_date <= end,
            )
            .order_by(
                TicketmasterConcert.event_date.asc(),
                TicketmasterConcert.event_time.asc(),
                TicketmasterConcert.name.asc(),
            )
            .all()
        )