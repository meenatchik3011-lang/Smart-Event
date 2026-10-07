# SmartEvent – Event Discovery & Ticket Booking System

SmartEvent is a full-stack event discovery and ticket booking application built using **FastAPI** for the backend and **React + Vite** for the frontend.

The application allows users to register and log in securely, discover events, search and filter events, book tickets, view booking history, receive digital QR tickets, and manage notifications.

---

## Project Overview

SmartEvent simulates a real-world event booking platform where users can:

- Create an account
- Login using JWT authentication
- Browse available events
- Search events by title
- Filter events by category
- View event details
- Book event tickets
- View booking history
- Generate digital QR tickets
- View and download QR tickets
- Receive booking notifications
- Mark notifications as read

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- bcrypt
- QRCode
- Uvicorn

## Frontend

- React
- Vite
- JavaScript
- Axios
- React Router DOM
- CSS

---

# Project Structure

```text
SmartEvent/
│
├── README.md
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   │
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── events.py
│   │       ├── bookings.py
│   │       ├── tickets.py
│   │       └── notifications.py
│   │
│   ├── static/
│   │   └── qr/
│   │
│   ├── requirements.txt
│   ├── .env
│   └── smartevent.db
│
└── frontend/
    │
    ├── src/
    │   │
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   |── NotificationDropdown.jsx
    │   │   └── ProtectedRoute.jsx
    │   │   
    │   │ 
    │   │
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   ├── Home.jsx
    │   │   ├── EventDetails.jsx
    │   │   ├── BookingConfirmation.jsx
    │   │   ├── BookingHistory.jsx
    │   │   ├── Tickets.jsx
    │   │   └── Notifications.jsx
    │   │
    │   ├── api.js
    │   ├── App.jsx
    │   └── main.jsx
    │   
    │
    ├── package.json
    └── vite.config.js
```

---

# Phase 1 Modules

## Module 1 – User Authentication

The authentication module provides secure user account management.

### Features

- User registration
- User login
- Password hashing using bcrypt
- JWT token generation
- Protected API routes
- User profile API
- Token storage in browser localStorage
- Automatic JWT attachment using Axios

### User Fields

```text
id
username
email
hashed_password
created_at
```

