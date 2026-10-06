from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventResponse


router = APIRouter(
    prefix="/api/v1/events",
    tags=["Events"]
)


# =========================================================
# CREATE EVENT
# =========================================================

@router.post(
    "/",
    response_model=EventResponse,
    status_code=201
)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db)
):
    event = Event(
        title=event_data.title,
        description=event_data.description,
        category=event_data.category,
        location=event_data.location,
        event_date=event_data.event_date,
        ticket_price=event_data.ticket_price,
        banner_image=event_data.banner_image,
        total_tickets=event_data.total_tickets,
        available_tickets=event_data.total_tickets
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


# =========================================================
# GET ALL EVENTS
# =========================================================

@router.get(
    "/",
    response_model=list[EventResponse]
)
def get_events(
    category: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
):

    query = db.query(Event)

    # Filter by category
    if category:
        query = query.filter(
            Event.category.ilike(f"%{category}%")
        )

    # Search by title
    if search:
        query = query.filter(
            Event.title.ilike(f"%{search}%")
        )

    events = (
        query
        .order_by(Event.event_date.asc())
        .all()
    )

    return events


# =========================================================
# GET EVENT BY ID
# =========================================================

@router.get(
    "/{event_id}",
    response_model=EventResponse
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event