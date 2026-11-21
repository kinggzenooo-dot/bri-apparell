import re
from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import role_required

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")

@category_bp.route("", methods=["GET"])
def get_categories():
    categories = query_db("""
        SELECT c.*, COUNT(p.id) as product_count
        FROM categories c
        LEFT JOIN products p ON LOWER(p.category) = LOWER(c.name) AND p.is_active = 1
        WHERE c.is_active = 1
        GROUP BY c.id
        ORDER BY c.display_order ASC, c.name ASC
    """)
    return jsonify({"categories": categories})

@category_bp.route("", methods=["POST"])
@role_required(["admin"])
def create_category(current_user):
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    description = (data.get("description") or "").strip()
    image_url = data.get("image_url") or "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000"
    display_order = data.get("display_order", 0)

    if not name:
        return jsonify({"error": "Category name is required."}), 400

    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

    existing = query_db("SELECT id FROM categories WHERE LOWER(name) = LOWER(?) OR slug = ?", (name, slug), one=True)
    if existing:
        return jsonify({"error": "Category with this name or slug already exists."}), 409

    execute_db(
        "INSERT INTO categories (name, slug, description, image_url, display_order, is_active) VALUES (?, ?, ?, ?, ?, 1)",
        (name, slug, description, image_url, display_order)
    )

    cat = query_db("SELECT * FROM categories WHERE slug = ?", (slug,), one=True)
    return jsonify({"message": "Category created successfully.", "category": cat}), 201

@category_bp.route("/<int:cat_id>", methods=["PUT"])
@role_required(["admin"])
def update_category(current_user, cat_id):
    data = request.get_json() or {}
    existing = query_db("SELECT * FROM categories WHERE id = ?", (cat_id,), one=True)
    if not existing:
        return jsonify({"error": "Category not found."}), 404

    name = data.get("name", existing["name"]).strip()
    description = data.get("description", existing["description"])
    image_url = data.get("image_url", existing["image_url"])
    display_order = data.get("display_order", existing["display_order"])
    is_active = 1 if data.get("is_active", existing["is_active"]) else 0

    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

    execute_db(
        "UPDATE categories SET name = ?, slug = ?, description = ?, image_url = ?, display_order = ?, is_active = ? WHERE id = ?",
        (name, slug, description, image_url, display_order, is_active, cat_id)
    )

    cat = query_db("SELECT * FROM categories WHERE id = ?", (cat_id,), one=True)
    return jsonify({"message": "Category updated successfully.", "category": cat})

@category_bp.route("/<int:cat_id>", methods=["DELETE"])
@role_required(["admin"])
def delete_category(current_user, cat_id):
    existing = query_db("SELECT * FROM categories WHERE id = ?", (cat_id,), one=True)
    if not existing:
        return jsonify({"error": "Category not found."}), 404

    execute_db("DELETE FROM categories WHERE id = ?", (cat_id,))
    return jsonify({"message": f"Category {existing['name']} deleted."})
