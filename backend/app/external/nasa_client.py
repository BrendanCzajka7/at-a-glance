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