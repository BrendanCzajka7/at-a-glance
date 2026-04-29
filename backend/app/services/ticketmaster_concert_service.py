import math
from datetime import date

from app.models.ticketmaster_concert import TicketmasterConcert
from app.repositories.ticketmaster_concert_repository import (
    TicketmasterConcertRepository,
)


class TicketmasterConcertService:
    def __init__(self, db):
        self.repo = TicketmasterConcertRepository(db)

    def save_from_raw_events(
        self,
        location_key: str,
        origin_latitude: float,
        origin_longitude: float,
        radius_miles: int,
        raw_events: list[dict],
    ) -> list[TicketmasterConcert]:
        rows: list[TicketmasterConcert] = []
        seen_event_ids: set[str] = set()

        for raw in raw_events:
            event_id = raw.get("id")
            name = raw.get("name")

            start_data = raw.get("dates", {}).get("start", {})
            event_date_raw = start_data.get("localDate")
            event_time = start_data.get("localTime")

            if not event_id or not name or not event_date_raw:
                continue

            if event_id in seen_event_ids:
                continue

            seen_event_ids.add(event_id)

            try:
                event_date = date.fromisoformat(event_date_raw)
            except ValueError:
                continue

            venue = raw.get("_embedded", {}).get("venues", [{}])[0]

            city = venue.get("city", {}).get("name")
            state = venue.get("state", {}).get("stateCode")
            country = venue.get("country", {}).get("countryCode")

            location = venue.get("location", {})
            latitude = _safe_float(location.get("latitude"))
            longitude = _safe_float(location.get("longitude"))

            # Critical safety filter:
            # Ticketmaster can occasionally return weird out-of-area results.
            # Only save events whose venue coordinates are actually within radius.
            if latitude is None or longitude is None:
                continue

            distance = _distance_miles(
                origin_latitude,
                origin_longitude,
                latitude,
                longitude,
            )

            if distance > radius_miles:
                continue

            classification = (raw.get("classifications") or [{}])[0]
            genre = classification.get("genre", {}).get("name")
            sub_genre = classification.get("subGenre", {}).get("name")

            image_url = _pick_best_image_url(raw.get("images") or [])

            rows.append(
                TicketmasterConcert(
                    ticketmaster_event_id=event_id,
                    location_key=location_key,
                    name=name,
                    event_date=event_date,
                    event_time=event_time,
                    venue_name=venue.get("name"),
                    city=city,
                    state=state,
                    country=country,
                    latitude=latitude,
                    longitude=longitude,
                    genre=genre,
                    sub_genre=sub_genre,
                    image_url=image_url,
                    source_url=raw.get("url"),
                )
            )

        return self.repo.upsert_many(rows)

    def list_between(
        self,
        location_key: str,
        start: date,
        end: date,
    ) -> list[TicketmasterConcert]:
        return self.repo.list_between(
            location_key=location_key,
            start=start,
            end=end,
        )


def _safe_float(value):
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _distance_miles(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    earth_radius_miles = 3958.8

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_miles * c


def _pick_best_image_url(images: list[dict]) -> str | None:
    if not images:
        return None

    sorted_images = sorted(
        images,
        key=lambda image: (image.get("width") or 0) * (image.get("height") or 0),
        reverse=True,
    )

    return sorted_images[0].get("url")