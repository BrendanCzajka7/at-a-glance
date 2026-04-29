from datetime import date, datetime

from app.models.nature_photo import NaturePhoto


class NaturePhotoRepository:
    def __init__(self, db):
        self.db = db

    def upsert_for_date(self, row: NaturePhoto) -> NaturePhoto:
        existing = (
            self.db.query(NaturePhoto)
            .filter(NaturePhoto.photo_date == row.photo_date)
            .first()
        )

        if existing:
            existing.theme = row.theme
            existing.pexels_photo_id = row.pexels_photo_id
            existing.photographer = row.photographer
            existing.photographer_url = row.photographer_url
            existing.pexels_url = row.pexels_url
            existing.image_url = row.image_url
            existing.alt = row.alt
            existing.avg_color = row.avg_color
            existing.fetched_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_for_date(self, photo_date: date) -> NaturePhoto | None:
        return (
            self.db.query(NaturePhoto)
            .filter(NaturePhoto.photo_date == photo_date)
            .first()
        )

    def get_latest(self) -> NaturePhoto | None:
        return (
            self.db.query(NaturePhoto)
            .order_by(NaturePhoto.photo_date.desc())
            .first()
        )