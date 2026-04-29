# backend/app/repositories/music_artist_repository.py

from app.models.music_artist import MusicArtist


class MusicArtistRepository:
    def __init__(self, db):
        self.db = db

    def get_by_mbid(self, musicbrainz_artist_id: str) -> MusicArtist | None:
        return (
            self.db.query(MusicArtist)
            .filter(MusicArtist.musicbrainz_artist_id == musicbrainz_artist_id)
            .first()
        )

    def list_active(self) -> list[MusicArtist]:
        return (
            self.db.query(MusicArtist)
            .filter(MusicArtist.is_active == True)
            .order_by(MusicArtist.name.asc())
            .all()
        )

    def upsert(self, artist: MusicArtist) -> MusicArtist:
        existing = self.get_by_mbid(artist.musicbrainz_artist_id)

        if existing:
            existing.name = artist.name
            existing.is_active = True
            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(artist)
        self.db.commit()
        self.db.refresh(artist)
        return artist