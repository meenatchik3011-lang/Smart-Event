import { Link, useNavigate } from "react-router-dom";
import NotificationDropdown from "./NotificationDropdown";

function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
    window.location.reload();
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">

        <Link to="/" className="logo">
          Smart<span>Event</span>
        </Link>

        <div className="nav-links">
          <Link to="/">Events</Link>

          {token ? (
            <>
              <Link to="/bookings">
                My Bookings
              </Link>

              <Link to="/tickets">
                My Tickets
              </Link>

              <NotificationDropdown />

              <button
                className="logout-button"
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">
                Login
              </Link>

              <Link
                to="/register"
                className="register-nav"
              >
                Register
              </Link>
            </>
          )}
        </div>

      </div>
    </nav>
  );
}

export default Navbar;