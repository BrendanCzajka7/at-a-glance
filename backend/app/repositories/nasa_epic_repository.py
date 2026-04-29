from datetime import datetime

from sqlalchemy.orm import Session

from app.models.nasa_epic import NasaEpicImage


class NasaEpicRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(self, row: NasaEpicImage) -> NasaEpicImage:
        existing = (
            self.db.query(NasaEpicImage)
            .filter(NasaEpicImage.identifier == row.identifier)
            .first()
        )

        if existing:
            existing.caption = row.caption
            existing.image_name = row.image_name
            existing.image_date = row.image_date
            existing.image_url = row.image_url
            existing.fetched_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_latest(self) -> NasaEpicImage | None:
        return (
            self.db.query(NasaEpicImage)
            .order_by(NasaEpicImage.image_date.desc())
            .first()
        )