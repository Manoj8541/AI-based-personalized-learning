import axios from "axios";
import "./commonAuth.css";
import { useNavigate } from "react-router-dom";

export default function UserLogin() {
  const navigate = useNavigate();

  const login = () => {
    axios.post("http://localhost:5000/api/user/login", {
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
    })
    .then((res) => {
      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("userName", res.data.name);
      navigate("/profile");   
    })
    .catch(() => alert("Invalid email or password"));
  };

  return (
    <div className="auth-wrapper fade">
      <h2>User Login</h2>
      <input id="email" placeholder="Enter your Email" required/>
      <input id="password" type="password" placeholder="Enter Password" min={3} required/>
      <button className="glow-btn" onClick={login}>Login</button>
    </div>
  );
}
