from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.dependencies import require_role
from app.models import Event, Booking, User
from app.schemas import OrganizerEventAnalytics


router = APIRouter(
    prefix="/api/v1/organizer",
    tags=["Organizer Analytics"]
)


# =========================================================
# EVENT ANALYTICS
# =========================================================

@router.get(
    "/events/{event_id}/analytics",
    response_model=OrganizerEventAnalytics
)
def get_event_analytics(
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

    # Ownership check
    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only view analytics for your own events"
        )

    booking_stats = (
        db.query(
            func.coalesce(
                func.sum(Booking.ticket_quantity),
                0
            ).label("tickets_sold"),

            func.coalesce(
                func.sum(Booking.total_price),
                0
            ).label("total_revenue"),

            func.count(
                Booking.id
            ).label("booking_count")
        )
        .filter(
            Booking.event_id == event_id,
            Booking.booking_status == "CONFIRMED"
        )
        .first()
    )

    tickets_sold = int(
        booking_stats.tickets_sold or 0
    )

    total_revenue = float(
        booking_stats.total_revenue or 0
    )

    booking_count = int(
        booking_stats.booking_count or 0
    )

    return OrganizerEventAnalytics(
        event_id=event.id,
        event_title=event.title,
        total_tickets=event.total_tickets,
        tickets_sold=tickets_sold,
        remaining_tickets=event.available_tickets,
        total_revenue=total_revenue,
        booking_count=booking_count
    )