import axios from "axios";
import { useEffect, useState } from "react";
import "./AdminDashboard.css";
import Header from "../../components/header/header";
import { useNavigate } from "react-router-dom";

export default function AdminDashboard() {
  const navigate = useNavigate();

  const [users, setUsers] = useState([]);
  const [admins, setAdmins] = useState([]);

  const [newAdminEmail, setNewAdminEmail] = useState("");
  const [newAdminPassword, setNewAdminPassword] = useState("");

  // ✅ EDIT STATES (EMAIL + NAME)
  const [editingUserEmail, setEditingUserEmail] = useState(null);
  const [editedEmail, setEditedEmail] = useState("");
  const [editedName, setEditedName] = useState("");

  const loggedAdmin = localStorage.getItem("adminEmail");

  // ✅ ADMIN AUTH GUARD
  useEffect(() => {
    if (!localStorage.getItem("adminEmail")) {
      navigate("/admin-login");
    }
  }, [navigate]);

  // FETCH USERS
  useEffect(() => {
    axios
      .get("http://localhost:5000/api/admin/users")
      .then(res => setUsers(res.data))
      .catch(() => setUsers([]));
  }, []);

  // FETCH ADMINS
  useEffect(() => {
    axios
      .get("http://localhost:5000/api/admin/list")
      .then(res => setAdmins(res.data))
      .catch(() => setAdmins([]));
  }, []);

  // DELETE USER
  const deleteUser = (email) => {
    axios
      .delete("http://localhost:5000/api/admin/users", {
        data: { email }
      })
      .then(() => {
        setUsers(users.filter(u => u.email !== email));
      });
  };

  // ✅ UPDATE USER (NAME + EMAIL)
  const updateUser = (oldEmail) => {
    axios
      .put("http://localhost:5000/api/admin/user/update", {
        oldEmail,
        newEmail: editedEmail,
        name: editedName
      })
      .then(() => {
        setUsers(users.map(u =>
          u.email === oldEmail
            ? { ...u, email: editedEmail, name: editedName }
            : u
        ));
        setEditingUserEmail(null);
        setEditedEmail("");
        setEditedName("");
      });
  };

  // CREATE ADMIN
  const createAdmin = () => {
    if (!newAdminEmail || !newAdminPassword) {
      alert("Enter admin email and password");
      return;
    }

    axios
      .post("http://localhost:5000/api/admin/create", {
        email: newAdminEmail,
        password: newAdminPassword
      })
      .then(() => {
        alert("Admin created successfully");
        setAdmins([...admins, { email: newAdminEmail }]);
        setNewAdminEmail("");
        setNewAdminPassword("");
      });
  };

  // DELETE ADMIN
  const deleteAdmin = (email) => {
    axios
      .delete("http://localhost:5000/api/admin/delete", {
        data: { email, loggedAdmin }
      })
      .then(() => {
        setAdmins(admins.filter(a => a.email !== email));
      })
      .catch(err => {
        alert(err.response?.data?.error || "Cannot delete admin");
      });
  };

  return (
    <div className="admin-page">
      <Header hideHome={true} />

      <div className="admin-wrapper fade">
        <h1 className="admin-title">Admin Dashboard</h1>

        {/* CREATE ADMIN */}
        <div className="admin-section">
          <h2>Create New Admin</h2>
          <div className="admin-form">
            <input
              placeholder="Admin Email"
              value={newAdminEmail}
              onChange={(e) => setNewAdminEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={newAdminPassword}
              onChange={(e) => setNewAdminPassword(e.target.value)}
            />
            <button className="primary-btn" onClick={createAdmin}>
              Create Admin
            </button>
          </div>
        </div>

        {/* ADMIN LIST */}
        <div className="admin-section">
          <h2>Administrators</h2>

          {admins.map((a) => (
            <div className="user-card" key={a.email}>
              <div className="user-info">
                <span className="email">{a.email}</span>
                <span className="role">
                  {a.email === "admin@learnx.com" ? "SUPER ADMIN" : "ADMIN"}
                </span>
              </div>

              {a.email !== loggedAdmin &&
                a.email !== "admin@learnx.com" && (
                  <button
                    className="danger-btn"
                    onClick={() => deleteAdmin(a.email)}
                  >
                    Delete
                  </button>
                )}
            </div>
          ))}
        </div>

        {/* USER LIST */}
        <div className="admin-section">
          <h2>Registered Users</h2>

          {users.map((u) => (
            <div className="user-card" key={u.email}>
              <div className="user-info">

                {editingUserEmail === u.email ? (
                  <>
                    <input
                      className="edit-input"
                      placeholder="Name"
                      value={editedName}
                      onChange={(e) => setEditedName(e.target.value)}
                    />
                    <input
                      className="edit-input"
                      placeholder="Email"
                      value={editedEmail}
                      onChange={(e) => setEditedEmail(e.target.value)}
                    />
                  </>
                ) : (
                  <>
                    <span className="email">{u.name || "—"}</span>
                    <span className="email">{u.email}</span>
                  </>
                )}

                <span className="role">USER</span>
              </div>

              {editingUserEmail === u.email ? (
                <button
                  className="primary-btn"
                  onClick={() => updateUser(u.email)}
                >
                  Save
                </button>
              ) : (
                <div className="action-buttons">
                  <button
                    className="edit-btn"
                    onClick={() => {
                      setEditingUserEmail(u.email);
                      setEditedEmail(u.email);
                      setEditedName(u.name || "");
                    }}
                  >
                    Edit
                  </button>

                  <button
                    className="danger-btn"
                    onClick={() => deleteUser(u.email)}
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
