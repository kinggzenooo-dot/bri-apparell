"""
BRI APPARELL — Centralized Database Layer
Supports PostgreSQL (Render / Supabase / Neon) with seamless SQLite local fallback.
Provides thread-safe connections, dict-like cursors, parameterized queries, and auto-initialization.
"""

import os
import re
import json
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "bri_apparel.db")
USE_POSTGRES = False

if DATABASE_URL:
    try:
        import psycopg2
        import psycopg2.extras
        # Test connection
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        USE_POSTGRES = True
        print("[DATABASE] Successfully connected to PostgreSQL database.")
    except Exception as e:
        print(f"[DATABASE] PostgreSQL connection attempt failed ({e}). Falling back to local SQLite.")
        USE_POSTGRES = False
else:
    print("[DATABASE] No DATABASE_URL specified. Running with SQLite database engine.")

def get_connection():
    """Returns a raw database connection object."""
    if USE_POSTGRES:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        return conn
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

def format_query(sql):
    """Adapts query parameter placeholders (? vs %s) based on active DB backend."""
    if USE_POSTGRES:
        # Convert SQLite style ? to PostgreSQL %s
        return sql.replace("?", "%s")
    else:
        # Convert PostgreSQL style %s to SQLite ?
        # Be careful not to replace format specifiers like '%Y-%m-%d'
        formatted = re.sub(r'(?<!%)(%s)', '?', sql)
        # SQLite doesn't use ON CONFLICT (col) DO NOTHING without unique index in some versions,
        # but in SQLite 3.24+ it does. SQLite also handles INSERT OR IGNORE.
        return formatted

def query_db(sql, args=(), one=False):
    """Executes a SELECT query and returns a list of dictionaries (or a single dict)."""
    conn = get_connection()
    adapted_sql = format_query(sql)
    try:
        if USE_POSTGRES:
            import psycopg2.extras
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(adapted_sql, args)
                rows = cur.fetchall()
                result = [dict(row) for row in rows]
                return (result[0] if result else None) if one else result
        else:
            cur = conn.cursor()
            cur.execute(adapted_sql, args)
            rows = cur.fetchall()
            result = [dict(row) for row in rows]
            return (result[0] if result else None) if one else result
    finally:
        conn.close()

def execute_db(sql, args=(), commit=True):
    """Executes an INSERT, UPDATE, or DELETE query."""
    conn = get_connection()
    adapted_sql = format_query(sql)
    last_id = None
    rowcount = 0
    try:
        if USE_POSTGRES:
            with conn.cursor() as cur:
                cur.execute(adapted_sql, args)
                rowcount = cur.rowcount
                try:
                    if "RETURNING" in adapted_sql.upper():
                        last_id = cur.fetchone()[0]
                except Exception:
                    pass
            if commit:
                conn.commit()
        else:
            cur = conn.cursor()
            cur.execute(adapted_sql, args)
            rowcount = cur.rowcount
            last_id = cur.lastrowid
            if commit:
                conn.commit()
        return {"last_id": last_id, "rowcount": rowcount}
    except Exception as e:
        if commit:
            conn.rollback()
        raise e
    finally:
        conn.close()

def init_db(force_seed=False):
    """
    Initializes database tables and seeds initial catalog & admin accounts.
    Idempotent: safe to run on startup.
    """
    conn = get_connection()
    try:
        if USE_POSTGRES:
            schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
            seed_file = os.path.join(os.path.dirname(__file__), "seed.sql")
            with conn.cursor() as cur:
                if os.path.exists(schema_file):
                    with open(schema_file, "r", encoding="utf-8") as f:
                        cur.execute(f.read())
                # Check if products exist
                cur.execute("SELECT COUNT(*) FROM products;")
                count = cur.fetchone()[0]
                if count == 0 or force_seed:
                    print("[DATABASE] Seeding initial PostgreSQL data...")
                    if os.path.exists(seed_file):
                        with open(seed_file, "r", encoding="utf-8") as f:
                            cur.execute(f.read())
            conn.commit()
        else:
            # SQLite Table definitions
            cur = conn.cursor()
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT,
                role TEXT NOT NULL DEFAULT 'customer',
                status TEXT NOT NULL DEFAULT 'Active',
                department TEXT,
                avatar_initials TEXT,
                street TEXT,
                city TEXT,
                province TEXT,
                postal_code TEXT,
                country TEXT DEFAULT 'Philippines',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                description TEXT,
                image_url TEXT,
                display_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                gender TEXT DEFAULT 'Unisex',
                price NUMERIC NOT NULL,
                sale_price NUMERIC,
                is_sale INTEGER DEFAULT 0,
                is_new INTEGER DEFAULT 0,
                is_featured INTEGER DEFAULT 0,
                rating NUMERIC DEFAULT 5.0,
                review_count INTEGER DEFAULT 0,
                collection TEXT,
                tag TEXT,
                short_desc TEXT,
                description TEXT,
                materials TEXT,
                care TEXT,
                details TEXT,
                colors TEXT,
                sizes TEXT,
                images TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS product_variants (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                sku TEXT UNIQUE NOT NULL,
                color_name TEXT NOT NULL,
                color_hex TEXT,
                size TEXT NOT NULL,
                stock_quantity INTEGER NOT NULL DEFAULT 0,
                threshold INTEGER NOT NULL DEFAULT 5,
                location TEXT DEFAULT 'Main Warehouse - Bin 1',
                status TEXT DEFAULT 'In Stock',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS inventory_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variant_id TEXT,
                product_id TEXT,
                change_type TEXT NOT NULL,
                quantity_changed INTEGER NOT NULL,
                new_stock INTEGER NOT NULL,
                reason TEXT,
                performed_by TEXT DEFAULT 'System',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_phone TEXT,
                shipping_address TEXT NOT NULL,
                city TEXT,
                province TEXT,
                postal_code TEXT,
                country TEXT DEFAULT 'Philippines',
                subtotal NUMERIC NOT NULL,
                discount NUMERIC DEFAULT 0,
                shipping_fee NUMERIC DEFAULT 0,
                total NUMERIC NOT NULL,
                status TEXT NOT NULL DEFAULT 'Placed',
                status_step INTEGER NOT NULL DEFAULT 1,
                payment_method TEXT NOT NULL,
                payment_status TEXT NOT NULL DEFAULT 'Pending',
                courier TEXT DEFAULT 'LBC Express',
                tracking_number TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                product_id TEXT REFERENCES products(id) ON DELETE SET NULL,
                variant_id TEXT,
                sku TEXT,
                product_name TEXT NOT NULL,
                variant_name TEXT,
                size TEXT,
                color TEXT,
                quantity INTEGER NOT NULL DEFAULT 1,
                unit_price NUMERIC NOT NULL,
                total_price NUMERIC NOT NULL
            );

            CREATE TABLE IF NOT EXISTS order_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                status TEXT NOT NULL,
                notes TEXT,
                staff_name TEXT DEFAULT 'System',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                amount NUMERIC NOT NULL,
                payment_method TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Completed',
                reference_number TEXT,
                notes TEXT,
                paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT REFERENCES products(id) ON DELETE CASCADE,
                customer_name TEXT NOT NULL,
                customer_email TEXT,
                rating INTEGER NOT NULL,
                title TEXT,
                comment TEXT NOT NULL,
                is_verified_purchase INTEGER DEFAULT 1,
                status TEXT DEFAULT 'Approved',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                role_target TEXT DEFAULT 'admin',
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'order',
                link TEXT,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS promo_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                discount_percent INTEGER DEFAULT 0,
                discount_fixed NUMERIC DEFAULT 0,
                description TEXT,
                min_spend NUMERIC DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS system_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Check if products exist in SQLite
            cur.execute("SELECT COUNT(*) FROM products;")
            count = cur.fetchone()[0]
            if count == 0 or force_seed:
                print("[DATABASE] Seeding SQLite database from seed.sql...")
                seed_file = os.path.join(os.path.dirname(__file__), "seed.sql")
                if os.path.exists(seed_file):
                    with open(seed_file, "r", encoding="utf-8") as f:
                        seed_sql = f.read()
                    # Execute statements
                    # Replace boolean literals if needed
                    seed_sql_sqlite = seed_sql.replace("TRUE", "1").replace("FALSE", "0")
                    # SQLite supports ON CONFLICT (col) DO NOTHING in modern versions
                    try:
                        cur.executescript(seed_sql_sqlite)
                    except Exception as seed_err:
                        print(f"[DATABASE] Script execution warning: {seed_err}")
            conn.commit()
        print("[DATABASE] Initialization verified successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
