from datetime import date

from app.models.nature_photo import NaturePhoto
from app.repositories.nature_photo_repository import NaturePhotoRepository


class NaturePhotoService:
    def __init__(self, db):
        self.repo = NaturePhotoRepository(db)

    def save_from_raw(
        self,
        photo_date: date,
        raw: dict,
    ) -> NaturePhoto:
        image_url = raw.get("image_url")

        if not image_url:
            raise ValueError("Pexels photo is missing image_url")

        return self.repo.upsert_for_date_and_theme(
            NaturePhoto(
                photo_date=photo_date,
                theme=raw["theme"],
                pexels_photo_id=raw.get("pexels_photo_id"),
                photographer=raw.get("photographer"),
                photographer_url=raw.get("photographer_url"),
                pexels_url=raw.get("pexels_url"),
                image_url=image_url,
                alt=raw.get("alt"),
                avg_color=raw.get("avg_color"),
            )
        )

    def list_for_date(self, photo_date: date) -> list[NaturePhoto]:
        return self.repo.list_for_date(photo_date=photo_date)

    def get_for_date_and_theme(
        self,
        photo_date: date,
        theme: str,
    ) -> NaturePhoto | None:
        return self.repo.get_for_date_and_theme(
            photo_date=photo_date,
            theme=theme,
        )