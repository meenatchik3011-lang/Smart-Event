import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function EventDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [event, setEvent] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [booking, setBooking] = useState(false);

  useEffect(() => {
    axios
      .get(`${API_URL}/api/v1/events/${id}`)
      .then((response) => {
        setEvent(response.data);
      })
      .catch(() => {
        setError("Event not found.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  const handleBooking = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    try {
      setBooking(true);
      setError("");

      const response = await axios.post(
        `${API_URL}/api/v1/bookings/`,
        {
          event_id: Number(id),
          ticket_quantity: Number(quantity),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      navigate("/booking-confirmation", {
        state: {
          booking: response.data,
        },
      });

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Booking failed."
      );
    } finally {
      setBooking(false);
    }
  };

  if (loading) {
    return <p className="center-text">Loading...</p>;
  }

  if (!event) {
    return (
      <p className="error-message">
        {error || "Event not found."}
      </p>
    );
  }

  return (
    <div className="details-page">

      <div className="details-card">

        {event.banner_image && (
          <img
            src={event.banner_image}
            alt={event.title}
          />
        )}

        <div className="details-content">

          <span className="category">
            {event.category}
          </span>

          <h1>{event.title}</h1>

          <p>{event.description}</p>

          <p>
            📍 <strong>Location:</strong>{" "}
            {event.location}
          </p>

          <p>
            📅 <strong>Date:</strong>{" "}
            {new Date(
              event.event_date
            ).toLocaleString()}
          </p>

          <p>
            💰 <strong>Price:</strong>{" "}
            ₹{event.ticket_price}
          </p>

          <p>
            🎟️ <strong>Available:</strong>{" "}
            {event.available_tickets}
          </p>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="booking-box">

            <label>Number of Tickets</label>

            <input
              type="number"
              min="1"
              max={Math.min(
                10,
                event.available_tickets
              )}
              value={quantity}
              onChange={(e) =>
                setQuantity(
                  Math.max(
                    1,
                    Number(e.target.value)
                  )
                )
              }
            />

            <p className="total">
              Total: ₹
              {(
                event.ticket_price * quantity
              ).toFixed(2)}
            </p>

            <button
              className="primary-button"
              onClick={handleBooking}
              disabled={booking}
            >
              {booking
                ? "Booking..."
                : "Book Tickets"}
            </button>

          </div>

        </div>
      </div>
    </div>
  );
}

export default EventDetails;