import { Link, useLocation } from "react-router-dom";

function BookingConfirmation() {
  const location = useLocation();
  const booking = location.state?.booking;

  return (
    <div className="confirmation-page">

      <div className="confirmation-card">

        <div className="success-icon">
          ✓
        </div>

        <h1>Booking Confirmed!</h1>

        {booking ? (
          <>
            <p>
              Your booking has been successfully created.
            </p>

            <div className="booking-info">
              <p>
                <strong>Booking ID:</strong>{" "}
                {booking.id}
              </p>

              <p>
                <strong>Event ID:</strong>{" "}
                {booking.event_id}
              </p>

              <p>
                <strong>Tickets:</strong>{" "}
                {booking.ticket_quantity}
              </p>

              <p>
                <strong>Total:</strong>{" "}
                ₹{booking.total_price}
              </p>

              <p>
                <strong>Status:</strong>{" "}
                {booking.booking_status}
              </p>
            </div>
          </>
        ) : (
          <p>
            Your booking was completed successfully.
          </p>
        )}

        <Link
          to="/bookings"
          className="primary-button"
        >
          View My Bookings
        </Link>

      </div>
    </div>
  );
}

export default BookingConfirmation;