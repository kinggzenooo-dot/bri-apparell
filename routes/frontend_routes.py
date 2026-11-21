import os
from flask import Blueprint, send_from_directory, redirect, request
from auth_helper import get_current_user

frontend_bp = Blueprint("frontend", __name__)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# -----------------------------------------------------------------------------
# 1. MAIN ENTRY POINT (WEBSITE ROOT)
# -----------------------------------------------------------------------------
@frontend_bp.route("/", methods=["GET"])
def index():
    """
    Main website entry point.
    If unauthenticated, displays the centralized Login & Sign-Up interface first.
    If authenticated:
      - Customer -> Customer Home Dashboard (index.html)
      - Staff -> Staff Dashboard (/staff/dashboard.html)
      - Administrator -> Admin Dashboard (/admin/index.html)
    """
    user = get_current_user()
    if not user:
        return redirect("/authorization/login.html")

    if user.get("role") == "admin":
        return redirect("/admin/index.html")
    elif user.get("role") == "staff":
        return redirect("/staff/dashboard.html")
    else:
        return send_from_directory(ROOT_DIR, "index.html")

# -----------------------------------------------------------------------------
# 2. CENTRALIZED AUTHORIZATION PORTAL (/authorization)
# -----------------------------------------------------------------------------
@frontend_bp.route("/authorization", methods=["GET"])
@frontend_bp.route("/authorization/", methods=["GET"])
def auth_root():
    return redirect("/authorization/login.html")

@frontend_bp.route("/authorization/<path:filename>", methods=["GET"])
def auth_files(filename):
    auth_dir = os.path.join(ROOT_DIR, "authorization")
    if os.path.exists(os.path.join(auth_dir, filename)):
        return send_from_directory(auth_dir, filename)
    if not filename.endswith(".html") and os.path.exists(os.path.join(auth_dir, filename + ".html")):
        return send_from_directory(auth_dir, filename + ".html")
    return redirect("/authorization/login.html")

# -----------------------------------------------------------------------------
# 3. EXECUTIVE ADMIN PORTAL (/admin)
# -----------------------------------------------------------------------------
@frontend_bp.route("/admin", methods=["GET"])
def admin_redirect():
    return redirect("/admin/")

@frontend_bp.route("/admin/", methods=["GET"])
def admin_root():
    user = get_current_user()
    if not user or user.get("role") != "admin":
        return redirect("/authorization/login.html?redirect=/admin/index.html&reason=admin_required")
    admin_dir = os.path.join(ROOT_DIR, "admin")
    return send_from_directory(admin_dir, "index.html")

@frontend_bp.route("/admin/<path:filename>", methods=["GET"])
def admin_files(filename):
    admin_dir = os.path.join(ROOT_DIR, "admin")

    # Static assets (css, js, images) can be served directly
    if any(filename.endswith(ext) for ext in [".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico"]):
        if os.path.exists(os.path.join(admin_dir, filename)):
            return send_from_directory(admin_dir, filename)

    # Legacy admin login redirects to centralized auth portal
    if filename in ["login.html", "login"]:
        return redirect("/authorization/login.html?redirect=/admin/index.html&reason=admin_required")

    # Enforce admin authentication on all admin pages
    user = get_current_user()
    if not user or user.get("role") != "admin":
        return redirect(f"/authorization/login.html?redirect=/admin/{filename}&reason=admin_required")

    if os.path.exists(os.path.join(admin_dir, filename)):
        return send_from_directory(admin_dir, filename)
    if not filename.endswith(".html") and os.path.exists(os.path.join(admin_dir, filename + ".html")):
        return send_from_directory(admin_dir, filename + ".html")

    return send_from_directory(admin_dir, "index.html")

# -----------------------------------------------------------------------------
# 4. STAFF OPERATIONS PORTAL (/staff)
# -----------------------------------------------------------------------------
@frontend_bp.route("/staff", methods=["GET"])
def staff_redirect():
    return redirect("/staff/")

