from flask import Blueprint, request, jsonify
from database.db import get_db

auth = Blueprint("auth", __name__)

# =========================
# USER LOGIN
# =========================
@auth.route("/api/user/login", methods=["POST"])
def user_login():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT name, email FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "name": user["name"],
            "email": user["email"]
        })

    return jsonify({"status": "fail"}), 401


# =========================
# ADMIN LOGIN
# =========================
@auth.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT email FROM admins WHERE email=? AND password=?",
        (data["email"], data["password"])
    )
    admin = cur.fetchone()
    conn.close()

    if admin:
        return jsonify({"status": "success"})

    return jsonify({"status": "fail"}), 401


# =========================
# USER MANAGEMENT (ADMIN)
# =========================
@auth.route("/api/admin/users", methods=["GET", "POST", "DELETE"])
def manage_users():
    conn = get_db()
    conn.execute("PRAGMA busy_timeout = 3000")
    cur = conn.cursor()

    try:
        # READ USERS
        if request.method == "GET":
            cur.execute("SELECT name, email FROM users")
            rows = cur.fetchall()
            return jsonify([
                {"name": r["name"], "email": r["email"]}
                for r in rows
            ])

        # CREATE USER
        if request.method == "POST":
            data = request.json
            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (data["name"], data["email"], data["password"])
            )
            conn.commit()
            return jsonify({"status": "created"})

        # DELETE USER
        if request.method == "DELETE":
            cur.execute(
                "DELETE FROM users WHERE email=?",
                (request.json["email"],)
            )
            conn.commit()
            return jsonify({"status": "deleted"})

    finally:
        conn.close()


# =========================
# UPDATE USER (NAME + EMAIL)
# =========================
@auth.route("/api/admin/user/update", methods=["PUT"])
def update_user():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE users SET name=?, email=? WHERE email=?",
            (data["name"], data["newEmail"], data["oldEmail"])
        )
        conn.commit()
        return jsonify({"status": "updated"})
    finally:
        conn.close()


# =========================
# CREATE ADMIN
# =========================
@auth.route("/api/admin/create", methods=["POST"])
def create_admin():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO admins (email, password) VALUES (?, ?)",
        (data["email"], data["password"])
    )

    conn.commit()
    conn.close()
    return jsonify({"status": "admin_created"})


# =========================
# LIST ADMINS
# =========================
@auth.route("/api/admin/list", methods=["GET"])
def list_admins():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT email FROM admins")
    admins = [{"email": row["email"]} for row in cur.fetchall()]

    conn.close()
    return jsonify(admins)


# =========================
# DELETE ADMIN
# =========================
@auth.route("/api/admin/delete", methods=["DELETE"])
def delete_admin():
    data = request.json
    target_email = data.get("email")
    logged_admin = data.get("loggedAdmin")

    if target_email == "admin@learnx.com":
        return jsonify({"error": "Cannot delete super admin"}), 403

    if target_email == logged_admin:
        return jsonify({"error": "Cannot delete yourself"}), 403

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM admins WHERE email=?", (target_email,))
    conn.commit()
    conn.close()

    return jsonify({"status": "admin_deleted"})
