import os
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"


def encode_geohash(latitude: float, longitude: float, precision: int = 9) -> str:
    lat_interval = [-90.0, 90.0]
    lon_interval = [-180.0, 180.0]
    geohash = []
    bits = [16, 8, 4, 2, 1]
    bit = 0
    char_value = 0
    even_bit = True

    while len(geohash) < precision:
        if even_bit:
            mid = sum(lon_interval) / 2
            if longitude >= mid:
                char_value |= bits[bit]
                lon_interval[0] = mid
            else:
                lon_interval[1] = mid
        else:
            mid = sum(lat_interval) / 2
            if latitude >= mid:
                char_value |= bits[bit]
                lat_interval[0] = mid
            else:
                lat_interval[1] = mid

        even_bit = not even_bit

        if bit < 4:
            bit += 1
        else:
            geohash.append(_BASE32[char_value])
            bit = 0
            char_value = 0

    return "".join(geohash)


class TicketmasterClient:
    BASE_URL = "https://app.ticketmaster.com/discovery/v2"

    def __init__(self):
        self.api_key = os.getenv("TICKETMASTER_API_KEY")

        if not self.api_key:
            raise RuntimeError("TICKETMASTER_API_KEY is required")

    async def search_music_events_near_location(
        self,
        latitude: float,
        longitude: float,
        start: datetime,
        end: datetime,
        radius_miles: int = 75,
    ) -> list[dict]:
        geo_point = encode_geohash(latitude, longitude)

        params = {
            "apikey": self.api_key,
            "classificationName": "music",
            "geoPoint": geo_point,
            "radius": radius_miles,
            "unit": "miles",
            "countryCode": "US",
            "sort": "date,asc",
            "size": 100,
            "startDateTime": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endDateTime": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.BASE_URL}/events.json", params=params)
            response.raise_for_status()
            data = response.json()

        return data.get("_embedded", {}).get("events", [])