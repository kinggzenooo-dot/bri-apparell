-- =============================================================================
-- BRI APPARELL - PRODUCTION DATABASE SCHEMA (PostgreSQL Compatible)
-- Enterprise Retail & Apparel Management System
-- =============================================================================

-- Enable UUID extension if available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USERS & ROLES
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    role VARCHAR(50) NOT NULL DEFAULT 'customer', -- 'admin', 'staff', 'customer'
    status VARCHAR(50) NOT NULL DEFAULT 'Active', -- 'Active', 'Suspended', 'Inactive'
    department VARCHAR(100),
    avatar_initials VARCHAR(10),
    street TEXT,
    city VARCHAR(100),
    province VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(50) DEFAULT 'Philippines',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. CATEGORIES
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    image_url TEXT,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    gender VARCHAR(50) DEFAULT 'Unisex',
    price NUMERIC(10, 2) NOT NULL,
    sale_price NUMERIC(10, 2),
    is_sale BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    rating NUMERIC(3, 2) DEFAULT 5.0,
    review_count INTEGER DEFAULT 0,
    collection VARCHAR(100),
    tag VARCHAR(100),
    short_desc TEXT,
    description TEXT,
    materials TEXT,
    care TEXT,          -- JSON string or newline-delimited text
    details TEXT,       -- JSON string or newline-delimited text
    colors TEXT,        -- JSON string of [{name, hex}]
    sizes TEXT,         -- JSON string of [{size, inStock}]
    images TEXT,        -- JSON string of image URLs
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_collection ON products(collection);

-- 4. PRODUCT VARIANTS / INVENTORY
CREATE TABLE IF NOT EXISTS product_variants (
    id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sku VARCHAR(100) UNIQUE NOT NULL,
    color_name VARCHAR(100) NOT NULL,
    color_hex VARCHAR(20),
    size VARCHAR(20) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    threshold INTEGER NOT NULL DEFAULT 5,
    location VARCHAR(100) DEFAULT 'Main Warehouse - Bin 1',
    status VARCHAR(50) DEFAULT 'In Stock',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_variants_product ON product_variants(product_id);
CREATE INDEX IF NOT EXISTS idx_variants_sku ON product_variants(sku);

-- 5. INVENTORY STOCK LOGS
CREATE TABLE IF NOT EXISTS inventory_logs (
    id SERIAL PRIMARY KEY,
    variant_id VARCHAR(50) REFERENCES product_variants(id) ON DELETE SET NULL,
    product_id VARCHAR(50),
    change_type VARCHAR(50) NOT NULL, -- 'RESTOCK', 'ORDER_DEDUCTION', 'AUDIT_CORRECTION', 'RETURN'
    quantity_changed INTEGER NOT NULL,
    new_stock INTEGER NOT NULL,
    reason TEXT,
    performed_by VARCHAR(255) DEFAULT 'System',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. ORDERS
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(50) PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(50),
    shipping_address TEXT NOT NULL,
    city VARCHAR(100),
    province VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(50) DEFAULT 'Philippines',
    subtotal NUMERIC(10, 2) NOT NULL,
    discount NUMERIC(10, 2) DEFAULT 0,
    shipping_fee NUMERIC(10, 2) DEFAULT 0,
    total NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Placed', -- 'Placed', 'Confirmed', 'Processing', 'Packed', 'Ready to Ship', 'In Transit', 'Delivered', 'Cancelled'
    status_step INTEGER NOT NULL DEFAULT 1,
    payment_method VARCHAR(100) NOT NULL,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'Pending', -- 'Paid', 'Pending', 'Failed', 'Refunded'
    courier VARCHAR(100) DEFAULT 'LBC Express',
    tracking_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_email ON orders(customer_email);

-- 7. ORDER ITEMS
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id VARCHAR(50) REFERENCES products(id) ON DELETE SET NULL,
    variant_id VARCHAR(50),
    sku VARCHAR(100),
    product_name VARCHAR(255) NOT NULL,
    variant_name VARCHAR(100),
    size VARCHAR(20),
    color VARCHAR(50),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(10, 2) NOT NULL,
    total_price NUMERIC(10, 2) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);

-- 8. ORDER STATUS HISTORY AUDIT LOG
CREATE TABLE IF NOT EXISTS order_history (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    status VARCHAR(100) NOT NULL,
    notes TEXT,
    staff_name VARCHAR(255) DEFAULT 'System',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. PAYMENTS & TRANSACTIONS
CREATE TABLE IF NOT EXISTS payments (
    id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL,
    payment_method VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Completed', -- 'Completed', 'Pending', 'Failed', 'Refunded'
    reference_number VARCHAR(100),
    notes TEXT,
    paid_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. REVIEWS & RATINGS
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) REFERENCES products(id) ON DELETE CASCADE,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    comment TEXT NOT NULL,
    is_verified_purchase BOOLEAN DEFAULT TRUE,
    status VARCHAR(50) DEFAULT 'Approved', -- 'Approved', 'Pending', 'Flagged'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. NOTIFICATIONS
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_target VARCHAR(50) DEFAULT 'admin', -- 'all', 'admin', 'staff', 'customer'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'order', -- 'order', 'stock', 'customer', 'system'
    link VARCHAR(255),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. PROMO CODES
CREATE TABLE IF NOT EXISTS promo_codes (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_percent INTEGER DEFAULT 0,
    discount_fixed NUMERIC(10, 2) DEFAULT 0,
    description TEXT,
    min_spend NUMERIC(10, 2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. SYSTEM SETTINGS
CREATE TABLE IF NOT EXISTS system_settings (
    setting_key VARCHAR(100) PRIMARY KEY,
    setting_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
