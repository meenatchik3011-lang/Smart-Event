import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function Home() {
  const [events, setEvents] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchEvents = async () => {
    try {
      setLoading(true);

      const response = await axios.get(
        `${API_URL}/api/v1/events/`,
        {
          params: {
            search: search || undefined,
            category: category || undefined,
          },
        }
      );

      setEvents(response.data);
      setError("");

    } catch (err) {
      setError("Unable to load events.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [category]);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchEvents();
  };

  return (
    <div className="home-page">

      <section className="hero-section">

        <h1>
          Discover Amazing Events
        </h1>

        <p>
          Find events, book tickets and enjoy unforgettable
          experiences.
        </p>

        <form
          className="search-form"
          onSubmit={handleSearch}
        >
          <input
            type="text"
            placeholder="Search events..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <button type="submit">
            Search
          </button>
        </form>

      </section>

      <section className="events-section">

        <div className="section-header">
          <h2>Upcoming Events</h2>

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="">All Categories</option>
            <option value="Music">Music</option>
            <option value="Sports">Sports</option>
            <option value="Conference">Conference</option>
            <option value="Workshop">Workshop</option>
          </select>
        </div>

        {loading && (
          <p className="center-text">
            Loading events...
          </p>
        )}

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        {!loading && events.length === 0 && (
          <p className="center-text">
            No events found.
          </p>
        )}

        <div className="event-grid">

          {events.map((event) => (
            <div
              className="event-card"
              key={event.id}
            >

              {event.banner_image && (
                <img
                  src={event.banner_image}
                  alt={event.title}
                />
              )}

              <div className="event-card-content">

                <span className="category">
                  {event.category}
                </span>

                <h3>{event.title}</h3>

                <p>
                  {event.description}
                </p>

                <p>
                  📍 {event.location}
                </p>

                <p>
                  🎟️ ₹{event.ticket_price}
                </p>

                <p>
                  Available:
                  {" "}
                  {event.available_tickets}
                </p>

                <Link
                  to={`/events/${event.id}`}
                  className="primary-button"
                >
                  View Details
                </Link>

              </div>
            </div>
          ))}

        </div>

      </section>
    </div>
  );
}

export default Home;