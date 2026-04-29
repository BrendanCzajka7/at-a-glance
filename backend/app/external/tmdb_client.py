import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class TmdbClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.bearer_token = os.getenv("TMDB_BEARER_TOKEN")

        if not self.api_key and not self.bearer_token:
            raise RuntimeError("TMDB_API_KEY or TMDB_BEARER_TOKEN is required")

    def _headers(self) -> dict:
        if self.bearer_token:
            return {"Authorization": f"Bearer {self.bearer_token}"}

        return {}

    def _params(self, params: dict | None = None) -> dict:
        final = dict(params or {})

        if self.api_key and not self.bearer_token:
            final["api_key"] = self.api_key

        return final

    async def _get(self, path: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(timeout=20, headers=self._headers()) as client:
            response = await client.get(
                f"{self.BASE_URL}{path}",
                params=self._params(params),
            )
            response.raise_for_status()
            return response.json()

    async def list_movie_genres(self) -> list[dict]:
        data = await self._get(
            "/genre/movie/list",
            {"language": "en-US"},
        )

        return data.get("genres", [])

    async def search_directors(self, query: str) -> list[dict]:
        data = await self._get(
            "/search/person",
            {
                "query": query,
                "include_adult": "false",
                "language": "en-US",
                "page": 1,
            },
        )

        results = data.get("results", [])

        return [
            item
            for item in results
            if item.get("known_for_department") == "Directing"
        ]

    async def discover_movies_for_genre(
        self,
        genre_id: int,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        return await self._discover_movies(
            {
                "with_genres": str(genre_id),
                "primary_release_date.gte": start_date,
                "primary_release_date.lte": end_date,
            }
        )

    async def discover_movies_for_director(
        self,
        director_id: int,
        start_date: str,
        end_date: str,
    ) -> list[dict]:
        return await self._discover_movies(
            {
                "with_crew": str(director_id),
                "primary_release_date.gte": start_date,
                "primary_release_date.lte": end_date,
            }
        )

    async def _discover_movies(self, extra_params: dict) -> list[dict]:
        params = {
            "include_adult": "false",
            "include_video": "false",
            "language": "en-US",
            "page": 1,
            "sort_by": "primary_release_date.asc",
            "region": "US",
            "with_release_type": "2|3",
            **extra_params,
        }

        data = await self._get("/discover/movie", params)
        return data.get("results", [])