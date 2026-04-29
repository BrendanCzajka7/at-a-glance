from app.models.tmdb_watch_item import TmdbWatchItem
from app.repositories.tmdb_watch_item_repository import TmdbWatchItemRepository


VALID_TMDB_WATCH_KINDS = {"genre", "director"}


class TmdbWatchItemService:
    def __init__(self, db):
        self.repo = TmdbWatchItemRepository(db)

    def create_or_update(
        self,
        kind: str,
        tmdb_id: int,
        name: str,
    ) -> TmdbWatchItem:
        if kind not in VALID_TMDB_WATCH_KINDS:
            raise ValueError(f"Unsupported TMDB watch kind: {kind}")

        return self.repo.upsert(
            TmdbWatchItem(
                kind=kind,
                tmdb_id=tmdb_id,
                name=name,
                is_active=True,
            )
        )

    def list_active(self) -> list[TmdbWatchItem]:
        return self.repo.list_active()