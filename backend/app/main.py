import os

import app.models

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

from app.routes import (
    auth,
    bookings,
    events,
    notifications,
    tickets,
    organizer,
    admin,
)


# =========================================================
# DATABASE
# =========================================================

# Create database tables
Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="SmartEvent API",
    description="Event Discovery & Ticket Booking System",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# STATIC FILES
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

STATIC_FOLDER = os.path.join(
    BASE_DIR,
    "static"
)

QR_FOLDER = os.path.join(
    STATIC_FOLDER,
    "qr"
)


# Create static/qr folder if it doesn't exist
os.makedirs(QR_FOLDER, exist_ok=True)


# Serve static files
app.mount(
    "/static",
    StaticFiles(directory=STATIC_FOLDER),
    name="static",
)


# =========================================================
# API ROUTES
# =========================================================

# Authentication
app.include_router(auth.router)

# Event discovery and management
app.include_router(events.router)

# Booking APIs
app.include_router(bookings.router)

# Ticket APIs
app.include_router(tickets.router)

# Notification APIs
app.include_router(notifications.router)

# Organizer analytics
app.include_router(organizer.router)

# Admin dashboard and analytics
app.include_router(admin.router)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to SmartEvent API",
        "status": "running",
    }