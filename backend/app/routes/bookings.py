
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Booking, Event, Notification, User
from app.schemas import BookingCreate, BookingResponse


router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"],
)


def get_current_utc_time():
    """Return the current UTC time without timezone information."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def refresh_event_status(event: Event) -> None:
    """Update an event's status based on its start and end dates."""
    if event.event_status == "CANCELLED":
        return

    now = get_current_utc_time()

    # Handle older records that may not have an end date.
    if event.event_end_date is None:
        if now < event.event_date:
            event.event_status = "UPCOMING"
        else:
            event.event_status = "ONGOING"
        return

    if now < event.event_date:
        event.event_status = "UPCOMING"
    elif now < event.event_end_date:
        event.event_status = "ONGOING"
    else:
        event.event_status = "COMPLETED"


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    request: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Validate the requested ticket quantity.
    if request.ticket_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket quantity must be greater than zero.",
        )

    # Find the event.
    event = (
        db.query(Event)
        .filter(Event.id == request.event_id)
        .with_for_update()
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )

    # Refresh the event status before allowing a booking.
    refresh_event_status(event)

    if event.event_status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This event has been cancelled.",
        )

    if event.event_status == "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bookings are not available for completed events.",
        )

    if event.available_tickets < request.ticket_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough tickets available.",
        )

    # Calculate the total booking price.
    total_price = event.ticket_price * request.ticket_quantity

    try:
        # Create the booking.
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            ticket_quantity=request.ticket_quantity,
            total_price=total_price,
            booking_status="CONFIRMED",
        )

        # Reserve tickets.
        event.available_tickets -= request.ticket_quantity

        db.add(booking)
        db.flush()

        # Notify the user about the confirmed booking.
        notification = Notification(
            user_id=current_user.id,
            title="Booking Confirmed",
            message=(
                f"Your booking for '{event.title}' has been confirmed. "
                f"Tickets booked: {request.ticket_quantity}. "
                f"Total amount: {total_price:.2f}."
            ),
            type="BOOKING",
            is_read=False,
        )

        db.add(notification)
        db.commit()
        db.refresh(booking)

        return booking

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Booking could not be completed. Please try again.",
        )


@router.get(
    "/my",
    response_model=list[BookingResponse],
)
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return bookings belonging to the currently logged-in user."""
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )

    return bookings
