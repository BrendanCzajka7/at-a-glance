from datetime import date

from sqlalchemy.orm import Session

from app.models.nasa_apod import NasaApod
from app.repositories.nasa_apod_repository import NasaApodRepository


class NasaApodService:
    def __init__(self, db: Session):
        self.repo = NasaApodRepository(db)

    def save_from_raw(self, raw: dict) -> NasaApod:
        apod = NasaApod(
            apod_date=date.fromisoformat(raw["date"]),
            title=raw["title"],
            explanation=raw["explanation"],
            image_url=raw.get("url"),
            hd_image_url=raw.get("hdurl"),
            media_type=raw["media_type"],
            copyright=raw.get("copyright"),
            source_url=raw.get("url"),
        )

        return self.repo.upsert(apod)

    def get_latest(self) -> NasaApod | None:
        return self.repo.get_latest()