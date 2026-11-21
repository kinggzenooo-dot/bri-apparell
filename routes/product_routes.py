import json
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import role_required

product_bp = Blueprint("products", __name__, url_prefix="/api/products")

def format_product(p):
    """Helper to parse JSON strings back into arrays/dicts for API responses."""
    if not p:
        return None
    res = dict(p)
    for field in ["colors", "sizes", "images", "care", "details"]:
        val = res.get(field)
        if isinstance(val, str):
            try:
                res[field] = json.loads(val)
            except Exception:
                res[field] = [line.strip() for line in val.split("\n") if line.strip()] if val else []
        elif val is None:
            res[field] = []
    # Boolean conversions
    res["isSale"] = bool(res.get("is_sale"))
    res["isNew"] = bool(res.get("is_new"))
    res["isFeatured"] = bool(res.get("is_featured"))
    res["isActive"] = bool(res.get("is_active"))
    res["salePrice"] = res.get("sale_price")
    res["shortDesc"] = res.get("short_desc")
    res["reviewCount"] = res.get("review_count")
    return res

@product_bp.route("", methods=["GET"])
def get_products():
    category = request.args.get("category")
    gender = request.args.get("gender")
    collection = request.args.get("collection")
    featured = request.args.get("featured")
    is_sale = request.args.get("sale")
    search = request.args.get("search")
    sort_by = request.args.get("sort", "featured")
    include_inactive = request.args.get("include_inactive", "false").lower() == "true"

    where_clauses = []
    params = []

    if not include_inactive:
        where_clauses.append("is_active = 1")

    if category and category.lower() != "all":
        where_clauses.append("LOWER(category) = LOWER(?)")
        params.append(category)

    if gender and gender.lower() != "all":
        where_clauses.append("(LOWER(gender) = LOWER(?) OR LOWER(gender) = 'unisex')")
        params.append(gender)

    if collection and collection.lower() != "all":
        where_clauses.append("LOWER(collection) = LOWER(?)")
        params.append(collection)

    if featured and featured.lower() == "true":
        where_clauses.append("is_featured = 1")

    if is_sale and is_sale.lower() == "true":
        where_clauses.append("is_sale = 1")

    if search:
        term = f"%{search.strip().lower()}%"
        where_clauses.append("(LOWER(name) LIKE ? OR LOWER(short_desc) LIKE ? OR LOWER(id) LIKE ? OR LOWER(tag) LIKE ?)")
        params.extend([term, term, term, term])

    where_str = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # Sort mappings
    order_clause = "ORDER BY id ASC"
    if sort_by == "price-low":
        order_clause = "ORDER BY COALESCE(sale_price, price) ASC"
    elif sort_by == "price-high":
        order_clause = "ORDER BY COALESCE(sale_price, price) DESC"
    elif sort_by == "newest":
        order_clause = "ORDER BY is_new DESC, created_at DESC"
    elif sort_by == "rating":
        order_clause = "ORDER BY rating DESC"
    elif sort_by == "featured":
        order_clause = "ORDER BY is_featured DESC, id ASC"

    sql = f"SELECT * FROM products {where_str} {order_clause}"
    products = query_db(sql, params)
    formatted = [format_product(p) for p in products]

    return jsonify({"products": formatted, "count": len(formatted)})

@product_bp.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    p = query_db("SELECT * FROM products WHERE id = ?", (product_id,), one=True)
    if not p:
        return jsonify({"error": "Product not found"}), 404

    formatted = format_product(p)
    # Fetch variants & inventory
    variants = query_db("SELECT * FROM product_variants WHERE product_id = ? ORDER BY sku ASC", (product_id,))
    formatted["variants"] = variants

    # Fetch reviews
    reviews = query_db("SELECT * FROM reviews WHERE product_id = ? AND status = 'Approved' ORDER BY created_at DESC", (product_id,))
    formatted["customerReviews"] = reviews

    return jsonify(formatted)

