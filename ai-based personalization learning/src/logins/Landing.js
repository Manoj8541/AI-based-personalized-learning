import "./commonAuth.css";
import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="auth-wrapper fade">
      <img src="/logo.png" className="logo" alt="LearnX" />
      <h1>Welcome!!</h1>

      <button className="glow-btn" onClick={() => navigate("/login")}>
        User Login
      </button>

      <button className="glow-btn" onClick={() => navigate("/admin-login")}>
        Admin Login
      </button>

      <p className="link" onClick={() => navigate("/register")}>
        New User? Create Account
      </p>
    </div>
  );
}
