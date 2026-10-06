import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function BookingHistory() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    axios
      .get(`${API_URL}/api/v1/bookings/my`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setBookings(response.data);
      })
      .catch((err) => {
        setError(
          err.response?.data?.detail ||
          "Unable to load bookings."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="content-page">

      <h1>My Bookings</h1>

      {loading && (
        <p className="center-text">
          Loading bookings...
        </p>
      )}

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {!loading && bookings.length === 0 && (
        <div className="empty-card">
          <p>You don't have any bookings yet.</p>

          <Link
            to="/"
            className="primary-button"
          >
            Explore Events
          </Link>
        </div>
      )}

      <div className="booking-list">

        {bookings.map((booking) => (
          <div
            className="booking-card"
            key={booking.id}
          >
            <h3>
              Booking #{booking.id}
            </h3>

            <p>
              Event ID: {booking.event_id}
            </p>

            <p>
              Tickets: {booking.ticket_quantity}
            </p>

            <p>
              Total: ₹{booking.total_price}
            </p>

            <p>
              Status: {booking.booking_status}
            </p>

            <p>
              {new Date(
                booking.created_at
              ).toLocaleString()}
            </p>
          </div>
        ))}

      </div>
    </div>
  );
}

export default BookingHistory;