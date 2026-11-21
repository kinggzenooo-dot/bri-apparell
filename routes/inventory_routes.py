from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import role_required

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/inventory")

@inventory_bp.route("", methods=["GET"])
@role_required(["admin", "staff"])
def get_inventory(current_user):
    status_filter = request.args.get("status")
    category_filter = request.args.get("category")
    search = request.args.get("search")

    where_clauses = ["p.is_active = 1"]
    params = []

    if status_filter and status_filter.lower() != "all":
        if status_filter.lower() == "low":
            where_clauses.append("v.stock_quantity <= v.threshold AND v.stock_quantity > 0")
        elif status_filter.lower() == "out":
            where_clauses.append("v.stock_quantity = 0")
        elif status_filter.lower() == "in":
            where_clauses.append("v.stock_quantity > v.threshold")
        else:
            where_clauses.append("LOWER(v.status) = LOWER(?)")
            params.append(status_filter)

    if category_filter and category_filter.lower() != "all":
        where_clauses.append("LOWER(p.category) = LOWER(?)")
        params.append(category_filter)

    if search:
        term = f"%{search.strip().lower()}%"
        where_clauses.append("(LOWER(p.name) LIKE ? OR LOWER(v.sku) LIKE ? OR LOWER(v.color_name) LIKE ? OR LOWER(v.id) LIKE ?)")
        params.extend([term, term, term, term])

    where_str = "WHERE " + " AND ".join(where_clauses)

    sql = f"""
        SELECT 
            v.id, v.product_id, v.sku, v.color_name, v.color_hex, v.size,
            v.stock_quantity, v.threshold, v.location, v.status, v.updated_at,
            p.name as product_name, p.category, p.price, p.sale_price, p.is_sale
        FROM product_variants v
        JOIN products p ON p.id = v.product_id
        {where_str}
        ORDER BY (v.stock_quantity <= v.threshold) DESC, v.stock_quantity ASC, v.sku ASC
    """
    variants = query_db(sql, params)
    return jsonify({"inventory": variants, "count": len(variants)})

@inventory_bp.route("/adjust", methods=["POST"])
@role_required(["admin", "staff"])
def adjust_stock(current_user):
    data = request.get_json() or {}
    variant_id = data.get("variant_id")
    quantity_change = data.get("quantity_change") # e.g. +10 or -5
    new_absolute_stock = data.get("new_stock")
    change_type = data.get("change_type", "RESTOCK") # RESTOCK, AUDIT_CORRECTION, DAMAGE, RETURN
    reason = data.get("reason", "Manual Inventory Adjustment")

    if not variant_id:
        return jsonify({"error": "variant_id is required."}), 400

    variant = query_db("SELECT * FROM product_variants WHERE id = ?", (variant_id,), one=True)
    if not variant:
        return jsonify({"error": "Variant not found."}), 404

    current_stock = variant["stock_quantity"]
    if new_absolute_stock is not None:
        new_stock = max(0, int(new_absolute_stock))
        qty_diff = new_stock - current_stock
    elif quantity_change is not None:
        qty_diff = int(quantity_change)
        new_stock = max(0, current_stock + qty_diff)
    else:
        return jsonify({"error": "Either quantity_change or new_stock must be provided."}), 400

    # Determine status
    if new_stock == 0:
        status = "Out of Stock"
    elif new_stock <= variant["threshold"]:
        status = "Low Stock"
    else:
        status = "In Stock"

    execute_db(
        "UPDATE product_variants SET stock_quantity = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_stock, status, variant_id)
    )

    # Insert audit history log
    execute_db(
        """INSERT INTO inventory_logs (variant_id, product_id, change_type, quantity_changed, new_stock, reason, performed_by)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (variant_id, variant["product_id"], change_type, qty_diff, new_stock, reason, current_user["full_name"])
    )

    if status in ["Low Stock", "Out of Stock"]:
        execute_db(
            "INSERT INTO notifications (role_target, title, message, type, link) VALUES ('admin', 'Inventory Alert', ?, 'stock', 'inventory.html')",
            (f"SKU {variant['sku']} is {status.lower()} ({new_stock} remaining).",)
        )

    updated_variant = query_db("SELECT * FROM product_variants WHERE id = ?", (variant_id,), one=True)
    return jsonify({
        "message": f"Stock for {variant['sku']} updated from {current_stock} to {new_stock}.",
        "variant": updated_variant
    })

@inventory_bp.route("/logs", methods=["GET"])
@role_required(["admin", "staff"])
def get_inventory_logs(current_user):
    logs = query_db("""
        SELECT l.*, v.sku, p.name as product_name
        FROM inventory_logs l
        LEFT JOIN product_variants v ON v.id = l.variant_id
        LEFT JOIN products p ON p.id = l.product_id
        ORDER BY l.created_at DESC
        LIMIT 100
    """)
    return jsonify({"logs": logs})
