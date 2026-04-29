from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.pipeline_logging import run_logged_pipeline
from app.pipelines.ingest_ticketmaster_concerts import (
    TicketmasterConcertIngestPipeline,
)
from app.schemas.ticketmaster import TicketmasterConcertRead
from app.services.ticketmaster_concert_service import TicketmasterConcertService

router = APIRouter(prefix="/api/ticketmaster", tags=["ticketmaster"])


@router.post("/ingest-concerts", response_model=list[TicketmasterConcertRead])
async def ingest_concerts_for_location(
    location_key: str = Query(default="okaloosa_island"),
    radius_miles: int = Query(default=75, ge=1, le=250),
    db: Session = Depends(get_db),
):
    pipeline = TicketmasterConcertIngestPipeline(db)

    return await run_logged_pipeline(
        db=db,
        source="ticketmaster",
        event_type="ingest_ticketmaster_concerts_failed",
        message=(
            "Ticketmaster concert ingest failed "
            f"for location_key={location_key}, radius_miles={radius_miles}"
        ),
        action=pipeline.run_for_location(
            location_key=location_key,
            radius_miles=radius_miles,
        ),
    )


@router.get("/concerts", response_model=list[TicketmasterConcertRead])
def list_concerts(
    location_key: str = Query(default="okaloosa_island"),
    start: date = Query(...),
    end: date = Query(...),
    db: Session = Depends(get_db),
):
    return TicketmasterConcertService(db).list_between(
        location_key=location_key,
        start=start,
        end=end,
    )