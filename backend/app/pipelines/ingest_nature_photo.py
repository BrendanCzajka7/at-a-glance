from datetime import datetime

from app.external.pexels_client import PexelsClient
from app.nature_themes import NATURE_THEMES, is_valid_nature_theme
from app.services.nature_photo_service import NaturePhotoService


class NaturePhotoIngestPipeline:
    def __init__(self, db):
        self.client = PexelsClient()
        self.nature_service = NaturePhotoService(db)

    async def run_for_today(self, theme: str):
        if not is_valid_nature_theme(theme):
            raise ValueError(f"Invalid nature theme: {theme}")

        today = datetime.utcnow().date()
        raw = await self.client.fetch_nature_photo(theme=theme)

        if not raw:
            return None

        return self.nature_service.save_from_raw(
            photo_date=today,
            raw=raw,
        )

    async def run_all_for_today(self):
        saved = []

        for theme in NATURE_THEMES:
            row = await self.run_for_today(theme)

            if row:
                saved.append(row)

        return saved