@product_bp.route("", methods=["POST"])
@role_required(["admin"])
def create_product(current_user):
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    category = (data.get("category") or "Tops").strip()
    gender = data.get("gender") or "Unisex"
    price = data.get("price")
    sale_price = data.get("salePrice") or data.get("sale_price")
    is_sale = bool(data.get("isSale") or data.get("is_sale"))
    is_new = bool(data.get("isNew") or data.get("is_new"))
    is_featured = bool(data.get("isFeatured") or data.get("is_featured"))
    collection = data.get("collection") or "essentials"
    tag = data.get("tag") or ""
    short_desc = data.get("shortDesc") or data.get("short_desc") or ""
    description = data.get("description") or ""
    materials = data.get("materials") or ""
    care = json.dumps(data.get("care") or [])
    details = json.dumps(data.get("details") or [])
    colors = json.dumps(data.get("colors") or [{"name": "Standard", "hex": "#000000"}])
    sizes = json.dumps(data.get("sizes") or [{"size": "S", "inStock": True}, {"size": "M", "inStock": True}, {"size": "L", "inStock": True}])
    images = json.dumps(data.get("images") or ["https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000"])

    if not name or price is None:
        return jsonify({"error": "Product name and price are required."}), 400

    # Generate custom product ID if not supplied
    p_id = data.get("id")
    if not p_id:
        count_res = query_db("SELECT COUNT(*) as cnt FROM products", one=True)
        p_id = f"bri-{(count_res['cnt'] + 1):03d}"

    existing = query_db("SELECT id FROM products WHERE id = ?", (p_id,), one=True)
    if existing:
        return jsonify({"error": f"Product with ID '{p_id}' already exists."}), 409

    execute_db(
        """INSERT INTO products (id, name, category, gender, price, sale_price, is_sale, is_new, is_featured, rating, review_count, collection, tag, short_desc, description, materials, care, details, colors, sizes, images, is_active)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 5.0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
        (p_id, name, category, gender, price, sale_price, 1 if is_sale else 0, 1 if is_new else 0, 1 if is_featured else 0, collection, tag, short_desc, description, materials, care, details, colors, sizes, images)
    )

    # Automatically create initial variant SKUs
    raw_colors = data.get("colors") or [{"name": "Standard", "hex": "#000000"}]
    raw_sizes = data.get("sizes") or [{"size": "S"}, {"size": "M"}, {"size": "L"}]
    for c in raw_colors:
        for s in raw_sizes:
            s_val = s.get("size") if isinstance(s, dict) else str(s)
            c_name = c.get("name") if isinstance(c, dict) else str(c)
            c_hex = c.get("hex", "#000000") if isinstance(c, dict) else "#000000"
            sku = f"BRI-{p_id.upper()}-{c_name[:3].upper()}-{s_val}"
            var_id = f"var-{p_id}-{c_name[:3].lower()}-{s_val.lower()}"
            execute_db(
                """INSERT OR IGNORE INTO product_variants (id, product_id, sku, color_name, color_hex, size, stock_quantity, threshold, location, status)
                   VALUES (?, ?, ?, ?, ?, ?, 20, 5, 'Main Warehouse - Rack C', 'In Stock')""",
                (var_id, p_id, sku, c_name, c_hex, s_val)
            )

    # Log notification
    execute_db(
        "INSERT INTO notifications (role_target, title, message, type) VALUES ('admin', 'Product Created', ?, 'system')",
        (f"New product '{name}' ({p_id}) added to catalog by {current_user['full_name']}.",)
    )

    created = query_db("SELECT * FROM products WHERE id = ?", (p_id,), one=True)
    return jsonify({"message": "Product created successfully.", "product": format_product(created)}), 201

@product_bp.route("/<product_id>", methods=["PUT"])
@role_required(["admin", "staff"])
def update_product(current_user, product_id):
    data = request.get_json() or {}
    existing = query_db("SELECT * FROM products WHERE id = ?", (product_id,), one=True)
    if not existing:
        return jsonify({"error": "Product not found."}), 404

    name = data.get("name", existing["name"])
    category = data.get("category", existing["category"])
    gender = data.get("gender", existing["gender"])
    price = data.get("price", existing["price"])
    sale_price = data.get("salePrice", existing["sale_price"])
    is_sale = 1 if (data.get("isSale") if "isSale" in data else existing["is_sale"]) else 0
    is_new = 1 if (data.get("isNew") if "isNew" in data else existing["is_new"]) else 0
    is_featured = 1 if (data.get("isFeatured") if "isFeatured" in data else existing["is_featured"]) else 0
    is_active = 1 if (data.get("isActive") if "isActive" in data else existing["is_active"]) else 0
    collection = data.get("collection", existing["collection"])
    tag = data.get("tag", existing["tag"])
    short_desc = data.get("shortDesc", existing["short_desc"])
    description = data.get("description", existing["description"])
    materials = data.get("materials", existing["materials"])

    care = json.dumps(data["care"]) if "care" in data else existing["care"]
    details = json.dumps(data["details"]) if "details" in data else existing["details"]
    colors = json.dumps(data["colors"]) if "colors" in data else existing["colors"]
    sizes = json.dumps(data["sizes"]) if "sizes" in data else existing["sizes"]
    images = json.dumps(data["images"]) if "images" in data else existing["images"]

    execute_db(
        """UPDATE products SET name = ?, category = ?, gender = ?, price = ?, sale_price = ?, is_sale = ?, is_new = ?, is_featured = ?, is_active = ?, collection = ?, tag = ?, short_desc = ?, description = ?, materials = ?, care = ?, details = ?, colors = ?, sizes = ?, images = ?, updated_at = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (name, category, gender, price, sale_price, is_sale, is_new, is_featured, is_active, collection, tag, short_desc, description, materials, care, details, colors, sizes, images, product_id)
    )

    updated = query_db("SELECT * FROM products WHERE id = ?", (product_id,), one=True)
    return jsonify({"message": "Product updated successfully.", "product": format_product(updated)})

@product_bp.route("/<product_id>", methods=["DELETE"])
@role_required(["admin"])
def delete_product(current_user, product_id):
    existing = query_db("SELECT * FROM products WHERE id = ?", (product_id,), one=True)
    if not existing:
        return jsonify({"error": "Product not found."}), 404

    # Soft delete / toggle active
    execute_db("UPDATE products SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (product_id,))
    return jsonify({"message": f"Product {product_id} deactivated successfully."})
