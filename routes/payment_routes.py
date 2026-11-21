from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import role_required

payment_bp = Blueprint("payments", __name__, url_prefix="/api/payments")

@payment_bp.route("", methods=["GET"])
@role_required(["admin", "staff"])
def get_payments(current_user):
    status_filter = request.args.get("status")
    method_filter = request.args.get("method")
    search = request.args.get("search")

    where_clauses = []
    params = []

    if status_filter and status_filter.lower() != "all":
        where_clauses.append("LOWER(p.status) = LOWER(?)")
        params.append(status_filter)

    if method_filter and method_filter.lower() != "all":
        where_clauses.append("LOWER(p.payment_method) LIKE ?")
        params.append(f"%{method_filter.lower()}%")

    if search:
        term = f"%{search.strip().lower()}%"
        where_clauses.append("(LOWER(p.id) LIKE ? OR LOWER(p.order_id) LIKE ? OR LOWER(p.reference_number) LIKE ? OR LOWER(o.customer_name) LIKE ?)")
        params.extend([term, term, term, term])

    where_str = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    sql = f"""
        SELECT 
            p.id, p.order_id, p.amount, p.payment_method, p.status, p.reference_number, p.notes, p.paid_at,
            o.customer_name, o.customer_email, o.total as order_total
        FROM payments p
        JOIN orders o ON o.id = p.order_id
        {where_str}
        ORDER BY p.paid_at DESC
    """
    payments = query_db(sql, params)
    return jsonify({"payments": payments, "count": len(payments)})

@payment_bp.route("/<payment_id>/status", methods=["PUT"])
@role_required(["admin"])
def update_payment_status(current_user, payment_id):
    data = request.get_json() or {}
    new_status = data.get("status")
    notes = data.get("notes") or f"Payment marked as {new_status}"

    if not new_status:
        return jsonify({"error": "Payment status is required."}), 400

    payment = query_db("SELECT * FROM payments WHERE id = ?", (payment_id,), one=True)
    if not payment:
        return jsonify({"error": "Payment record not found."}), 404

    execute_db("UPDATE payments SET status = ?, notes = ? WHERE id = ?", (new_status, notes, payment_id))
    
    # Synchronize order payment status
    execute_db("UPDATE orders SET payment_status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_status, payment["order_id"]))

    return jsonify({"message": f"Payment #{payment_id} updated to {new_status}."})
