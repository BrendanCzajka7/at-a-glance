# backend/app/repositories/music_release_repository.py

from datetime import date, datetime

from app.models.music_release import MusicRelease


class MusicReleaseRepository:
    def __init__(self, db):
        self.db = db

    def upsert_many(self, releases: list[MusicRelease]) -> list[MusicRelease]:
        saved: list[MusicRelease] = []

        for release in releases:
            existing = (
                self.db.query(MusicRelease)
                .filter(
                    MusicRelease.musicbrainz_release_id
                    == release.musicbrainz_release_id
                )
                .first()
            )

            if existing:
                existing.artist_name = release.artist_name
                existing.title = release.title
                existing.release_date = release.release_date
                existing.status = release.status
                existing.release_type = release.release_type
                existing.country = release.country
                existing.source_url = release.source_url
                existing.fetched_at = datetime.utcnow()
                saved.append(existing)
            else:
                self.db.add(release)
                saved.append(release)

        self.db.commit()

        for item in saved:
            self.db.refresh(item)

        return saved

    def list_between(self, start: date, end: date) -> list[MusicRelease]:
        return (
            self.db.query(MusicRelease)
            .filter(
                MusicRelease.release_date >= start,
                MusicRelease.release_date <= end,
            )
            .order_by(MusicRelease.release_date.asc(), MusicRelease.artist_name.asc())
            .all()
        )