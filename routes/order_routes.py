import random
import datetime
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import get_current_user, login_required, role_required

order_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

STATUS_STEPS = {
    "Placed": 1,
    "Confirmed": 2,
    "Processing": 3,
    "Packed": 4,
    "Ready to Ship": 5,
    "In Transit": 6,
    "Delivered": 7,
    "Cancelled": 0
}

@order_bp.route("", methods=["POST"])
def create_order():
    """
    Places an order into the centralized database.
    Can be called by authenticated customer or guest checkout.
    """
    user = get_current_user()
    data = request.get_json() or {}

    items = data.get("items") or []
    if not items:
        return jsonify({"error": "Cannot place an empty order. Please add items to your bag."}), 400

    customer_name = (data.get("customer_name") or (user["full_name"] if user else "")).strip()
    customer_email = (data.get("customer_email") or (user["email"] if user else "")).strip().lower()
    customer_phone = (data.get("customer_phone") or (user.get("phone") if user else "")).strip()
    shipping_address = (data.get("shipping_address") or "").strip()
    city = (data.get("city") or (user.get("city") if user else "Taguig")).strip()
    province = (data.get("province") or (user.get("province") if user else "Metro Manila")).strip()
    postal_code = (data.get("postal_code") or (user.get("postal_code") if user else "1634")).strip()
    payment_method = (data.get("payment_method") or "GCASH").strip().upper()
    notes = (data.get("notes") or "").strip()

    if not customer_name or not customer_email or not shipping_address:
        return jsonify({"error": "Customer name, email, and shipping address are required."}), 400

    # Calculate item totals and verify prices
    subtotal = 0.0
    processed_items = []
    for itm in items:
        p_id = itm.get("id")
        p = query_db("SELECT id, name, price, sale_price, is_sale FROM products WHERE id = ?", (p_id,), one=True)
        if not p:
            continue
        price = float(p["sale_price"]) if (p["is_sale"] and p["sale_price"]) else float(p["price"])
        qty = max(1, int(itm.get("quantity", 1)))
        tot = price * qty
        subtotal += tot
        
        size = itm.get("size", "M")
        color = itm.get("color", "Standard")
        sku = f"BRI-{p['id'].upper()}-{color[:3].upper()}-{size}"

        processed_items.append({
            "product_id": p["id"],
            "product_name": p["name"],
            "variant_name": color,
            "size": size,
            "color": color,
            "sku": sku,
            "quantity": qty,
            "unit_price": price,
            "total_price": tot
        })

    if not processed_items:
        return jsonify({"error": "No valid products found in order."}), 400

    # Discount from promo code if provided
    discount = float(data.get("discount", 0.0))
    shipping_fee = 0.0 if subtotal >= 2500 else float(data.get("shipping_fee", 150.0))
    grand_total = max(0.0, subtotal - discount + shipping_fee)

    # Generate unique Order ID: e.g. BRI-2026-8942
    order_id = f"BRI-2026-{random.randint(1000, 9999)}"
    # Check uniqueness
    while query_db("SELECT id FROM orders WHERE id = ?", (order_id,), one=True):
        order_id = f"BRI-2026-{random.randint(1000, 9999)}"

    user_id = user["id"] if user else None

    # Insert Order
    execute_db(
        """INSERT INTO orders (id, user_id, customer_name, customer_email, customer_phone, shipping_address, city, province, postal_code, country, subtotal, discount, shipping_fee, total, status, status_step, payment_method, payment_status, courier, tracking_number, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Philippines', ?, ?, ?, ?, 'Placed', 1, ?, 'Pending', 'LBC Express', NULL, ?)""",
        (order_id, user_id, customer_name, customer_email, customer_phone, shipping_address, city, province, postal_code, subtotal, discount, shipping_fee, grand_total, payment_method, notes)
    )

    # Insert Items & Deduct Inventory Stock
    for item in processed_items:
        execute_db(
            """INSERT INTO order_items (order_id, product_id, sku, product_name, variant_name, size, color, quantity, unit_price, total_price)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (order_id, item["product_id"], item["sku"], item["product_name"], item["variant_name"], item["size"], item["color"], item["quantity"], item["unit_price"], item["total_price"])
        )

        # Deduct stock variant if exists
        variant = query_db(
            "SELECT id, stock_quantity, threshold FROM product_variants WHERE product_id = ? AND size = ? LIMIT 1",
            (item["product_id"], item["size"]),
            one=True
        )
        if variant:
            new_stock = max(0, variant["stock_quantity"] - item["quantity"])
            status = "Low Stock" if new_stock <= variant["threshold"] else ("Out of Stock" if new_stock == 0 else "In Stock")
            execute_db("UPDATE product_variants SET stock_quantity = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (new_stock, status, variant["id"]))
            execute_db(
                "INSERT INTO inventory_logs (variant_id, product_id, change_type, quantity_changed, new_stock, reason, performed_by) VALUES (?, ?, 'ORDER_DEDUCTION', ?, ?, ?, 'System Order Placement')",
                (variant["id"], item["product_id"], -item["quantity"], new_stock, f"Order #{order_id}")
            )

    # Insert Initial Order History
    execute_db(
        "INSERT INTO order_history (order_id, status, notes, staff_name) VALUES (?, 'Placed', 'Order placed by customer online', 'System')",
        (order_id,)
    )

    # Insert Payment record
    txn_id = f"TXN-2026-{random.randint(10000, 99999)}"
    pay_status = "Paid" if payment_method in ["GCASH", "MAYA", "CARD"] else "Pending"
    execute_db(
        "INSERT INTO payments (id, order_id, amount, payment_method, status, reference_number, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (txn_id, order_id, grand_total, payment_method, pay_status, txn_id, f"Payment for {order_id}")
    )
    if pay_status == "Paid":
        execute_db("UPDATE orders SET payment_status = 'Paid' WHERE id = ?", (order_id,))

    # Create Real-time Notification for Admin & Staff
    execute_db(
        "INSERT INTO notifications (role_target, title, message, type, link) VALUES ('admin', 'New Order Received', ?, 'order', ?)",
        (f"Order #{order_id} placed by {customer_name} for ₱{grand_total:,.2f}.", f"order-details.html?id={order_id}")
    )

    full_order = query_db("SELECT * FROM orders WHERE id = ?", (order_id,), one=True)
    full_order["items"] = processed_items

    return jsonify({
        "message": "Order placed successfully.",
        "orderId": order_id,
        "order": full_order
    }), 201

@order_bp.route("", methods=["GET"])
def get_orders():
    """
    Returns orders.
    Admin and Staff see all orders.
    Customers see only their own orders.
    """
    user = get_current_user()
    email_query = request.args.get("email")
    status_filter = request.args.get("status")
    search_query = request.args.get("search")

    is_staff = user and user.get("role") in ["admin", "staff"]

    where_clauses = []
    params = []

    if not is_staff:
        # Restricted to current user
        if user:
            where_clauses.append("(user_id = ? OR LOWER(customer_email) = LOWER(?))")
            params.extend([user["id"], user["email"]])
        elif email_query:
            where_clauses.append("LOWER(customer_email) = LOWER(?)")
            params.append(email_query.strip().lower())
        else:
            return jsonify({"orders": [], "count": 0})
    else:
        # Staff/Admin filters
        if email_query:
            where_clauses.append("LOWER(customer_email) = LOWER(?)")
            params.append(email_query.strip().lower())

    if status_filter and status_filter.lower() != "all":
        where_clauses.append("LOWER(status) = LOWER(?)")
        params.append(status_filter.strip().lower())

    if search_query:
        term = f"%{search_query.strip().lower()}%"
        where_clauses.append("(LOWER(id) LIKE ? OR LOWER(customer_name) LIKE ? OR LOWER(customer_email) LIKE ? OR LOWER(customer_phone) LIKE ?)")
        params.extend([term, term, term, term])

    where_str = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    sql = f"SELECT * FROM orders {where_str} ORDER BY created_at DESC"
    orders = query_db(sql, params)

    # Attach items to each order
    for o in orders:
        items = query_db("SELECT * FROM order_items WHERE order_id = ?", (o["id"],))
        o["items"] = items

    return jsonify({"orders": orders, "count": len(orders)})

@order_bp.route("/<order_id>", methods=["GET"])
def get_order_details(order_id):
    order = query_db("SELECT * FROM orders WHERE id = ?", (order_id,), one=True)
    if not order:
        return jsonify({"error": "Order not found."}), 404

    user = get_current_user()
    is_staff = user and user.get("role") in ["admin", "staff"]

    # Customer privacy check
    if not is_staff and user:
        if order.get("user_id") != user["id"] and order.get("customer_email").lower() != user["email"].lower():
            return jsonify({"error": "Unauthorized to view this order."}), 403

    items = query_db("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    history = query_db("SELECT * FROM order_history WHERE order_id = ? ORDER BY created_at ASC", (order_id,))
    payments = query_db("SELECT * FROM payments WHERE order_id = ?", (order_id,))

    order["items"] = items
    order["history"] = history
    order["payments"] = payments

    return jsonify(order)

@order_bp.route("/<order_id>/status", methods=["PUT"])
@role_required(["admin", "staff"])
def update_order_status(current_user, order_id):
    order = query_db("SELECT * FROM orders WHERE id = ?", (order_id,), one=True)
    if not order:
        return jsonify({"error": "Order not found."}), 404

    data = request.get_json() or {}
    new_status = data.get("status")
    notes = data.get("notes") or f"Status updated to {new_status}"
    courier = data.get("courier") or order.get("courier")
    tracking_number = data.get("tracking_number") or order.get("tracking_number")

    if not new_status:
        return jsonify({"error": "New status is required."}), 400

    step = STATUS_STEPS.get(new_status, order.get("status_step", 1))

    execute_db(
        "UPDATE orders SET status = ?, status_step = ?, courier = ?, tracking_number = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_status, step, courier, tracking_number, order_id)
    )

    # Insert into order history
    execute_db(
        "INSERT INTO order_history (order_id, status, notes, staff_name) VALUES (?, ?, ?, ?)",
        (order_id, new_status, notes, current_user["full_name"])
    )

    # Log notification
    execute_db(
        "INSERT INTO notifications (role_target, title, message, type, link) VALUES ('admin', 'Order Status Updated', ?, 'order', ?)",
        (f"Order #{order_id} moved to '{new_status}' by {current_user['full_name']}.", f"order-details.html?id={order_id}")
    )

    updated_order = query_db("SELECT * FROM orders WHERE id = ?", (order_id,), one=True)
    return jsonify({"message": f"Order #{order_id} status updated to {new_status}.", "order": updated_order})

@order_bp.route("/<order_id>/payment", methods=["PUT"])
@role_required(["admin", "staff"])
def update_order_payment(current_user, order_id):
    data = request.get_json() or {}
    payment_status = data.get("payment_status", "Paid")
    notes = data.get("notes", "Payment verified by staff")

    execute_db("UPDATE orders SET payment_status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (payment_status, order_id))
    execute_db("UPDATE payments SET status = ?, notes = ? WHERE order_id = ?", (payment_status, notes, order_id))

    execute_db(
        "INSERT INTO order_history (order_id, status, notes, staff_name) VALUES (?, ?, ?, ?)",
        (order_id, f"Payment: {payment_status}", notes, current_user["full_name"])
    )

    return jsonify({"message": f"Order #{order_id} payment marked as {payment_status}."})