### Authentication APIs

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/profile
```

---

# Module 2 – Event Discovery System

Users can browse and discover available events.

### Event Fields

```text
id
title
description
category
location
event_date
ticket_price
banner_image
total_tickets
available_tickets
created_at
```

### Supported Categories

```text
Music
Tech
Sports
Business
```

### Features

- Event listing
- Event details
- Search by title
- Category filtering
- Event date
- Location
- Ticket price
- Available ticket count
- Event banner images

### Event APIs

```text
POST /api/v1/events/
GET /api/v1/events/
GET /api/v1/events/{event_id}
```

Search example:

```text
GET /api/v1/events/?search=Tech
```

Category example:

```text
GET /api/v1/events/?category=Music
```

---

# Module 3 – Ticket Booking System

Users can book tickets for available events.

### Booking Fields

```text
id
user_id
event_id
ticket_quantity
total_price
booking_status
created_at
```

### Booking Status

```text
PENDING
CONFIRMED
CANCELLED
```

### Features

- Ticket quantity selection
- Automatic total price calculation
- Ticket availability validation
- Sold-out prevention
- Booking ownership
- Booking history
- Booking confirmation

### Booking APIs

```text
POST /api/v1/bookings/
GET  /api/v1/bookings/my
```

Example booking request:

```json
{
  "event_id": 1,
  "ticket_quantity": 2
}
```

If the ticket price is ₹999:

```text
999 × 2 = ₹1998
```

---

# Module 4 – QR Code Ticket System

Each confirmed booking can have a unique digital ticket.

### Ticket Fields

```text
id
booking_id
ticket_code
qr_code_url
created_at
```

### Features

- Unique ticket code
- QR code generation
- QR image storage
- Digital ticket display
- QR ticket download
- User ticket listing

### Ticket APIs

```text
POST /api/v1/tickets/booking/{booking_id}
GET  /api/v1/tickets/my
```

QR codes are stored inside:

```text
backend/static/qr/
```

---

# Module 5 – Event Notifications

Users receive notifications related to their bookings and events.

### Notification Fields

```text
id
user_id
title
message
type
is_read
created_at
```

### Notification Types

```text
EVENT
BOOKING
SYSTEM
```

### Features

- Booking confirmation notification
- Notification list
- Unread notification indicator
- Mark notification as read
- Notification dropdown
- Notifications page

### Notification APIs

```text
GET   /api/v1/notifications/
PATCH /api/v1/notifications/{notification_id}/read
```

---

# Module 6 – React Frontend

The React frontend provides a responsive user interface for the SmartEvent application.

### Pages

```text
Register Page
Login Page
Home Page
Event Details Page
Booking Confirmation Page
Booking History Page
Tickets Page
Notifications Page
```

### Components

```text
Navbar
EventCard
TicketCard
NotificationDropdown
ProtectedRoute
```

### Frontend Features

- React Router navigation
- Axios API integration
- JWT localStorage
- Protected routes
- Event search
- Category filters
- Ticket quantity selector
- Booking confirmation
- Booking history
- QR ticket display
- Notification dropdown
- Responsive design
- Loading states
- Error handling

---

# Database

SmartEvent currently uses SQLite for development.

Database:

```text
smartevent.db
```

## Database Tables

### Users

```text
users
├── id
├── username
├── email
├── hashed_password
└── created_at
```

### Events

```text
events
├── id
├── title
├── description
├── category
├── location
├── event_date
├── ticket_price
├── banner_image
├── total_tickets
├── available_tickets
└── created_at
```

### Bookings

```text
bookings
├── id
├── user_id
├── event_id
├── ticket_quantity
├── total_price
├── booking_status
└── created_at
```

### Tickets

```text
tickets
├── id
├── booking_id
├── ticket_code
├── qr_code_url
└── created_at
```

### Notifications

```text
notifications
├── id
├── user_id
├── title
├── message
├── type
├── is_read
└── created_at
```

---

# Backend Setup

## 1. Navigate to Backend

```powershell
cd SmartEvent/backend
```

## 2. Create Virtual Environment

```powershell
python -m venv venv
```

## 3. Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\activate
```

You should see:

```text
(venv)
```

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Environment Configuration

Create:

```text
backend/.env
```

Example:

```env
APP_NAME=SmartEvent
DATABASE_URL=sqlite:///./smartevent.db
SECRET_KEY=change-this-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

For production, use a strong randomly generated secret key.

---

# Run Backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

# Swagger Documentation

FastAPI automatically provides Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

Available API groups:

```text
Authentication
Events
Bookings
Tickets
Notifications
```

---

# Swagger Testing Flow

The recommended API testing order is:

```text
1. Register
      ↓
2. Login
      ↓
3. Copy JWT token
      ↓
4. Authorize Swagger
      ↓
5. Test Profile
      ↓
6. Test Events
      ↓
7. Test Event Search
      ↓
8. Test Category Filter
      ↓
9. Book Tickets
      ↓
10. View Booking History
      ↓
11. Generate QR Ticket
      ↓
12. View Tickets
      ↓
13. View Notifications
      ↓
14. Mark Notification as Read
```

---

# Frontend Setup

Open another terminal.

Navigate to:

```powershell
cd SmartEvent/frontend
```

Install dependencies:

```powershell
npm install
```

Install required packages:

```powershell
npm install axios react-router-dom
```

---

# Run Frontend

```powershell
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

# Frontend to Backend Connection

Axios is configured in:

```text
frontend/src/api.js
```

Backend API URL:

```text
http://127.0.0.1:8000/api/v1
```

JWT tokens are stored in:

```text
localStorage
```

The Axios interceptor automatically sends:

```text
Authorization: Bearer <JWT_TOKEN>
```

for authenticated requests.

---

# Complete User Workflow

