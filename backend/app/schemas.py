from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =========================================================
# AUTH
# =========================================================

class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# EVENTS
# =========================================================

class EventCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200
    )

    description: str

    category: str

    location: str

    event_date: datetime

    ticket_price: float = Field(
        ge=0
    )

    banner_image: Optional[str] = None

    total_tickets: int = Field(
        default=100,
        gt=0
    )


class EventUpdate(BaseModel):
    """
    All fields are optional.
    The organizer can update only the fields
    that need to be changed.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    description: Optional[str] = None

    category: Optional[str] = None

    location: Optional[str] = None

    event_date: Optional[datetime] = None

    ticket_price: Optional[float] = Field(
        default=None,
        ge=0
    )

    banner_image: Optional[str] = None

    total_tickets: Optional[int] = Field(
        default=None,
        gt=0
    )


class EventResponse(BaseModel):
    id: int

    title: str

    description: str

    category: str

    location: str

    event_date: datetime

    ticket_price: float

    banner_image: Optional[str]

    total_tickets: int

    available_tickets: int

    # Phase 2 - RBAC / Organizer Management
    organizer_id: int

    # UPCOMING / ONGOING / COMPLETED / CANCELLED
    event_status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# BOOKINGS
# =========================================================

class BookingCreate(BaseModel):
    event_id: int

    ticket_quantity: int = Field(
        gt=0,
        le=10
    )


class BookingResponse(BaseModel):
    id: int

    user_id: int

    event_id: int

    ticket_quantity: int

    total_price: float

    booking_status: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# TICKETS
# =========================================================

class TicketResponse(BaseModel):
    id: int

    booking_id: int

    ticket_code: str

    qr_code_url: Optional[str]

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

class NotificationResponse(BaseModel):
    id: int

    user_id: int

    title: str

    message: str

    type: str

    is_read: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# MODULE 9 - ORGANIZER ANALYTICS
# =========================================================

class OrganizerEventAnalytics(BaseModel):
    """
    Analytics for one event owned by the organizer.
    """

    event_id: int

    event_title: str

    total_tickets: int

    tickets_sold: int

    remaining_tickets: int

    total_revenue: float

    booking_count: int


# =========================================================
# MODULE 11 - ADMIN ANALYTICS
# =========================================================

class AdminAnalyticsResponse(BaseModel):
    """
    Overall platform analytics available to ADMIN.
    """

    total_users: int

    total_events: int

    total_tickets_sold: int

    total_bookings: int

    platform_revenue: float