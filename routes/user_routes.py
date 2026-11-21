from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database import query_db, execute_db
from auth_helper import role_required

user_bp = Blueprint("users", __name__, url_prefix="/api/users")

@user_bp.route("", methods=["GET"])
@role_required(["admin"])
def get_users(current_user):
    role = request.args.get("role")
    status = request.args.get("status")
    search = request.args.get("search")

    where_clauses = []
    params = []

    if role and role.lower() != "all":
        where_clauses.append("role = ?")
        params.append(role)

    if status and status.lower() != "all":
        where_clauses.append("status = ?")
        params.append(status)

    if search:
        term = f"%{search.strip().lower()}%"
        where_clauses.append("(LOWER(full_name) LIKE ? OR LOWER(email) LIKE ? OR LOWER(phone) LIKE ?)")
        params.extend([term, term, term])

    where_str = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    sql = f"SELECT id, email, full_name, phone, role, status, department, avatar_initials, city, created_at FROM users {where_str} ORDER BY created_at DESC"
    users = query_db(sql, params)

    return jsonify({"users": users, "count": len(users)})

@user_bp.route("", methods=["POST"])
@role_required(["admin"])
def create_user(current_user):
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or "password123"
    full_name = (data.get("full_name") or data.get("name") or "").strip()
    role = data.get("role") or "staff"
    phone = (data.get("phone") or "").strip()
    department = (data.get("department") or "").strip()

    if not email or "@" not in email:
        return jsonify({"error": "A valid email address is required."}), 400
    if not full_name:
        return jsonify({"error": "Full name is required."}), 400
    if role not in ["admin", "staff", "customer"]:
        return jsonify({"error": "Role must be admin, staff, or customer."}), 400

    existing = query_db("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (email,), one=True)
    if existing:
        return jsonify({"error": "A user with this email already exists."}), 409

    parts = full_name.split()
    initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()
    hashed = generate_password_hash(password)

    execute_db(
        """INSERT INTO users (email, password_hash, full_name, phone, role, status, department, avatar_initials, country)
           VALUES (?, ?, ?, ?, ?, 'Active', ?, ?, 'Philippines')""",
        (email, hashed, full_name, phone, role, department, initials)
    )

    new_user = query_db("SELECT id, email, full_name, phone, role, status, department, avatar_initials, created_at FROM users WHERE LOWER(email) = LOWER(?)", (email,), one=True)
    
    execute_db(
        "INSERT INTO notifications (role_target, title, message, type) VALUES ('admin', 'System User Created', ?, 'system')",
        (f"User {full_name} ({email}) was created with role '{role}' by {current_user['full_name']}.",)
    )

    return jsonify({"message": f"User {full_name} created successfully.", "user": new_user}), 201

@user_bp.route("/<int:user_id>", methods=["PUT"])
@role_required(["admin"])
def update_user(current_user, user_id):
    existing = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if not existing:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json() or {}
    full_name = data.get("full_name", existing["full_name"]).strip()
    role = data.get("role", existing["role"])
    status = data.get("status", existing["status"])
    phone = data.get("phone", existing.get("phone"))
    department = data.get("department", existing.get("department"))

    parts = full_name.split()
    initials = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

    execute_db(
        "UPDATE users SET full_name = ?, role = ?, status = ?, phone = ?, department = ?, avatar_initials = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (full_name, role, status, phone, department, initials, user_id)
    )

    updated = query_db("SELECT id, email, full_name, phone, role, status, department, avatar_initials, updated_at FROM users WHERE id = ?", (user_id,), one=True)
    return jsonify({"message": "User updated successfully.", "user": updated})

@user_bp.route("/<int:user_id>/reset-password", methods=["PUT"])
@role_required(["admin"])
def reset_password(current_user, user_id):
    existing = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if not existing:
        return jsonify({"error": "User not found."}), 404

    data = request.get_json() or {}
    new_password = data.get("new_password")
    if not new_password or len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400

    new_hash = generate_password_hash(new_password)
    execute_db("UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_hash, user_id))

    return jsonify({"message": f"Password reset successfully for {existing['email']}."})

@user_bp.route("/<int:user_id>", methods=["DELETE"])
@role_required(["admin"])
def delete_user(current_user, user_id):
    if user_id == current_user["id"]:
        return jsonify({"error": "You cannot deactivate or delete your own account."}), 400

    existing = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if not existing:
        return jsonify({"error": "User not found."}), 404

    # Soft delete / toggle Inactive
    execute_db("UPDATE users SET status = 'Inactive', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
    return jsonify({"message": f"User {existing['email']} has been marked Inactive."})
