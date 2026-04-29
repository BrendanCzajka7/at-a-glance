from app.models.nasa_apod import NasaApod


class NasaApodRepository:
    def __init__(self, db):
        self.db = db

    def upsert(self, row: NasaApod):
        existing = (
            self.db.query(NasaApod)
            .filter(NasaApod.apod_date == row.apod_date)
            .first()
        )

        if existing:
            existing.title = row.title
            existing.explanation = row.explanation
            existing.image_url = row.image_url
            existing.hd_image_url = row.hd_image_url
            existing.media_type = row.media_type
            existing.copyright = row.copyright
            existing.source_url = row.source_url
            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def get_latest(self):
        return (
            self.db.query(NasaApod)
            .order_by(NasaApod.apod_date.desc())
            .first()
        )