from datetime import date, timedelta

from app.external.musicbrainz_client import MusicBrainzClient
from app.services.music_artist_service import MusicArtistService
from app.services.music_release_service import MusicReleaseService


class MusicReleaseIngestPipeline:
    def __init__(self, db):
        self.client = MusicBrainzClient()
        self.artist_service = MusicArtistService(db)
        self.release_service = MusicReleaseService(db)

    async def run_for_all_artists(self):
        saved = []

        for artist in self.artist_service.list_active():
            saved.extend(
                await self.run_for_artist(
                    artist_name=artist.name,
                    musicbrainz_artist_id=artist.musicbrainz_artist_id,
                )
            )

        return saved

    async def run_for_artist(
        self,
        artist_name: str,
        musicbrainz_artist_id: str,
    ):
        start = date.today()
        end = start + timedelta(days=31)

        raw_releases = await self.client.search_future_releases_for_artist(
            artist_mbid=musicbrainz_artist_id,
            start_date=start.isoformat(),
            end_date=end.isoformat(),
        )

        return self.release_service.save_from_raw_releases(
            artist_name=artist_name,
            musicbrainz_artist_id=musicbrainz_artist_id,
            raw_releases=raw_releases,
        )