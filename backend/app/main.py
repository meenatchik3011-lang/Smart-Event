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
)


# =========================================================
# DATABASE
# =========================================================

# Create all database tables
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

# Create folders if they don't exist
os.makedirs(QR_FOLDER, exist_ok=True)


# Serve /static files
app.mount(
    "/static",
    StaticFiles(directory=STATIC_FOLDER),
    name="static",
)


# =========================================================
# API ROUTES
# =========================================================

app.include_router(auth.router)

app.include_router(events.router)

app.include_router(bookings.router)

app.include_router(tickets.router)

app.include_router(notifications.router)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to SmartEvent API",
        "status": "running",
    }