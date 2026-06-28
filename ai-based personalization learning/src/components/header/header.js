import { NavLink, useNavigate } from "react-router-dom";
import "./header.css";
import { Home, LogOut, CircleUser } from "lucide-react";

const Header = ({ hideHome = false }) => {
  const navigate = useNavigate();

  const isUserLoggedIn = localStorage.getItem("isLoggedIn");
  const isAdminLoggedIn = localStorage.getItem("adminEmail");

  if (!isUserLoggedIn && !isAdminLoggedIn) return null;

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <header>
      <img src="/logo.png" alt="LearnX" height={40} className="logo" />

      {/* Home only for users */}
      {!hideHome && isUserLoggedIn && (
        <NavLink to="/profile" className="Home">
          <Home size={40} strokeWidth={1} color="white" />
        </NavLink>
      )}

      {/* Logout for both */}
      <button className="Logout" onClick={handleLogout}>
        <LogOut size={40} strokeWidth={1} color="white" />
      </button>

      {/* Profile only for users */}
      {!hideHome && isUserLoggedIn && (
        <NavLink to="/profile" className="ProfileAvatar">
          <CircleUser size={45} strokeWidth={1} color="white" />
        </NavLink>
      )}
    </header>
  );
};

export default Header;
