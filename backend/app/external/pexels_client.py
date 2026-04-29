import os
import random
from pathlib import Path

import httpx
from dotenv import load_dotenv

from app.nature_themes import NATURE_THEMES

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class PexelsClient:
    BASE_URL = "https://api.pexels.com/v1/search"

    def __init__(self):
        self.api_key = os.getenv("PEXELS_API_KEY")

        if not self.api_key:
            raise RuntimeError("PEXELS_API_KEY is required")

    async def fetch_nature_photo(self, theme: str | None = None) -> dict | None:
        query = theme or self.pick_theme()

        params = {
            "query": query,
            "per_page": 20,
            "orientation": "landscape",
            "size": "large",
            "locale": "en-US",
        }

        headers = {"Authorization": self.api_key}

        async with httpx.AsyncClient(timeout=20, headers=headers) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        photos = data.get("photos", [])

        if not photos:
            return None

        photo = self.pick_best_photo(photos)
        src = photo.get("src") or {}

        return {
            "theme": query,
            "pexels_photo_id": photo.get("id"),
            "photographer": photo.get("photographer"),
            "photographer_url": photo.get("photographer_url"),
            "pexels_url": photo.get("url"),
            "image_url": src.get("large2x") or src.get("large") or src.get("original"),
            "alt": photo.get("alt"),
            "avg_color": photo.get("avg_color"),
        }

    def pick_theme(self) -> str:
        return random.choice(NATURE_THEMES)

    def pick_best_photo(self, photos: list[dict]) -> dict:
        usable = [
            photo
            for photo in photos
            if (photo.get("src") or {}).get("large")
            or (photo.get("src") or {}).get("large2x")
        ]

        if not usable:
            return photos[0]

        return random.choice(usable[:8])