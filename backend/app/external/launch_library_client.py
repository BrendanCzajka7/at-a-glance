from datetime import datetime

import httpx


class LaunchLibraryClient:
    BASE_URL = "https://ll.thespacedevs.com/2.2.0"

    async def fetch_upcoming_launches(
        self,
        start: datetime,
        end: datetime,
    ) -> list[dict]:
        params = {
            "mode": "normal",
            "limit": 100,
            "ordering": "net",
            "net__gte": start.isoformat(),
            "net__lte": end.isoformat(),
        }

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                f"{self.BASE_URL}/launch/upcoming/",
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        return data.get("results", [])