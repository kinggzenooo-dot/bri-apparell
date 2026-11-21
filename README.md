# BRI APPARELL — Enterprise Web Application & Operations Platform

> **Refined Architectural Streetwear & Contemporary Retail Management System**  
> Complete Full-Stack Solution: Customer Storefront, Executive Admin Console, Staff Operations Engine, Python Flask REST API, and Centralized PostgreSQL Database.

---

## 1. Project Overview

**BRI APPARELL** is an end-to-end luxury streetwear e-commerce platform crafted with architectural aesthetics, high-performance responsive frontend design, and a production-grade Python backend. The application unifies all retail operations under **one single source of truth**, synchronizing customer purchases, admin inventory management, staff fulfillment, and payment gateways in real-time.

### Key Highlights
- **Unified Centralized Database**: Powered by PostgreSQL (with automatic local SQLite fallback) storing users, products, variants, orders, payments, reviews, notifications, and settings.
- **Executive Admin Console (`/admin`)**: Complete management suite for system administrators with full CRUD capabilities across all business records.
- **Enhanced Customer Storefront (`/`)**: Curated editorial catalog, interactive product configurator, dynamic shopping bag, voucher discounts, instant checkout, and real-time 4-stage delivery tracking.
- **Staff Operations Hub (`/staff`)**: Dedicated fulfillment workspace for warehouse and logistics associates with SKU variant stock adjustments and order processing.
- **Enterprise Security**: Role-based access control (RBAC), scrypt password hashing, HMAC-SHA256 session tokens, parameterized SQL queries, and zero hardcoded production secrets.

---

## 2. System Architecture

```
                       ┌─────────────────────────┐
                       │   CUSTOMER STOREFRONT   │
                       │   (shop, cart, account) │
                       └────────────┬────────────┘
                                    │
                                    ▼
┌──────────────────────┐   ┌─────────────────┐   ┌──────────────────────┐
│  EXECUTIVE ADMIN     │   │  PYTHON FLASK   │   │   STAFF OPERATIONS   │
│  DASHBOARD (/admin)  ├──►│ UNIFIED REST API│◄──┤   PORTAL (/staff)    │
└──────────────────────┘   └────────┬────────┘   └──────────────────────┘
                                    │
                                    ▼
                       ┌─────────────────────────┐
                       │   CENTRALIZED DATABASE  │
                       │   PostgreSQL / SQLite   │
                       └─────────────────────────┘
```

---

## 3. Core Modules & Functionality

### A. Executive Admin Console (`admin/`)
Located in the designated `admin/` directory:
1. **Dashboard Overview (`index.html`)**: Real-time KPI cards (Gross Revenue, Total Orders, Active Customers, AOV, Low Stock Alerts), sales by category, status distribution, and recent orders.
2. **User Management (`users.html`)**: Add, edit, deactivate, and reset passwords for administrators, staff, and customers.
3. **Customer Directory (`customers.html`)**: View customer order frequency, lifetime spend, verified delivery locations, and internal admin notes.
4. **Product Catalog (`products.html`)**: Full CRUD product management with image previews, category mapping, price rules, sale flags, and automatic SKU variant generation.
5. **Category Taxonomy (`categories.html`)**: Create and organize apparel departments with real-time product counts.
6. **Orders & Transactions (`orders.html` & `order-details.html`)**: Live order fulfillment dropdown, courier assignment, tracking numbers, packing slip printing, and payment verification.
7. **Inventory & Stock (`inventory.html`)**: Monitor stock counts per size and color variant, set reorder thresholds, and execute logged restocks with audit history.
8. **Payments (`payments.html`)**: Transaction records across GCash, Maya, Cards, and COD, with one-click payment verification and refund processing.
9. **Reports & Analytics (`reports.html`)**: Printable financial reports, turnover by department, top silhouettes, and average order value.
10. **Notifications Center (`notifications.html`)**: Alert feed for order events, low-stock warnings, and member registrations.
11. **System Settings (`settings.html`)**: Store concierge contacts, currency symbols, shipping fees, tax rates, and maintenance mode.
12. **Admin Profile (`profile.html`)**: Update administrative profile and change passwords with current-password verification.

### B. Enhanced Customer Storefront
- **Editorial Experience**: Clean monochromatic aesthetic, typography hierarchy, and smooth hover micro-animations.
- **Dynamic Database Synchronization**: Automatically queries `/api/products` and `/api/promotions` so catalog changes made in the Admin Console reflect on the storefront instantly.
- **Encrypted Checkout**: Supports GCash, Maya, Credit/Debit cards, Cash on Delivery, and promo voucher discounts (`BRIFIRST10`, `FREESHIP2500`).
- **Interactive Delivery Tracker**: Real-time timeline (Placed &rarr; Confirmed &rarr; Processing &rarr; In Transit &rarr; Delivered) updated whenever staff or admins change order status.

