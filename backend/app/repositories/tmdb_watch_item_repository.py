from app.models.tmdb_watch_item import TmdbWatchItem


class TmdbWatchItemRepository:
    def __init__(self, db):
        self.db = db

    def get_by_kind_and_tmdb_id(
        self,
        kind: str,
        tmdb_id: int,
    ) -> TmdbWatchItem | None:
        return (
            self.db.query(TmdbWatchItem)
            .filter(
                TmdbWatchItem.kind == kind,
                TmdbWatchItem.tmdb_id == tmdb_id,
            )
            .first()
        )

    def list_active(self) -> list[TmdbWatchItem]:
        return (
            self.db.query(TmdbWatchItem)
            .filter(TmdbWatchItem.is_active == True)
            .order_by(TmdbWatchItem.kind.asc(), TmdbWatchItem.name.asc())
            .all()
        )

    def upsert(self, item: TmdbWatchItem) -> TmdbWatchItem:
        existing = self.get_by_kind_and_tmdb_id(
            kind=item.kind,
            tmdb_id=item.tmdb_id,
        )

        if existing:
            existing.name = item.name
            existing.is_active = True
            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item