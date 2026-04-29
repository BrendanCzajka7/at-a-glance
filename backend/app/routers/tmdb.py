from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.external.tmdb_client import TmdbClient
from app.pipelines.ingest_tmdb_movies import TmdbMovieIngestPipeline
from app.schemas.tmdb import (
    TmdbDirectorSearchResult,
    TmdbGenreSearchResult,
    TmdbMovieReleaseRead,
    TmdbWatchItemRead,
)
from app.services.tmdb_movie_release_service import TmdbMovieReleaseService
from app.services.tmdb_watch_item_service import TmdbWatchItemService


router = APIRouter(prefix="/api/tmdb", tags=["tmdb"])


@router.get("/genre-search", response_model=list[TmdbGenreSearchResult])
async def search_genres():
    client = TmdbClient()
    genres = await client.list_movie_genres()

    return [
        TmdbGenreSearchResult(
            tmdb_id=genre["id"],
            name=genre["name"],
        )
        for genre in genres
    ]


@router.get("/director-search", response_model=list[TmdbDirectorSearchResult])
async def search_directors(name: str = Query(...)):
    client = TmdbClient()
    directors = await client.search_directors(name)

    return [
        TmdbDirectorSearchResult(
            tmdb_id=director["id"],
            name=director["name"],
            known_for_department=director.get("known_for_department"),
            profile_path=director.get("profile_path"),
            popularity=director.get("popularity"),
        )
        for director in directors
    ]


@router.post("/watch-items", response_model=TmdbWatchItemRead)
async def add_watch_item(
    kind: str = Query(...),
    tmdb_id: int = Query(...),
    name: str = Query(...),
    ingest_now: bool = Query(default=True),
    db: Session = Depends(get_db),
):
    item = TmdbWatchItemService(db).create_or_update(
        kind=kind,
        tmdb_id=tmdb_id,
        name=name,
    )

    if ingest_now:
        await TmdbMovieIngestPipeline(db).run_for_watch_item(
            kind=item.kind,
            tmdb_id=item.tmdb_id,
            name=item.name,
        )

    return item


@router.get("/watch-items", response_model=list[TmdbWatchItemRead])
def list_watch_items(db: Session = Depends(get_db)):
    return TmdbWatchItemService(db).list_active()


@router.get("/movie-releases", response_model=list[TmdbMovieReleaseRead])
def list_movie_releases(
    start: date,
    end: date,
    db: Session = Depends(get_db),
):
    return TmdbMovieReleaseService(db).list_between(start=start, end=end)