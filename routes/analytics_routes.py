from flask import Blueprint, jsonify
from database import query_db
from auth_helper import role_required

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")

@analytics_bp.route("/overview", methods=["GET"])
@role_required(["admin", "staff"])
def get_overview(current_user):
    # Total revenue from paid/delivered orders
    rev_res = query_db("SELECT COALESCE(SUM(total), 0) as total_revenue FROM orders WHERE payment_status = 'Paid' OR status = 'Delivered'", one=True)
    total_revenue = float(rev_res["total_revenue"]) if rev_res else 0.0

    # Total orders count
    orders_cnt = query_db("SELECT COUNT(*) as count FROM orders", one=True)["count"]

    # Average Order Value
    aov = (total_revenue / orders_cnt) if orders_cnt > 0 else 0.0

    # Customers count
    cust_cnt = query_db("SELECT COUNT(*) as count FROM users WHERE role = 'customer' AND status = 'Active'", one=True)["count"]

    # Low stock items count
    low_stock_cnt = query_db("SELECT COUNT(*) as count FROM product_variants WHERE stock_quantity <= threshold", one=True)["count"]

    # Pending orders count
    pending_cnt = query_db("SELECT COUNT(*) as count FROM orders WHERE status IN ('Placed', 'Processing')", one=True)["count"]

    # Sales by category
    sales_by_cat = query_db("""
        SELECT 
            p.category, 
            COUNT(oi.id) as units_sold, 
            COALESCE(SUM(oi.total_price), 0) as total_sales
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        GROUP BY p.category
        ORDER BY total_sales DESC
    """)

    # Top selling products
    top_products = query_db("""
        SELECT 
            oi.product_id, 
            oi.product_name, 
            COUNT(oi.id) as order_count,
            SUM(oi.quantity) as total_qty, 
            SUM(oi.total_price) as total_sales
        FROM order_items oi
        GROUP BY oi.product_id, oi.product_name
        ORDER BY total_sales DESC
        LIMIT 6
    """)

    # Payment methods breakdown
    pay_methods = query_db("""
        SELECT payment_method, COUNT(*) as count, SUM(amount) as total
        FROM payments
        GROUP BY payment_method
        ORDER BY total DESC
    """)

    # Order status breakdown
    order_statuses = query_db("""
        SELECT status, COUNT(*) as count
        FROM orders
        GROUP BY status
        ORDER BY count DESC
    """)

    # Recent 6 orders
    recent_orders = query_db("SELECT * FROM orders ORDER BY created_at DESC LIMIT 6")
    for ro in recent_orders:
        ro["items"] = query_db("SELECT * FROM order_items WHERE order_id = ?", (ro["id"],))

    return jsonify({
        "kpi": {
            "totalRevenue": total_revenue,
            "totalOrders": orders_cnt,
            "averageOrderValue": aov,
            "activeCustomers": cust_cnt,
            "lowStockCount": low_stock_cnt,
            "pendingOrders": pending_cnt
        },
        "salesByCategory": sales_by_cat,
        "topProducts": top_products,
        "paymentMethods": pay_methods,
        "orderStatuses": order_statuses,
        "recentOrders": recent_orders
    })
