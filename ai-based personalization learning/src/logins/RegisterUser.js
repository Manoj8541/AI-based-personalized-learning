import axios from "axios";
import "./commonAuth.css";
import { useNavigate } from "react-router-dom";

export default function RegisterUser() {
  const navigate = useNavigate();

  const register = () => {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // ✅ validation
    if (!name || !email || !password || !confirmPassword) {
      alert("All fields are required");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    axios.post("http://localhost:5000/api/admin/users", {
      name,
      email,
      password,
    })
    .then(() => {
      alert("Account created successfully");
      navigate("/login");
    })
    .catch(() => alert("User already exists"));
  };

  return (
    <div className="auth-wrapper fade">
      <h2>Create Account</h2>

      {/* ✅ ADD NAME */}
      <input
        id="name"
        placeholder="Full Name"
        required
      />

      <input
        id="email"
        placeholder="Email"
        required
      />

      <input
        id="password"
        type="password"
        placeholder="Password"
        required
      />

      {/* ✅ ADD CONFIRM PASSWORD */}
      <input
        id="confirmPassword"
        type="password"
        placeholder="Confirm Password"
        required
      />

      <button className="glow-btn" onClick={register}>
        Register
      </button>
    </div>
  );
}
