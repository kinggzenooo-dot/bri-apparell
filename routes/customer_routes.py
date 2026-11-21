from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import role_required

customer_bp = Blueprint("customers", __name__, url_prefix="/api/customers")

@customer_bp.route("", methods=["GET"])
@role_required(["admin", "staff"])
def get_customers(current_user):
    search = request.args.get("search")
    where_clauses = ["u.role = 'customer'"]
    params = []

    if search:
        term = f"%{search.strip().lower()}%"
        where_clauses.append("(LOWER(u.full_name) LIKE ? OR LOWER(u.email) LIKE ? OR LOWER(u.phone) LIKE ?)")
        params.extend([term, term, term])

    where_str = "WHERE " + " AND ".join(where_clauses)

    sql = f"""
        SELECT 
            u.id, u.email, u.full_name, u.phone, u.status, u.street, u.city, u.province, u.postal_code, u.notes, u.created_at,
            COUNT(o.id) as orders_count,
            COALESCE(SUM(o.total), 0) as total_spent,
            MAX(o.created_at) as last_order_date
        FROM users u
        LEFT JOIN orders o ON (o.user_id = u.id OR LOWER(o.customer_email) = LOWER(u.email))
        {where_str}
        GROUP BY u.id
        ORDER BY total_spent DESC, u.created_at DESC
    """
    customers = query_db(sql, params)
    return jsonify({"customers": customers, "count": len(customers)})

@customer_bp.route("/<int:customer_id>", methods=["GET"])
@role_required(["admin", "staff"])
def get_customer_detail(current_user, customer_id):
    customer = query_db("SELECT id, email, full_name, phone, status, street, city, province, postal_code, country, notes, created_at FROM users WHERE id = ? AND role = 'customer'", (customer_id,), one=True)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    orders = query_db("SELECT * FROM orders WHERE user_id = ? OR LOWER(customer_email) = LOWER(?) ORDER BY created_at DESC", (customer_id, customer["email"]))
    for o in orders:
        o["items"] = query_db("SELECT * FROM order_items WHERE order_id = ?", (o["id"],))

    customer["orders"] = orders
    customer["total_spent"] = sum(float(o["total"]) for o in orders)
    customer["orders_count"] = len(orders)

    return jsonify(customer)

@customer_bp.route("/<int:customer_id>", methods=["PUT"])
@role_required(["admin", "staff"])
def update_customer(current_user, customer_id):
    data = request.get_json() or {}
    customer = query_db("SELECT * FROM users WHERE id = ? AND role = 'customer'", (customer_id,), one=True)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    status = data.get("status", customer["status"])
    notes = data.get("notes", customer.get("notes"))
    phone = data.get("phone", customer.get("phone"))

    execute_db(
        "UPDATE users SET status = ?, notes = ?, phone = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (status, notes, phone, customer_id)
    )

    updated = query_db("SELECT id, email, full_name, phone, status, notes, updated_at FROM users WHERE id = ?", (customer_id,), one=True)
    return jsonify({"message": "Customer updated successfully.", "customer": updated})
