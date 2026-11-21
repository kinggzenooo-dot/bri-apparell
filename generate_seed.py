import json
import re
from werkzeug.security import generate_password_hash

with open('initial_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])
promos = data.get('promo_codes', [])
staff_data = data.get('staff_data', {})
orders = staff_data.get('orders', [])
customers = staff_data.get('customers', [])
inventory = staff_data.get('inventoryVariants', [])
reviews = staff_data.get('reviews', [])
notifs = staff_data.get('notifications', [])
stock_hist = staff_data.get('stockHistory', [])

admin_hash = generate_password_hash('admin123')
staff_hash = generate_password_hash('staff123')
cust_hash = generate_password_hash('password123')

def escape_sql(val):
    if val is None:
        return 'NULL'
    if isinstance(val, bool):
        return 'TRUE' if val else 'FALSE'
    if isinstance(val, (int, float)):
        return str(val)
    # String
    s = str(val).replace("'", "''")
    return f"'{s}'"

lines = []
lines.append("-- =============================================================================")
lines.append("-- BRI APPARELL - PRODUCTION DATABASE SEED SCRIPT")
lines.append("-- =============================================================================")
lines.append("")

# 1. Users
lines.append("-- 1. USERS")
lines.append(f"INSERT INTO users (email, password_hash, full_name, phone, role, status, department, avatar_initials, street, city, province, postal_code, country, notes) VALUES")
lines.append(f"('admin@briapparell.com', '{admin_hash}', 'Administrator Vance', '+63 917 000 0001', 'admin', 'Active', 'Executive Management', 'AV', 'Unit 30A High Street South', 'Taguig', 'Metro Manila', '1634', 'Philippines', 'Chief System Administrator'),")
lines.append(f"('ops.admin@briapparell.com', '{admin_hash}', 'Elena Rostova', '+63 917 000 0002', 'admin', 'Active', 'Store Operations', 'ER', 'Greenbelt Residences', 'Makati', 'Metro Manila', '1229', 'Philippines', 'Operations Director'),")
lines.append(f"('alexander.vance@briapparell.com', '{staff_hash}', 'Alexander Vance', '+63 917 892 4567', 'staff', 'Active', 'Retail Operations & Logistics', 'AV', 'Unit 12C, Serendra Two', 'Taguig', 'Metro Manila', '1634', 'Philippines', 'EMP-0012 Senior Retail Staff'),")
lines.append(f"('maria.clara@briapparell.com', '{staff_hash}', 'Maria Clara', '+63 918 555 1234', 'staff', 'Active', 'Inventory & Fulfillment', 'MC', 'Salcedo Village', 'Makati', 'Metro Manila', '1227', 'Philippines', 'EMP-0015 Logistics Specialist'),")
lines.append(f"('john@email.com', '{cust_hash}', 'John Dela Cruz', '+63 917 123 4567', 'customer', 'Active', NULL, 'JD', 'Unit 14A, Grand Residences', 'Cebu City', 'Cebu', '6000', 'Philippines', 'VIP repeat client'),")
lines.append(f"('maria.santos@email.com', '{cust_hash}', 'Maria Santos', '+63 918 234 5678', 'customer', 'Active', NULL, 'MS', '74 Scout Rallos St.', 'Quezon City', 'Metro Manila', '1103', 'Philippines', 'COD verified client'),")
lines.append(f"('alexander.vance@example.com', '{cust_hash}', 'Alexander Vance', '+63 917 892 4567', 'customer', 'Active', NULL, 'AV', 'Unit 24B, Pacific Tower 1, 32nd St.', 'Taguig', 'Metro Manila', '1634', 'Philippines', 'Valued Customer'),")
lines.append(f"('sofia.rodriguez@email.com', '{cust_hash}', 'Sofia Rodriguez', '+63 919 345 6789', 'customer', 'Active', NULL, 'SR', 'Alveo Park Triangle', 'Taguig', 'Metro Manila', '1634', 'Philippines', 'Active online customer')")
lines.append("ON CONFLICT (email) DO NOTHING;")
lines.append("")

# 2. Categories
lines.append("-- 2. CATEGORIES")
categories = [
    ("Tops", "tops", "Heavyweight organic tees, relaxed shirts, and minimalist knits.", "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000", 1),
    ("Bottoms", "bottoms", "Tailored wide-leg trousers, relaxed shorts, and utilitarian bottoms.", "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?q=80&w=1000", 2),
    ("Outerwear", "outerwear", "Structured overshirts, kimono cardigans, and tailored trench coats.", "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?q=80&w=1000", 3),
    ("Accessories", "accessories", "Leather crossbodies, canvas totes, and raw metal jewelry.", "https://images.unsplash.com/photo-1544816155-12df9643f363?q=80&w=1000", 4),
    ("Footwear", "footwear", "Handcrafted leather derby shoes and minimalist slides.", "https://images.unsplash.com/photo-1549298916-b41d501d3772?q=80&w=1000", 5),
    ("Headwear", "headwear", "Low-profile twill caps and brushed wool beanies.", "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?q=80&w=1000", 6)
]
lines.append("INSERT INTO categories (name, slug, description, image_url, display_order) VALUES")
cat_vals = [f"({escape_sql(c[0])}, {escape_sql(c[1])}, {escape_sql(c[2])}, {escape_sql(c[3])}, {c[4]})" for c in categories]
lines.append(",\n".join(cat_vals))
lines.append("ON CONFLICT (slug) DO NOTHING;")
lines.append("")

# 3. Products
lines.append("-- 3. PRODUCTS")
prod_values = []
for p in products:
    p_id = p.get('id')
    p_name = p.get('name')
    p_cat = p.get('category')
    p_gender = p.get('gender', 'Unisex')
    p_price = p.get('price', 0)
    p_sale_price = p.get('salePrice')
    p_is_sale = p.get('isSale', False)
    p_is_new = p.get('isNew', False)
    p_is_feat = p.get('isFeatured', False)
    p_rating = p.get('rating', 5.0)
    p_rev_count = p.get('reviewCount', 0)
    p_coll = p.get('collection', '')
    p_tag = p.get('tag', '')
    p_short = p.get('shortDesc', '')
    p_desc = p.get('description', '')
    p_mat = p.get('materials', '')
    p_care = json.dumps(p.get('care', []))
    p_details = json.dumps(p.get('details', []))
    p_colors = json.dumps(p.get('colors', []))
    p_sizes = json.dumps(p.get('sizes', []))
    p_images = json.dumps(p.get('images', []))
    
    val_str = f"({escape_sql(p_id)}, {escape_sql(p_name)}, {escape_sql(p_cat)}, {escape_sql(p_gender)}, {p_price}, {escape_sql(p_sale_price)}, {escape_sql(p_is_sale)}, {escape_sql(p_is_new)}, {escape_sql(p_is_feat)}, {p_rating}, {p_rev_count}, {escape_sql(p_coll)}, {escape_sql(p_tag)}, {escape_sql(p_short)}, {escape_sql(p_desc)}, {escape_sql(p_mat)}, {escape_sql(p_care)}, {escape_sql(p_details)}, {escape_sql(p_colors)}, {escape_sql(p_sizes)}, {escape_sql(p_images)}, TRUE)"
    prod_values.append(val_str)

lines.append("INSERT INTO products (id, name, category, gender, price, sale_price, is_sale, is_new, is_featured, rating, review_count, collection, tag, short_desc, description, materials, care, details, colors, sizes, images, is_active) VALUES")
lines.append(",\n".join(prod_values))
lines.append("ON CONFLICT (id) DO NOTHING;")
lines.append("")

# 4. Product Variants (from inventoryVariants if available, or generate standard variants for each product)
lines.append("-- 4. PRODUCT VARIANTS / INVENTORY")
var_values = []
# First add from inventoryVariants in staff-data
seen_skus = set()
for var in inventory:
    v_id = var.get('id')
    v_pid = var.get('productId')
    v_sku = var.get('sku')
    if v_sku in seen_skus:
        continue
    seen_skus.add(v_sku)
    v_color = var.get('color', 'Standard')
    v_size = var.get('size', 'M')
    v_stock = var.get('stock', 10)
    v_thresh = var.get('threshold', 5)
    v_loc = var.get('location', 'Rack A-01')
    v_status = var.get('status', 'In Stock')
    var_values.append(f"({escape_sql(v_id)}, {escape_sql(v_pid)}, {escape_sql(v_sku)}, {escape_sql(v_color)}, '#000000', {escape_sql(v_size)}, {v_stock}, {v_thresh}, {escape_sql(v_loc)}, {escape_sql(v_status)})")

# For any products not in inventory, add default variants
for p in products:
    p_id = p.get('id')
    colors = p.get('colors', [{'name': 'Standard', 'hex': '#000000'}])
    sizes = p.get('sizes', [{'size': 'M', 'inStock': True}])
    for c in colors:
        for s in sizes:
            sku = f"BRI-{p_id.upper()}-{c['name'][:3].upper()}-{s['size']}"
            if sku not in seen_skus:
                seen_skus.add(sku)
                v_id = f"var-{len(seen_skus):03d}"
                var_values.append(f"({escape_sql(v_id)}, {escape_sql(p_id)}, {escape_sql(sku)}, {escape_sql(c['name'])}, {escape_sql(c.get('hex', '#000000'))}, {escape_sql(s['size'])}, 15, 5, 'Rack B-02', 'In Stock')")

lines.append("INSERT INTO product_variants (id, product_id, sku, color_name, color_hex, size, stock_quantity, threshold, location, status) VALUES")
lines.append(",\n".join(var_values))
lines.append("ON CONFLICT (id) DO NOTHING;")
lines.append("")

# 5. Promo Codes
lines.append("-- 5. PROMO CODES")
promo_vals = []
for pr in promos:
    p_code = pr.get('code')
    p_pct = pr.get('discountPercent', 0)
    p_fix = pr.get('discountFixed', 0)
    p_desc = pr.get('description', '')
    p_min = pr.get('minSpend', 0)
    promo_vals.append(f"({escape_sql(p_code)}, {p_pct}, {p_fix}, {escape_sql(p_desc)}, {p_min}, TRUE)")

lines.append("INSERT INTO promo_codes (code, discount_percent, discount_fixed, description, min_spend, is_active) VALUES")
lines.append(",\n".join(promo_vals))
lines.append("ON CONFLICT (code) DO NOTHING;")
lines.append("")

# 6. Orders & Order Items
lines.append("-- 6. ORDERS")
order_vals = []
item_vals = []
history_vals = []
payment_vals = []

for idx, o in enumerate(orders):
    o_id = o.get('orderId')
    cust = o.get('customer', {})
    c_name = cust.get('name', 'Valued Customer')
    c_email = cust.get('email', 'customer@example.com')
    c_phone = cust.get('phone', '+63 917 000 0000')
    c_addr = cust.get('address', 'Metro Manila, Philippines')
    date_val = o.get('date', '2026-08-24T12:00:00Z')
    status = o.get('status', 'Processing')
    step = o.get('statusStep', 3)
    pay_method = o.get('paymentMethod', 'GCASH')
    pay_status = o.get('paymentStatus', 'Paid')
    subtotal = o.get('subtotal', 2000)
    discount = o.get('discount', 0)
    ship_fee = o.get('shippingFee', 100)
    total = o.get('total', 2100)
    courier = o.get('courier', 'LBC Express')
    track = o.get('trackingNumber')
    notes = o.get('notes', '')
    
    order_vals.append(f"({escape_sql(o_id)}, {escape_sql(c_name)}, {escape_sql(c_email)}, {escape_sql(c_phone)}, {escape_sql(c_addr)}, 'Taguig', 'Metro Manila', '1634', 'Philippines', {subtotal}, {discount}, {ship_fee}, {total}, {escape_sql(status)}, {step}, {escape_sql(pay_method)}, {escape_sql(pay_status)}, {escape_sql(courier)}, {escape_sql(track)}, {escape_sql(notes)}, '{date_val}')")
    
    # Items
    for item in o.get('items', []):
        p_id = item.get('productId')
        sku = item.get('sku', '')
        name = item.get('name', '')
        variant = item.get('variant', 'Standard')
        size = item.get('size', 'M')
        qty = item.get('quantity', 1)
        price = item.get('price', 1000)
        tot = item.get('total', qty * price)
        item_vals.append(f"({escape_sql(o_id)}, {escape_sql(p_id)}, {escape_sql(sku)}, {escape_sql(name)}, {escape_sql(variant)}, {escape_sql(size)}, {qty}, {price}, {tot})")
        
    # History
    for h in o.get('history', []):
        h_time = h.get('time', date_val)
        h_ev = h.get('event', 'Order updated')
        h_staff = h.get('staff', 'System')
        history_vals.append(f"({escape_sql(o_id)}, {escape_sql(h_ev)}, {escape_sql(h_ev)}, {escape_sql(h_staff)}, '{h_time}')")
        
    # Payment
    txn_id = f"TXN-2026-{1000 + idx}"
    payment_vals.append(f"({escape_sql(txn_id)}, {escape_sql(o_id)}, {total}, {escape_sql(pay_method)}, {escape_sql(pay_status)}, {escape_sql(txn_id)}, '{date_val}')")

lines.append("INSERT INTO orders (id, customer_name, customer_email, customer_phone, shipping_address, city, province, postal_code, country, subtotal, discount, shipping_fee, total, status, status_step, payment_method, payment_status, courier, tracking_number, notes, created_at) VALUES")
lines.append(",\n".join(order_vals))
lines.append("ON CONFLICT (id) DO NOTHING;")
lines.append("")

if item_vals:
    lines.append("-- 7. ORDER ITEMS")
    lines.append("INSERT INTO order_items (order_id, product_id, sku, product_name, variant_name, size, quantity, unit_price, total_price) VALUES")
    lines.append(",\n".join(item_vals) + ";")
    lines.append("")

if history_vals:
    lines.append("-- 8. ORDER HISTORY")
    lines.append("INSERT INTO order_history (order_id, status, notes, staff_name, created_at) VALUES")
    lines.append(",\n".join(history_vals) + ";")
    lines.append("")

if payment_vals:
    lines.append("-- 9. PAYMENTS")
    lines.append("INSERT INTO payments (id, order_id, amount, payment_method, status, reference_number, paid_at) VALUES")
    lines.append(",\n".join(payment_vals))
    lines.append("ON CONFLICT (id) DO NOTHING;")
    lines.append("")

# 10. Reviews
lines.append("-- 10. REVIEWS")
rev_vals = []
for r in reviews:
    r_pid = r.get('productId')
    r_cust = r.get('customerName', 'Anonymous')
    r_rating = r.get('rating', 5)
    r_title = r.get('title', 'Great Quality')
    r_comm = r.get('comment', 'Love this product!')
    r_stat = r.get('status', 'Approved')
    r_date = r.get('date', '2026-08-20T10:00:00Z')
    rev_vals.append(f"({escape_sql(r_pid)}, {escape_sql(r_cust)}, {r_rating}, {escape_sql(r_title)}, {escape_sql(r_comm)}, TRUE, {escape_sql(r_stat)}, '{r_date}')")

if rev_vals:
    lines.append("INSERT INTO reviews (product_id, customer_name, rating, title, comment, is_verified_purchase, status, created_at) VALUES")
    lines.append(",\n".join(rev_vals) + ";")
    lines.append("")

# 11. Notifications
lines.append("-- 11. NOTIFICATIONS")
notif_vals = []
for n in notifs:
    n_title = n.get('title', 'Notification')
    n_msg = n.get('message', '')
    n_type = n.get('type', 'system')
    n_read = n.get('read', False)
    n_time = n.get('time', '2026-08-24T12:00:00Z')
    notif_vals.append(f"('admin', {escape_sql(n_title)}, {escape_sql(n_msg)}, {escape_sql(n_type)}, {escape_sql(n_read)}, '{n_time}')")

if notif_vals:
    lines.append("INSERT INTO notifications (role_target, title, message, type, is_read, created_at) VALUES")
    lines.append(",\n".join(notif_vals) + ";")
    lines.append("")

# 12. System Settings
lines.append("-- 12. SYSTEM SETTINGS")
settings = [
    ("store_name", "BRI APPARELL", "Brand and retail legal entity name"),
    ("store_tagline", "Refined Architectural Silhouettes & Essential Streetwear", "Brand subtitle"),
    ("store_email", "concierge@briapparell.com", "Primary customer support email"),
    ("store_phone", "+63 917 892 4567", "Customer concierge hotline"),
    ("currency_code", "PHP", "Store currency code"),
    ("currency_symbol", "₱", "Philippine Peso currency symbol"),
    ("free_shipping_threshold", "2500", "Cart minimum for automatic free shipping nationwide"),
    ("standard_shipping_fee", "150", "Standard flat shipping rate in PHP"),
    ("express_shipping_fee", "280", "Express door-to-door courier fee in PHP"),
    ("tax_rate", "0.12", "Value Added Tax (12% VAT in Philippines)"),
    ("maintenance_mode", "false", "Storefront maintenance mode switch"),
    ("allow_guest_checkout", "true", "Permit order placement without mandatory registration")
]
lines.append("INSERT INTO system_settings (setting_key, setting_value, description) VALUES")
s_vals = [f"({escape_sql(s[0])}, {escape_sql(s[1])}, {escape_sql(s[2])})" for s in settings]
lines.append(",\n".join(s_vals))
lines.append("ON CONFLICT (setting_key) DO NOTHING;")
lines.append("")

with open('seed.sql', 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print("Successfully generated seed.sql!")