```text
                    SmartEvent
                        │
                        ▼
                 Create Account
                        │
                        ▼
                      Login
                        │
                        ▼
                   JWT Token
                        │
                        ▼
                  Event Home Page
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
           Search              Category
              │                   │
              └─────────┬─────────┘
                        ▼
                  Event Details
                        │
                        ▼
                 Select Quantity
                        │
                        ▼
                  Book Tickets
                        │
                        ▼
               Booking Confirmation
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        Booking History        QR Ticket
                                  │
                                  ▼
                             Digital Ticket
                                  │
                                  ▼
                             QR Code
                                  │
                                  ▼
                           Notifications
```

---

# Security

SmartEvent implements the following security features:

- JWT authentication
- Password hashing with bcrypt
- Protected booking routes
- Protected ticket routes
- Protected notification routes
- Booking ownership validation
- Pydantic request validation
- Environment-based configuration
- Token-based API authorization
- Unique ticket codes

---

# API Authentication

Protected endpoints require a JWT token.

Example:

```text
Authorization: Bearer <access_token>
```

Swagger can be authorized using the **Authorize** button.

---

# Error Handling

The application handles common errors such as:

```text
Invalid email or password
Email already registered
Username already exists
User not found
Event not found
Booking not found
Not enough tickets available
Invalid JWT token
Expired JWT token
Notification not found
```

---

# Current Development Status

## Completed

- [x] FastAPI backend setup
- [x] SQLite database
- [x] User model
- [x] Event model
- [x] Booking model
- [x] Ticket model
- [x] Notification model
- [x] User registration
- [x] User login
- [x] Password hashing
- [x] JWT authentication
- [x] Protected APIs
- [x] User profile API
- [x] Event listing
- [x] Event search
- [x] Category filtering
- [x] Event details
- [x] Ticket booking
- [x] Automatic price calculation
- [x] Ticket availability validation
- [x] Booking history
- [x] QR ticket generation
- [x] User tickets API
- [x] Booking notifications
- [x] Notification listing
- [x] Mark notification as read
- [x] React + Vite frontend
- [x] React routing
- [x] Login page
- [x] Register page
- [x] Home page
- [x] Event cards
- [x] Event details page
- [x] Booking confirmation page
- [x] Booking history page
- [x] Tickets page
- [x] Notifications page
- [x] Protected routes
- [x] Axios integration
- [x] Responsive UI

---

# Future Enhancements

The following features can be added in future development:

- [ ] Admin dashboard
- [ ] Event creation and management
- [ ] Event update/delete
- [ ] Event image upload
- [ ] Advanced event search
- [ ] Booking cancellation
- [ ] QR ticket verification
- [ ] Event reminder scheduler
- [ ] Email notifications
- [ ] Payment gateway integration
- [ ] PostgreSQL database
- [ ] Redis caching
- [ ] Production deployment
- [ ] Automated testing
- [ ] CI/CD pipeline

---

# Testing

Backend tests can be executed using:

```powershell
pytest
```

Coverage:

```powershell
pytest --cov=app
```

Frontend can be manually tested through:

```text
http://localhost:5173
```

API testing:

```text
http://127.0.0.1:8000/docs
```

---

# Running the Complete Project

Two terminals are required.

## Terminal 1 – Backend

```powershell
cd SmartEvent/backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

## Terminal 2 – Frontend

```powershell
cd SmartEvent/frontend
npm run dev
```

Then open:

```text
Frontend:
http://localhost:5173

Backend:
http://127.0.0.1:8000

Swagger:
http://127.0.0.1:8000/docs
```

---

# Project Goal

The goal of SmartEvent is to demonstrate a complete full-stack development workflow using:

```text
React
   ↓
Axios
   ↓
FastAPI
   ↓
JWT Authentication
   ↓
SQLAlchemy
   ↓
SQLite
```

The project demonstrates authentication, API development, database relationships, event discovery, ticket booking, QR-based digital tickets, notifications, and frontend-backend integration.

---

# Conclusion

SmartEvent provides a complete foundation for a modern event discovery and ticket booking platform.

The project combines a secure **FastAPI backend** with a responsive **React + Vite frontend**, providing users with an easy way to discover events, book tickets, manage bookings, and access digital QR tickets.

---

## Author

**SmartEvent Development Project**

**Technology:** FastAPI + React + Vite + SQLAlchemy + SQLite + JWT