@frontend_bp.route("/staff/", methods=["GET"])
def staff_root():
    user = get_current_user()
    if not user or user.get("role") not in ["staff", "admin"]:
        return redirect("/authorization/login.html?redirect=/staff/dashboard.html&reason=staff_required")
    staff_dir = os.path.join(ROOT_DIR, "staff")
    return send_from_directory(staff_dir, "dashboard.html")

@frontend_bp.route("/staff/<path:filename>", methods=["GET"])
def staff_files(filename):
    staff_dir = os.path.join(ROOT_DIR, "staff")

    # Static assets
    if any(filename.endswith(ext) for ext in [".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico"]):
        if os.path.exists(os.path.join(staff_dir, filename)):
            return send_from_directory(staff_dir, filename)

    # Enforce staff/admin authentication on all staff pages
    user = get_current_user()
    if not user or user.get("role") not in ["staff", "admin"]:
        return redirect(f"/authorization/login.html?redirect=/staff/{filename}&reason=staff_required")

    if os.path.exists(os.path.join(staff_dir, filename)):
        return send_from_directory(staff_dir, filename)
    if not filename.endswith(".html") and os.path.exists(os.path.join(staff_dir, filename + ".html")):
        return send_from_directory(staff_dir, filename + ".html")

    return send_from_directory(staff_dir, "dashboard.html")

# -----------------------------------------------------------------------------
# 5. PROTECTED CUSTOMER PAGES & STOREFRONT ASSETS
# -----------------------------------------------------------------------------
@frontend_bp.route("/css/<path:filename>", methods=["GET"])
def css_files(filename):
    css_dir = os.path.join(ROOT_DIR, "css")
    if os.path.exists(os.path.join(css_dir, filename)):
        return send_from_directory(css_dir, filename)
    return "", 404

@frontend_bp.route("/js/<path:filename>", methods=["GET"])
def js_files(filename):
    js_dir = os.path.join(ROOT_DIR, "js")
    if os.path.exists(os.path.join(js_dir, filename)):
        return send_from_directory(js_dir, filename)
    return "", 404

@frontend_bp.route("/<path:filename>", methods=["GET"])
def customer_files(filename):
    # Customer core assets and admin fallback resolution
    if filename in ["styles.css", "script.js", "products.js", "favicon.ico"]:
        if os.path.exists(os.path.join(ROOT_DIR, filename)):
            return send_from_directory(ROOT_DIR, filename)

    if filename in ["css/admin.css", "admin.css"]:
        admin_css = os.path.join(ROOT_DIR, "admin", "css", "admin.css")
        if os.path.exists(admin_css):
            return send_from_directory(os.path.join(ROOT_DIR, "admin", "css"), "admin.css")

    if filename in ["js/admin.js", "admin.js"]:
        admin_js = os.path.join(ROOT_DIR, "admin", "js", "admin.js")
        if os.path.exists(admin_js):
            return send_from_directory(os.path.join(ROOT_DIR, "admin", "js"), "admin.js")

    # Protected Customer Pages: account.html, checkout.html, and direct index.html access
    if filename in ["account.html", "checkout.html", "index.html"]:
        user = get_current_user()
        if not user:
            reason = "checkout" if filename == "checkout.html" else "login_required"
            return redirect(f"/authorization/login.html?redirect={filename}&reason={reason}")

    # Storefront HTML files
    if filename.endswith(".html") and os.path.exists(os.path.join(ROOT_DIR, filename)):
        return send_from_directory(ROOT_DIR, filename)

    if not filename.endswith(".html") and os.path.exists(os.path.join(ROOT_DIR, filename + ".html")):
        target = filename + ".html"
        if target in ["account.html", "checkout.html"]:
            user = get_current_user()
            if not user:
                return redirect(f"/authorization/login.html?redirect={target}")
        return send_from_directory(ROOT_DIR, target)

    # Subdirectories check (e.g. images, assets)
    if os.path.exists(os.path.join(ROOT_DIR, filename)):
        return send_from_directory(ROOT_DIR, filename)

    # Fallback to authorization gateway
    return redirect("/authorization/login.html")
