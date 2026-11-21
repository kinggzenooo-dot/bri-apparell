from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import login_required

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")

@notification_bp.route("", methods=["GET"])
@login_required
def get_notifications(current_user):
    role = current_user.get("role", "customer")
    unread_only = request.args.get("unread_only", "false").lower() == "true"

    where_clauses = ["(role_target = ? OR role_target = 'all' OR user_id = ?)"]
    params = [role, current_user["id"]]

    if unread_only:
        where_clauses.append("is_read = 0")

    where_str = "WHERE " + " AND ".join(where_clauses)
    sql = f"SELECT * FROM notifications {where_str} ORDER BY created_at DESC LIMIT 50"
    notifications = query_db(sql, params)

    unread_count = query_db(
        "SELECT COUNT(*) as cnt FROM notifications WHERE (role_target = ? OR role_target = 'all' OR user_id = ?) AND is_read = 0",
        (role, current_user["id"]),
        one=True
    )["cnt"]

    return jsonify({"notifications": notifications, "unreadCount": unread_count})

@notification_bp.route("/<int:notif_id>/read", methods=["PUT"])
@login_required
def mark_read(current_user, notif_id):
    execute_db("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
    return jsonify({"message": "Notification marked as read."})

@notification_bp.route("/read-all", methods=["POST"])
@login_required
def mark_all_read(current_user):
    role = current_user.get("role", "customer")
    execute_db(
        "UPDATE notifications SET is_read = 1 WHERE (role_target = ? OR role_target = 'all' OR user_id = ?) AND is_read = 0",
        (role, current_user["id"])
    )
    return jsonify({"message": "All notifications marked as read."})
