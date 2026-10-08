from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models import Event, User, Booking, Notification
from app.schemas import (
    EventCreate,
    EventResponse,
    EventUpdate,
    BookingResponse,
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/v1/events",
    tags=["Events"]
)


# =========================================================
# CREATE EVENT
# ORGANIZER / ADMIN ONLY
# =========================================================

@router.post(
    "/",
    response_model=EventResponse,
    status_code=201
)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ORGANIZER", "ADMIN")
    )
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
        available_tickets=event_data.total_tickets,

        # Phase 2
        organizer_id=current_user.id,
        event_status="UPCOMING"
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


# =========================================================
# GET ALL EVENTS
# PUBLIC
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

    # Category filter
    if category:
        query = query.filter(
            Event.category.ilike(
                f"%{category}%"
            )
        )

    # Title search
    if search:
        query = query.filter(
            Event.title.ilike(
                f"%{search}%"
            )
        )

    return (
        query
        .order_by(Event.event_date.asc())
        .all()
    )


# =========================================================
# GET ORGANIZER'S OWN EVENTS
# ORGANIZER ONLY
# =========================================================

@router.get(
    "/organizer/events",
    response_model=list[EventResponse]
)
def get_my_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ORGANIZER")
    )
):
    return (
        db.query(Event)
        .filter(
            Event.organizer_id == current_user.id
        )
        .order_by(Event.event_date.asc())
        .all()
    )


# =========================================================
# GET BOOKINGS FOR ORGANIZER EVENT
# ORGANIZER ONLY + OWN EVENT
# =========================================================

@router.get(
    "/organizer/events/{event_id}/bookings",
    response_model=list[BookingResponse]
)
def get_event_bookings(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ORGANIZER")
    )
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

    # Ownership validation
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You can only view bookings "
                "for your own events"
            )
        )

    return (
        db.query(Booking)
        .filter(
            Booking.event_id == event_id
        )
        .order_by(
            Booking.created_at.desc()
        )
        .all()
    )


# =========================================================
# UPDATE EVENT
# ORGANIZER ONLY + OWN EVENT
# =========================================================

@router.put(
    "/{event_id}",
    response_model=EventResponse
)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ORGANIZER")
    )
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

    # Ownership validation
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You can only update "
                "your own events"
            )
        )

    # Do not update a cancelled event
    if event.event_status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Cancelled events cannot be updated"
        )

    update_data = event_data.model_dump(
        exclude_unset=True
    )

    # =====================================================
    # UPDATE TOTAL TICKETS SAFELY
    # =====================================================

    if "total_tickets" in update_data:

        new_total = update_data["total_tickets"]

        tickets_sold = (
            event.total_tickets
            - event.available_tickets
        )

        if new_total < tickets_sold:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Total tickets cannot be less "
                    "than tickets already sold"
                )
            )

        event.total_tickets = new_total

        event.available_tickets = (
            new_total - tickets_sold
        )

        del update_data["total_tickets"]

    # =====================================================
    # UPDATE OTHER FIELDS
    # =====================================================

    for field, value in update_data.items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)

    return event


# =========================================================
# CANCEL EVENT
# ORGANIZER ONLY + OWN EVENT
# =========================================================

@router.patch(
    "/{event_id}/cancel",
    response_model=EventResponse
)
def cancel_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ORGANIZER")
    )
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

    # Ownership validation
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail=(
                "You can only cancel "
                "your own events"
            )
        )

    # Already cancelled
    if event.event_status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Event is already cancelled"
        )

    # Change status
    event.event_status = "CANCELLED"

    # =====================================================
    # SEND NOTIFICATION TO BOOKED USERS
    # =====================================================

    bookings = (
        db.query(Booking)
        .filter(
            Booking.event_id == event.id,
            Booking.booking_status == "CONFIRMED"
        )
        .all()
    )

    for booking in bookings:

        notification = Notification(
            user_id=booking.user_id,
            title="Event Cancelled",
            message=(
                f"The event '{event.title}' "
                "has been cancelled."
            ),
            type="EVENT",
            is_read=False
        )

        db.add(notification)

    db.commit()
    db.refresh(event)

    return event


# =========================================================
# GET EVENT BY ID
# PUBLIC
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