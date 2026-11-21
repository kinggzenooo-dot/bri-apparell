"""
BRI APPARELL — Production Flask Application Server
Connects Customer Interface, Staff Operations, and Admin Dashboard to one centralized database.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from database import init_db
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.category_routes import category_bp
from routes.order_routes import order_bp
from routes.customer_routes import customer_bp
from routes.user_routes import user_bp
from routes.inventory_routes import inventory_bp
from routes.payment_routes import payment_bp
from routes.analytics_routes import analytics_bp
from routes.notification_routes import notification_bp
from routes.setting_routes import setting_bp, promo_bp
from routes.frontend_routes import frontend_bp

app = Flask(__name__, static_folder=None)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bri-apparell-production-secret-2026-secure")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Enable CORS for all API routes
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Register API blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(order_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(user_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(setting_bp)
app.register_blueprint(promo_bp)

# Register Frontend Blueprint
app.register_blueprint(frontend_bp)

# Health Check
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "BRI APPARELL Unified API Server",
        "version": "2.4.0",
        "environment": os.environ.get("FLASK_ENV", "production")
    })

# Global error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource or endpoint not found."}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "An internal server error occurred."}), 500

# Ensure database tables and initial records exist
with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"[STARTUP] Database init warning: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    print(f"==================================================")
    print(f" BRI APPARELL Server starting on http://localhost:{port}")
    print(f" Admin Dashboard:  http://localhost:{port}/admin/")
    print(f" Customer Store:   http://localhost:{port}/")
    print(f" Staff Interface:  http://localhost:{port}/staff/")
    print(f" Unified REST API: http://localhost:{port}/api/")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=debug)
