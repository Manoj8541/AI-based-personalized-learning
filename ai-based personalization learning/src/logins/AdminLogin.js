import axios from "axios";
import "./commonAuth.css";
import { useNavigate } from "react-router-dom";

export default function AdminLogin() {
  const nav = useNavigate();

  const login = () => {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    axios
      .post("http://localhost:5000/api/admin/login", {
        email,
        password,
      })
      .then(() => {
        // ✅ STORE ADMIN SESSION (THIS WAS MISSING)
        localStorage.setItem("adminEmail", email);

        // ❌ DO NOT set isLoggedIn for admin
        // localStorage.setItem("isLoggedIn", true); ❌

        nav("/admin");
      })
      .catch(() => alert("Invalid Admin Credentials"));
  };

  return (
    <div className="auth-wrapper fade">
      <h2>Admin Login</h2>
      <input id="email" placeholder="Admin ID" required />
      <input id="password" type="password" placeholder="Password" required />
      <button className="glow-btn" onClick={login}>Login</button>
    </div>
  );
}
