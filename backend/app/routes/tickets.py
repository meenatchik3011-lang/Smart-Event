import os
import uuid

import qrcode
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Booking, Ticket, User
from app.schemas import TicketResponse


router = APIRouter(
    prefix="/api/v1/tickets",
    tags=["Tickets"]
)


# =========================================================
# QR CODE FOLDER
# =========================================================

# Project backend directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# backend/static/qr
QR_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "qr"
)

# Create folder if it doesn't exist
os.makedirs(QR_FOLDER, exist_ok=True)


# =========================================================
# GENERATE TICKET
# =========================================================

@router.post(
    "/booking/{booking_id}",
    response_model=TicketResponse
)
def generate_ticket(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find booking belonging to logged-in user
    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id,
            Booking.user_id == current_user.id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    # Check if ticket already exists
    existing_ticket = (
        db.query(Ticket)
        .filter(
            Ticket.booking_id == booking.id
        )
        .first()
    )

    if existing_ticket:
        return existing_ticket

    # Generate unique ticket code
    ticket_code = str(uuid.uuid4())

    # Generate QR code
    qr = qrcode.make(ticket_code)

    # QR image filename
    filename = f"{ticket_code}.png"

    # Full file path
    filepath = os.path.join(
        QR_FOLDER,
        filename
    )

    # Save QR image
    qr.save(filepath)

    # Create ticket database record
    ticket = Ticket(
        booking_id=booking.id,
        ticket_code=ticket_code,
        qr_code_url=f"/static/qr/{filename}"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


# =========================================================
# GET MY TICKETS
# =========================================================

@router.get(
    "/my",
    response_model=list[TicketResponse]
)
def get_my_tickets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    tickets = (
        db.query(Ticket)
        .join(
            Booking,
            Ticket.booking_id == Booking.id
        )
        .filter(
            Booking.user_id == current_user.id
        )
        .all()
    )

    return tickets