from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import (
    Booking,
    Event,
    Notification,
    User,
)
from app.schemas import BookingCreate, BookingResponse


router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"]
)


@router.post(
    "/",
    response_model=BookingResponse
)
def create_booking(
    request: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == request.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.available_tickets < request.ticket_quantity:
        raise HTTPException(
            status_code=400,
            detail="Not enough tickets available"
        )

    total_price = (
        event.ticket_price *
        request.ticket_quantity
    )

    booking = Booking(
        user_id=current_user.id,
        event_id=event.id,
        ticket_quantity=request.ticket_quantity,
        total_price=total_price,
        booking_status="CONFIRMED"
    )

    event.available_tickets -= request.ticket_quantity

    db.add(booking)
    db.flush()

    notification = Notification(
        user_id=current_user.id,
        title="Booking Confirmed",
        message=(
            f"Your booking for {event.title} "
            "has been confirmed."
        ),
        type="BOOKING"
    )

    db.add(notification)

    db.commit()
    db.refresh(booking)

    return booking


@router.get(
    "/my",
    response_model=list[BookingResponse]
)
def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(
        Booking.created_at.desc()
    ).all()