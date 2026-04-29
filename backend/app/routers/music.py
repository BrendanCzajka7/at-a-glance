from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.external.musicbrainz_client import MusicBrainzClient
from app.pipelines.ingest_music_releases import MusicReleaseIngestPipeline
from app.schemas.music import MusicArtistRead, MusicReleaseRead
from app.services.music_artist_service import MusicArtistService
from app.services.music_release_service import MusicReleaseService


router = APIRouter(prefix="/api/music", tags=["music"])


@router.get("/artist-search")
async def search_artists(name: str = Query(...)):
    client = MusicBrainzClient()
    artists = await client.search_artist(name)

    return [
        {
            "musicbrainz_artist_id": artist.get("id"),
            "name": artist.get("name"),
            "sort_name": artist.get("sort-name"),
            "country": artist.get("country"),
            "disambiguation": artist.get("disambiguation"),
            "score": artist.get("score"),
            "type": artist.get("type"),
        }
        for artist in artists
    ]


@router.post("/artists", response_model=MusicArtistRead)
async def add_artist(
    name: str = Query(...),
    musicbrainz_artist_id: str = Query(...),
    ingest_now: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    artist = MusicArtistService(db).create_or_update(
        name=name,
        musicbrainz_artist_id=musicbrainz_artist_id,
    )

    if ingest_now:
        await run_logged_pipeline(
            db=db,
            source="musicbrainz",
            event_type="ingest_music_artist_failed",
            message=f"MusicBrainz ingest failed for artist={artist.name}",
            action=MusicReleaseIngestPipeline(db).run_for_artist(
                artist_name=artist.name,
                musicbrainz_artist_id=artist.musicbrainz_artist_id,
            ),
        )

    return artist


@router.get("/artists", response_model=list[MusicArtistRead])
def list_artists(db: Session = Depends(get_db)):
    return MusicArtistService(db).list_active()


@router.get("/releases", response_model=list[MusicReleaseRead])
def list_releases(
    start: date,
    end: date,
    db: Session = Depends(get_db),
):
    return MusicReleaseService(db).list_between(start=start, end=end)