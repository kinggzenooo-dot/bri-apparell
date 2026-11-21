import os
from flask import Blueprint, send_from_directory, redirect

frontend_bp = Blueprint("frontend", __name__)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Serve customer root
@frontend_bp.route("/", methods=["GET"])
def index():
    return send_from_directory(ROOT_DIR, "index.html")

# Serve customer HTML files
@frontend_bp.route("/<path:filename>", methods=["GET"])
def customer_files(filename):
    if filename.endswith(".html") and os.path.exists(os.path.join(ROOT_DIR, filename)):
        return send_from_directory(ROOT_DIR, filename)
    if filename in ["styles.css", "script.js", "products.js", "favicon.ico"]:
        return send_from_directory(ROOT_DIR, filename)
    # Check if inside css or js
    if os.path.exists(os.path.join(ROOT_DIR, filename)):
        return send_from_directory(ROOT_DIR, filename)
    return send_from_directory(ROOT_DIR, "index.html")

# Serve Admin portal
@frontend_bp.route("/admin", methods=["GET"])
@frontend_bp.route("/admin/", methods=["GET"])
def admin_root():
    admin_dir = os.path.join(ROOT_DIR, "admin")
    if os.path.exists(os.path.join(admin_dir, "index.html")):
        return send_from_directory(admin_dir, "index.html")
    return send_from_directory(admin_dir, "dashboard.html")

@frontend_bp.route("/admin/<path:filename>", methods=["GET"])
def admin_files(filename):
    admin_dir = os.path.join(ROOT_DIR, "admin")
    if os.path.exists(os.path.join(admin_dir, filename)):
        return send_from_directory(admin_dir, filename)
    # If not found but is html
    if not filename.endswith(".html") and os.path.exists(os.path.join(admin_dir, filename + ".html")):
        return send_from_directory(admin_dir, filename + ".html")
    return send_from_directory(admin_dir, "index.html")

# Serve Staff portal
@frontend_bp.route("/staff", methods=["GET"])
@frontend_bp.route("/staff/", methods=["GET"])
def staff_root():
    staff_dir = os.path.join(ROOT_DIR, "staff")
    return send_from_directory(staff_dir, "dashboard.html")

@frontend_bp.route("/staff/<path:filename>", methods=["GET"])
def staff_files(filename):
    staff_dir = os.path.join(ROOT_DIR, "staff")
    if os.path.exists(os.path.join(staff_dir, filename)):
        return send_from_directory(staff_dir, filename)
    if not filename.endswith(".html") and os.path.exists(os.path.join(staff_dir, filename + ".html")):
        return send_from_directory(staff_dir, filename + ".html")
    return send_from_directory(staff_dir, "dashboard.html")
