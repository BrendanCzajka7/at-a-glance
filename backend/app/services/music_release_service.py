# backend/app/services/music_release_service.py

from datetime import date

from app.models.music_release import MusicRelease
from app.repositories.music_release_repository import MusicReleaseRepository


class MusicReleaseService:
    def __init__(self, db):
        self.repo = MusicReleaseRepository(db)

    def save_from_raw_releases(
        self,
        artist_name: str,
        musicbrainz_artist_id: str,
        raw_releases: list[dict],
    ) -> list[MusicRelease]:
        rows: list[MusicRelease] = []
        seen: set[tuple[str, str, str]] = set()

        for raw in raw_releases:
            release_date_raw = raw.get("date")

            if not release_date_raw:
                continue

            try:
                release_date = date.fromisoformat(release_date_raw)
            except ValueError:
                continue

            release_id = raw.get("id")
            title = raw.get("title")

            if not release_id or not title:
                continue

            dedupe_key = (
                artist_name.lower().strip(),
                title.lower().strip(),
                release_date.isoformat(),
            )

            if dedupe_key in seen:
                continue

            seen.add(dedupe_key)

            rows.append(
                MusicRelease(
                    musicbrainz_release_id=release_id,
                    musicbrainz_artist_id=musicbrainz_artist_id,
                    artist_name=artist_name,
                    title=title,
                    release_date=release_date,
                    status=raw.get("status"),
                    release_type=", ".join(raw.get("type", []))
                    if isinstance(raw.get("type"), list)
                    else raw.get("type"),
                    country=raw.get("country"),
                    source_url=f"https://musicbrainz.org/release/{release_id}",
                )
            )

        return self.repo.upsert_many(rows)

    def list_between(self, start: date, end: date) -> list[MusicRelease]:
        return self.repo.list_between(start=start, end=end)