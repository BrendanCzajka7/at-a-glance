import httpx

from app.core.settings import NASA_API_KEY


class NasaClient:
    BASE_URL = "https://api.nasa.gov/planetary/apod"

    async def fetch_apod(self):
        params = {
            "api_key": NASA_API_KEY,
        }

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()

    async def fetch_space_weather_notifications(
        self,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        url = "https://api.nasa.gov/DONKI/notifications"

        params = {
            "startDate": start_date,
            "endDate": end_date,
            "api_key": NASA_API_KEY,
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def fetch_neows_feed(
        self,
        start_date: str,
        end_date: str,
    ) -> dict:
        url = "https://api.nasa.gov/neo/rest/v1/feed"

        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": NASA_API_KEY,
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def fetch_epic_latest_natural(self) -> list[dict]:
        url = "https://api.nasa.gov/EPIC/api/natural"

        params = {
            "api_key": NASA_API_KEY,
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()