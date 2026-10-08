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
# USER
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

    # Phase 2 - Role Based Access Control
    # Allowed roles:
    # USER
    # ORGANIZER
    # ADMIN
    role = Column(
        String(20),
        default="USER",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# EVENT
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

    event_date = Column(
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

    # =====================================================
    # PHASE 2 - ORGANIZER EVENT MANAGEMENT
    # =====================================================

    organizer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    event_status = Column(
        String(20),
        default="ACTIVE",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# BOOKING
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
        nullable=False
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    ticket_quantity = Column(
        Integer,
        nullable=False
    )

    total_price = Column(
        Float,
        nullable=False
    )

    booking_status = Column(
        String(20),
        default="CONFIRMED",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# TICKET
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
        nullable=False
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
        default=datetime.utcnow
    )


# =========================================================
# NOTIFICATION
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
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    type = Column(
        String(20),
        default="SYSTEM",
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )