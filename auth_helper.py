"""
BRI APPARELL — Authentication & Security Utilities
Session validation, token generation, role-based access decorators.
"""

import hmac
import hashlib
import base64
import json
import time
import os
from functools import wraps
from flask import request, jsonify, session
from database import query_db

SECRET_KEY = os.environ.get("SECRET_KEY", "bri-apparell-secret-token-key-2026")

def generate_token(user_id, email, role):
    """Creates a signed, tamper-proof bearer token with 7-day expiration."""
    payload = {
        "uid": user_id,
        "email": email,
        "role": role,
        "exp": int(time.time()) + (7 * 24 * 3600)
    }
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    signature = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
    return f"{payload_b64}.{signature}"

def verify_token(token):
    """Verifies a signed token and returns the payload dict or None if invalid/expired."""
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        payload_b64, signature = parts
        expected_sig = hmac.new(SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
        if payload.get("exp", 0) < int(time.time()):
            return None
        return payload
    except Exception:
        return None

def get_current_user():
    """Retrieves current user from Bearer header or Flask session."""
    auth_header = request.headers.get("Authorization")
    user_id = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if payload:
            user_id = payload.get("uid")

    if not user_id and "user_id" in session:
        user_id = session["user_id"]

    if not user_id:
        cookie_token = request.cookies.get("bri_token")
        if cookie_token:
            payload = verify_token(cookie_token)
            if payload:
                user_id = payload.get("uid")

    if not user_id:
        return None

    user = query_db(
        "SELECT id, email, full_name, phone, role, status, department, avatar_initials, street, city, province, postal_code, country FROM users WHERE id = ?",
        (user_id,),
        one=True
    )
    if user and user.get("status") == "Active":
        return user
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "Authentication required. Please sign in."}), 401
        return f(user, *args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({"error": "Authentication required. Please sign in."}), 401
            if user.get("role") not in allowed_roles:
                return jsonify({"error": "Access forbidden: insufficient permissions."}), 403
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator
