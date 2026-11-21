from flask import Blueprint, request, jsonify
from database import query_db, execute_db
from auth_helper import role_required

setting_bp = Blueprint("settings", __name__, url_prefix="/api/settings")
promo_bp = Blueprint("promotions", __name__, url_prefix="/api/promotions")

@setting_bp.route("", methods=["GET"])
def get_settings():
    rows = query_db("SELECT setting_key, setting_value, description FROM system_settings")
    settings_dict = {r["setting_key"]: r["setting_value"] for r in rows}
    return jsonify({"settings": settings_dict, "raw": rows})

@setting_bp.route("", methods=["PUT"])
@role_required(["admin"])
def update_settings(current_user):
    data = request.get_json() or {}
    for key, val in data.items():
        execute_db(
            "UPDATE system_settings SET setting_value = ?, updated_at = CURRENT_TIMESTAMP WHERE setting_key = ?",
            (str(val), key)
        )
    return jsonify({"message": "System settings updated successfully."})

# --- PROMOTIONS ---
@promo_bp.route("", methods=["GET"])
def get_promos():
    promos = query_db("SELECT * FROM promo_codes WHERE is_active = 1")
    return jsonify({"promotions": promos})

@promo_bp.route("/apply", methods=["POST"])
def apply_promo():
    data = request.get_json() or {}
    code = (data.get("code") or "").strip().upper()
    subtotal = float(data.get("subtotal", 0.0))

    if not code:
        return jsonify({"error": "Promo code is required."}), 400

    promo = query_db("SELECT * FROM promo_codes WHERE UPPER(code) = UPPER(?) AND is_active = 1", (code,), one=True)
    if not promo:
        return jsonify({"error": "Invalid or expired promo code."}), 404

    min_spend = float(promo.get("min_spend", 0.0))
    if subtotal < min_spend:
        return jsonify({"error": f"Code requires minimum purchase of ₱{min_spend:,.0f}."}), 400

    discount = 0.0
    if promo.get("discount_percent") and promo["discount_percent"] > 0:
        discount = (subtotal * promo["discount_percent"]) / 100.0
    elif promo.get("discount_fixed") and promo["discount_fixed"] > 0:
        discount = float(promo["discount_fixed"])

    return jsonify({
        "success": True,
        "code": promo["code"],
        "description": promo["description"],
        "discount": round(discount, 2),
        "message": f"Promo code {promo['code']} applied successfully!"
    })

@promo_bp.route("", methods=["POST"])
@role_required(["admin"])
def create_promo(current_user):
    data = request.get_json() or {}
    code = (data.get("code") or "").strip().upper()
    discount_pct = int(data.get("discount_percent", 0))
    discount_fix = float(data.get("discount_fixed", 0))
    desc = data.get("description", "")
    min_spend = float(data.get("min_spend", 0))

    if not code:
        return jsonify({"error": "Promo code is required."}), 400

    existing = query_db("SELECT id FROM promo_codes WHERE UPPER(code) = UPPER(?)", (code,), one=True)
    if existing:
        return jsonify({"error": "Promo code already exists."}), 409

    execute_db(
        "INSERT INTO promo_codes (code, discount_percent, discount_fixed, description, min_spend, is_active) VALUES (?, ?, ?, ?, ?, 1)",
        (code, discount_pct, discount_fix, desc, min_spend)
    )

    created = query_db("SELECT * FROM promo_codes WHERE UPPER(code) = UPPER(?)", (code,), one=True)
    return jsonify({"message": "Promo code created successfully.", "promo": created}), 201

@promo_bp.route("/<int:promo_id>", methods=["DELETE"])
@role_required(["admin"])
def delete_promo(current_user, promo_id):
    execute_db("DELETE FROM promo_codes WHERE id = ?", (promo_id,))
    return jsonify({"message": "Promo code deleted."})
