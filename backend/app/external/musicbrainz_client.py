# backend/app/external/musicbrainz_client.py

import asyncio

import httpx


class MusicBrainzClient:
    BASE_URL = "https://musicbrainz.org/ws/2"

    def __init__(self):
        self.headers = {
            "User-Agent": "AtAGlance/0.1 (brendanczajka77@gmail.com)",
            "Accept": "application/json",
        }

    async def _get(self, path: str, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=20, headers=self.headers) as client:
            response = await client.get(
                f"{self.BASE_URL}{path}",
                params=params,
            )
            response.raise_for_status()

        await asyncio.sleep(1.1)
        return response.json()

    async def search_artist(self, name: str) -> list[dict]:
        data = await self._get(
            "/artist",
            {
                "query": f'artist:"{name}"',
                "fmt": "json",
                "limit": 5,
            },
        )

        return data.get("artists", [])

    async def search_future_releases_for_artist(
        self,
        artist_mbid: str,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        data = await self._get(
            "/release",
            {
                "query": f'arid:{artist_mbid} AND date:[{start_date} TO {end_date}]',
                "fmt": "json",
                "limit": 100,
            },
        )

        return data.get("releases", [])