---

## 4. SQL Database Schema

The database is defined in `schema.sql` and initialized with production seeds from `seed.sql`:

| Table | Description | Key Relationships |
|---|---|---|
| `users` | Accounts, roles (admin, staff, customer), addresses, hashed credentials | Master table |
| `categories` | Apparel taxonomies and display order | One-to-Many with `products` |
| `products` | Garment catalog, pricing, materials, care, and images | Master catalog |
| `product_variants` | Multi-variant SKUs, sizes, colors, and stock counts | References `products(id)` |
| `inventory_logs` | Audit trail of all restocks and order deductions | References `product_variants(id)` |
| `orders` | Customer purchases, shipping address, totals, and courier status | References `users(id)` |
| `order_items` | Line items with size, color, quantity, and unit price | References `orders(id)`, `products(id)` |
| `order_history` | Audit log of status transitions and staff actions | References `orders(id)` |
| `payments` | Financial settlements, payment methods, and reference numbers | References `orders(id)` |
| `reviews` | Customer ratings and verified feedback | References `products(id)` |
| `notifications` | Real-time system alerts targeted by role | Filtered by `role_target` |
| `system_settings` | Global store settings and fiscal rules | Key-value store |
| `promo_codes` | Discount codes with spend thresholds | Checked on checkout |

---

## 5. Development & Local Setup

### Prerequisites
- Python 3.10+
- Modern Web Browser

### Installation Steps

```bash
# 1. Clone repository
git clone https://github.com/kinggzenooo-dot/bri-apparell.git
cd bri-apparell

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate # macOS/Linux

# 3. Install packages
pip install -r requirements.txt

# 4. Initialize Database
python database.py

# 5. Run the Automated Test Suite (All 9 Tests)
python test_system.py

# 6. Start Development Server
python app.py
```

Open your browser:
- **Customer Storefront**: `http://localhost:5000/`
- **Admin Console**: `http://localhost:5000/admin/login.html`
- **Staff Operations**: `http://localhost:5000/staff/dashboard.html`
- **REST API Health**: `http://localhost:5000/api/health`

### Development Credentials
- **Admin**: `admin@briapparell.com` / `admin123`
- **Ops Admin**: `ops.admin@briapparell.com` / `admin123`
- **Staff**: `alexander.vance@briapparell.com` / `staff123`
- **Customer**: `john@email.com` / `password123`

---

## 6. Render Deployment Guide

The repository includes a `render.yaml` Blueprint and `Procfile` configured for deployment on Render.

### Option A: Automatic Blueprint Deployment (Recommended)
1. In the **Render Dashboard**, click **New +** &rarr; **Blueprint**.
2. Connect your GitHub repository: `kinggzenooo-dot/bri-apparell`.
3. Render will read `render.yaml` and provision:
   - A **Web Service** (`gunicorn app:app`).
   - A managed **PostgreSQL Database** (`bri-apparel-db`).
4. Click **Apply**. Database migrations, schema initialization, and seeder scripts run automatically on first boot.

### Option B: Manual Web Service & PostgreSQL Setup
1. **Create PostgreSQL Database** on Render:
   - Name: `bri-apparel-db`
   - Copy the **Internal Database URL** (`postgresql://...`).
2. **Create Web Service** on Render:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
3. Add Environment Variables:
   - `DATABASE_URL` = `<your-postgresql-internal-url>`
   - `SECRET_KEY` = `<secure-random-secret-key>`
   - `FLASK_ENV` = `production`
4. Deploy and verify at `https://<your-app>.onrender.com/`.

---

## 7. Quality Assurance & Verification

The automated test suite (`test_system.py`) verifies:
- `test_01_health_check`: Unified API service availability
- `test_02_admin_authentication`: Secure login and wrong password rejection
- `test_03_customer_registration_and_login`: Customer lifecycle & hashing
- `test_04_role_based_access_control`: Customer role restricted from administrative endpoints
- `test_05_product_catalog_crud`: Full product create, update, and deactivate
- `test_06_order_placement_and_synchronization`: Cross-interface order synchronization
- `test_07_inventory_adjustment_and_audit_log`: Stock adjustments & logging
- `test_08_analytics_and_system_settings`: Real-time KPI calculations & settings
- `test_09_frontend_page_serving`: Clean HTTP 200 delivery for all 23 interface pages

---

## 8. License

&copy; 2026 BRI APPARELL. All rights reserved.
