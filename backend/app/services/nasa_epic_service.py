from datetime import datetime

from sqlalchemy.orm import Session

from app.models.nasa_epic import NasaEpicImage
from app.repositories.nasa_epic_repository import NasaEpicRepository
from app.core.settings import NASA_API_KEY


class NasaEpicService:
    def __init__(self, db: Session):
        self.repo = NasaEpicRepository(db)

    def save_latest_from_raw(self, raw_items: list[dict]) -> NasaEpicImage | None:
        if not raw_items:
            return None

        latest = raw_items[0]

        image_date = datetime.fromisoformat(latest["date"])
        date_path = image_date.strftime("%Y/%m/%d")

        image_url = (
            "https://api.nasa.gov/EPIC/archive/natural/"
            f"{date_path}/png/{latest['image']}.png"
            f"?api_key={NASA_API_KEY}"
        )

        row = NasaEpicImage(
            identifier=latest["identifier"],
            caption=latest.get("caption"),
            image_name=latest["image"],
            image_date=image_date,
            image_url=image_url,
        )

        return self.repo.upsert(row)

    def get_latest(self) -> NasaEpicImage | None:
        return self.repo.get_latest()