import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

function NotificationDropdown() {
  const [notifications, setNotifications] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) return;

    axios
      .get(`${API_URL}/api/v1/notifications/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setNotifications(response.data);
      })
      .catch(() => {
        setNotifications([]);
      });
  }, []);

  const unreadCount = notifications.filter(
    (notification) => !notification.is_read
  ).length;

  return (
    <div className="notification-wrapper">
      <button
        className="notification-button"
        onClick={() => setOpen(!open)}
      >
        🔔
        {unreadCount > 0 && (
          <span className="notification-count">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="notification-menu">
          <h3>Notifications</h3>

          {notifications.length === 0 ? (
            <p>No notifications</p>
          ) : (
            notifications.slice(0, 5).map((item) => (
              <div
                key={item.id}
                className="notification-item"
              >
                <strong>{item.title}</strong>
                <p>{item.message}</p>
              </div>
            ))
          )}

          <Link
            to="/notifications"
            onClick={() => setOpen(false)}
          >
            View all
          </Link>
        </div>
      )}
    </div>
  );
}

export default NotificationDropdown;