import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");

  const token = localStorage.getItem("token");

  const loadNotifications = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/api/v1/notifications/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setNotifications(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to load notifications."
      );
    }
  };

  useEffect(() => {
    loadNotifications();
  }, []);

  const markAsRead = async (id) => {
    try {
      await axios.patch(
        `${API_URL}/api/v1/notifications/${id}/read`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      loadNotifications();
    } catch (err) {
      setError("Unable to mark notification as read.");
    }
  };

  return (
    <div className="content-page">

      <h1>Notifications</h1>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {notifications.length === 0 ? (
        <div className="empty-card">
          <p>No notifications.</p>
        </div>
      ) : (
        <div className="notification-list">

          {notifications.map((notification) => (
            <div
              className={`notification-card ${
                notification.is_read
                  ? "read"
                  : "unread"
              }`}
              key={notification.id}
            >

              <div>
                <h3>{notification.title}</h3>

                <p>
                  {notification.message}
                </p>

                <small>
                  {new Date(
                    notification.created_at
                  ).toLocaleString()}
                </small>
              </div>

              {!notification.is_read && (
                <button
                  onClick={() =>
                    markAsRead(notification.id)
                  }
                >
                  Mark as read
                </button>
              )}

            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default Notifications;