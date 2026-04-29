import httpx


class UsgsClient:
    BASE_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary"

    async def fetch_significant_recent_earthquakes(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.BASE_URL}/2.5_day.geojson")
            response.raise_for_status()
            data = response.json()

        return data.get("features", [])