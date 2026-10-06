from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =========================
# AUTH
# =========================

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


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
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# EVENTS
# =========================

class EventCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str
    category: str
    location: str
    event_date: datetime
    ticket_price: float = Field(ge=0)
    banner_image: Optional[str] = None
    total_tickets: int = Field(default=100, gt=0)


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
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# BOOKINGS
# =========================

class BookingCreate(BaseModel):
    event_id: int
    ticket_quantity: int = Field(gt=0, le=10)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    ticket_quantity: int
    total_price: float
    booking_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# TICKETS
# =========================

class TicketResponse(BaseModel):
    id: int
    booking_id: int
    ticket_code: str
    qr_code_url: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# NOTIFICATIONS
# =========================

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)