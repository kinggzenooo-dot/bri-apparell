from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import query_db, execute_db
from auth_helper import generate_token, get_current_user, login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    full_name = (data.get("full_name") or data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    street = (data.get("street") or "").strip()
    city = (data.get("city") or "").strip()
    province = (data.get("province") or "").strip()
    postal_code = (data.get("postal_code") or "").strip()

    if not email or "@" not in email:
        return jsonify({"error": "A valid email address is required."}), 400
    if not password or len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if not full_name:
        return jsonify({"error": "Full name is required."}), 400

    existing = query_db("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (email,), one=True)
    if existing:
        return jsonify({"error": "An account with this email address already exists."}), 409

    # Generate initials
    parts = full_name.split()
    initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()
    hashed = generate_password_hash(password)

    res = execute_db(
        """INSERT INTO users (email, password_hash, full_name, phone, role, status, avatar_initials, street, city, province, postal_code, country)
           VALUES (?, ?, ?, ?, 'customer', 'Active', ?, ?, ?, ?, ?, 'Philippines')""",
        (email, hashed, full_name, phone, initials, street, city, province, postal_code)
    )

    user = query_db("SELECT id, email, full_name, phone, role, status, avatar_initials, street, city, province, postal_code, country, created_at FROM users WHERE LOWER(email) = LOWER(?)", (email,), one=True)
    
    # Notify admin
    execute_db(
        "INSERT INTO notifications (role_target, title, message, type) VALUES ('admin', ?, ?, 'customer')",
        ("New Customer Registered", f"{full_name} ({email}) created an account.")
    )

    token = generate_token(user["id"], user["email"], user["role"])
    session["user_id"] = user["id"]

    resp = jsonify({
        "message": "Account created successfully.",
        "token": token,
        "user": user
    })
    resp.set_cookie("bri_token", token, max_age=7*24*3600, samesite="Lax")
    return resp, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = query_db("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,), one=True)
    if not user:
        return jsonify({"error": "Invalid email or password."}), 401

    if user.get("status") != "Active":
        return jsonify({"error": "This account is inactive or suspended. Please contact store management."}), 403

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password."}), 401

    # Safe user dict
    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    token = generate_token(safe_user["id"], safe_user["email"], safe_user["role"])
    session["user_id"] = safe_user["id"]

    resp = jsonify({
        "message": f"Welcome back, {safe_user['full_name']}.",
        "token": token,
        "user": safe_user
    })
    resp.set_cookie("bri_token", token, max_age=7*24*3600, samesite="Lax")
    return resp

@auth_bp.route("/me", methods=["GET"])
def me():
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False, "user": None}), 200
    return jsonify({"authenticated": True, "user": user})

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    resp = jsonify({"message": "Successfully logged out."})
    resp.delete_cookie("bri_token")
    return resp

@auth_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile(current_user):
    data = request.get_json() or {}
    full_name = data.get("full_name") or current_user["full_name"]
    phone = data.get("phone") or current_user.get("phone")
    street = data.get("street") or current_user.get("street")
    city = data.get("city") or current_user.get("city")
    province = data.get("province") or current_user.get("province")
    postal_code = data.get("postal_code") or current_user.get("postal_code")

    parts = full_name.split()
    initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

    execute_db(
        """UPDATE users SET full_name = ?, phone = ?, street = ?, city = ?, province = ?, postal_code = ?, avatar_initials = ?, updated_at = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (full_name, phone, street, city, province, postal_code, initials, current_user["id"])
    )

    updated_user = query_db(
        "SELECT id, email, full_name, phone, role, status, department, avatar_initials, street, city, province, postal_code, country FROM users WHERE id = ?",
        (current_user["id"],),
        one=True
    )
    return jsonify({"message": "Profile updated successfully.", "user": updated_user})

@auth_bp.route("/password", methods=["PUT"])
@login_required
def change_password(current_user):
    data = request.get_json() or {}
    current_pass = data.get("current_password") or ""
    new_pass = data.get("new_password") or ""

    if not current_pass or not new_pass:
        return jsonify({"error": "Both current and new passwords are required."}), 400
    if len(new_pass) < 6:
        return jsonify({"error": "New password must be at least 6 characters."}), 400

    user_rec = query_db("SELECT password_hash FROM users WHERE id = ?", (current_user["id"],), one=True)
    if not check_password_hash(user_rec["password_hash"], current_pass):
        return jsonify({"error": "Incorrect current password."}), 400

    new_hash = generate_password_hash(new_pass)
    execute_db("UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_hash, current_user["id"]))

    return jsonify({"message": "Password changed successfully."})
