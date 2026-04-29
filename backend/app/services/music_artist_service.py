# backend/app/services/music_artist_service.py

from app.models.music_artist import MusicArtist
from app.repositories.music_artist_repository import MusicArtistRepository


class MusicArtistService:
    def __init__(self, db):
        self.repo = MusicArtistRepository(db)

    def create_or_update(
        self,
        name: str,
        musicbrainz_artist_id: str,
    ) -> MusicArtist:
        return self.repo.upsert(
            MusicArtist(
                name=name,
                musicbrainz_artist_id=musicbrainz_artist_id,
                is_active=True,
            )
        )

    def list_active(self) -> list[MusicArtist]:
        return self.repo.list_active()