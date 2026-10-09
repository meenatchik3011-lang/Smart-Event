
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.database import Base


# =========================================================
# USER MODEL
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    # Allowed roles: USER, ORGANIZER, ADMIN
    role = Column(
        String(20),
        default="USER",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# =========================================================
# EVENT MODEL
# =========================================================

class Event(Base):
    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=False
    )

    category = Column(
        String(50),
        nullable=False,
        index=True
    )

    location = Column(
        String(255),
        nullable=False
    )

    # Event start date and time
    event_date = Column(
        DateTime,
        nullable=False
    )

    # Module 10: Event end date and time
    event_end_date = Column(
        DateTime,
        nullable=False
    )

    ticket_price = Column(
        Float,
        nullable=False
    )

    banner_image = Column(
        String(500),
        nullable=True
    )

    total_tickets = Column(
        Integer,
        default=100,
        nullable=False
    )

    available_tickets = Column(
        Integer,
        default=100,
        nullable=False
    )

    # Organizer who owns this event
    organizer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Event lifecycle:
    # UPCOMING, ONGOING, COMPLETED, CANCELLED
    event_status = Column(
        String(20),
        default="UPCOMING",
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# =========================================================
# BOOKING MODEL
# =========================================================

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False,
        index=True
    )

    ticket_quantity = Column(
        Integer,
        nullable=False
    )

    total_price = Column(
        Float,
        nullable=False
    )

    # Example statuses: CONFIRMED, CANCELLED
    booking_status = Column(
        String(20),
        default="CONFIRMED",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# =========================================================
# TICKET MODEL
# =========================================================

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False,
        index=True
    )

    ticket_code = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    qr_code_url = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# =========================================================
# NOTIFICATION MODEL
# =========================================================

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    # Example types: SYSTEM, EVENT
    type = Column(
        String(20),
        default="SYSTEM",
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
