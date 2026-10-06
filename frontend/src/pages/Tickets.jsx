import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    axios
      .get(`${API_URL}/api/v1/tickets/my`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setTickets(response.data);
      })
      .catch((err) => {
        setError(
          err.response?.data?.detail ||
          "Unable to load tickets."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="content-page">

      <h1>My Tickets</h1>

      {loading && (
        <p className="center-text">
          Loading tickets...
        </p>
      )}

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {!loading && tickets.length === 0 && (
        <div className="empty-card">
          <p>No tickets found.</p>
        </div>
      )}

      <div className="ticket-grid">

        {tickets.map((ticket) => (
          <div
            className="ticket-card"
            key={ticket.id}
          >
            <h3>🎟️ Ticket</h3>

            <p>
              <strong>Ticket ID:</strong>{" "}
              {ticket.id}
            </p>

            <p>
              <strong>Booking ID:</strong>{" "}
              {ticket.booking_id}
            </p>

            <p className="ticket-code">
              {ticket.ticket_code}
            </p>

            {ticket.qr_code_url && (
              <img
                src={`${API_URL}${ticket.qr_code_url}`}
                alt="Ticket QR Code"
                className="qr-image"
              />
            )}

            <p>
              Created:{" "}
              {new Date(
                ticket.created_at
              ).toLocaleString()}
            </p>
          </div>
        ))}

      </div>
    </div>
  );
}

export default Tickets;