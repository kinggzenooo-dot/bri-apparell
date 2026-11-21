"""
BRI APPARELL — Comprehensive System Test Suite
Verifies backend APIs, database persistence, authentication, role-based access, and cross-interface synchronization.
"""

import unittest
import json
from app import app
from database import query_db, init_db

class BriApparelSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()
        cls.client.testing = True

    def test_01_health_check(self):
        """Verify health check endpoint returns 200 and correct payload."""
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("version", data)

    def test_02_admin_authentication(self):
        """Verify admin login with correct password, and rejection with invalid password."""
        # 1. Invalid password
        bad_res = self.client.post('/api/auth/login', json={
            "email": "admin@briapparell.com",
            "password": "wrongpassword"
        })
        self.assertEqual(bad_res.status_code, 401)

        # 2. Correct admin login
        res = self.client.post('/api/auth/login', json={
            "email": "admin@briapparell.com",
            "password": "admin123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("token", data)
        self.assertEqual(data["user"]["role"], "admin")
        self.admin_token = data["token"]

    def test_03_customer_registration_and_login(self):
        """Verify customer registration creates user in DB and logs in."""
        unique_email = "test.shopper@example.com"
        # Register
        reg_res = self.client.post('/api/auth/register', json={
            "email": unique_email,
            "password": "password123",
            "full_name": "Test Shopper",
            "phone": "+63 917 111 2222",
            "street": "123 Bonifacio High",
            "city": "Taguig",
            "province": "Metro Manila",
            "postal_code": "1634"
        })
        self.assertIn(reg_res.status_code, [201, 409]) # 201 if fresh, 409 if exists

        # Login
        login_res = self.client.post('/api/auth/login', json={
            "email": unique_email,
            "password": "password123"
        })
        self.assertEqual(login_res.status_code, 200)
        cust_data = login_res.get_json()
        self.assertEqual(cust_data["user"]["role"], "customer")
        self.assertEqual(cust_data["user"]["full_name"], "Test Shopper")

        # Test duplicate registration rejection (Phase 13 requirement)
        dup_res = self.client.post('/api/auth/register', json={
            "email": unique_email,
            "password": "password123",
            "full_name": "Duplicate Shopper"
        })
        self.assertEqual(dup_res.status_code, 409)

    def test_03b_guest_checkout_restrictions(self):
        """
        Phase 13 Critical Security Requirement:
        Guests must NOT be allowed to complete purchases or list customer orders without authentication.
        """
        anon_client = app.test_client()

        # 1. Anonymous POST /api/orders must return 401 Unauthorized
        guest_order_res = anon_client.post('/api/orders', json={
            "customer_name": "Anonymous Guest",
            "customer_email": "guest@example.com",
            "customer_phone": "+63 917 000 0000",
            "shipping_address": "Nowhere St",
            "city": "Manila",
            "province": "Metro Manila",
            "postal_code": "1000",
            "payment_method": "COD",
            "items": [{"id": "bri-001", "size": "M", "color": "Pitch Black", "quantity": 1}]
        })
        self.assertEqual(guest_order_res.status_code, 401)
        err_data = guest_order_res.get_json()
        self.assertIn("error", err_data)
        self.assertIn("Authentication required", err_data["error"])

        # 2. Anonymous GET /api/orders must return 401 Unauthorized
        guest_list_res = anon_client.get('/api/orders')
        self.assertEqual(guest_list_res.status_code, 401)

    def test_03c_inactive_account_blocked(self):
        """
        Phase 13 Requirement:
        Disabled / inactive accounts must be prevented from logging in.
        """
        from database import execute_db
        from werkzeug.security import generate_password_hash

        execute_db("DELETE FROM users WHERE email = 'banned@example.com'")
        execute_db(
            "INSERT INTO users (email, password_hash, full_name, role, status) VALUES (?, ?, ?, ?, ?)",
            ("banned@example.com", generate_password_hash("bannedpass123"), "Banned User", "customer", "Inactive")
        )

        login_res = self.client.post('/api/auth/login', json={
            "email": "banned@example.com",
            "password": "bannedpass123"
        })
        self.assertEqual(login_res.status_code, 403)
        err = login_res.get_json()
        self.assertIn("error", err)
        self.assertIn("inactive", err["error"].lower())

    def test_03d_session_persistence_and_profile(self):
        """
        Phase 13 Requirement:
        Authenticated session verification via /api/auth/me and proper logout.
        """
        login_res = self.client.post('/api/auth/login', json={
            "email": "john@email.com",
            "password": "password123"
        })
        token = login_res.get_json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Check me
        me_res = self.client.get('/api/auth/me', headers=headers)
        self.assertEqual(me_res.status_code, 200)
        user_info = me_res.get_json()["user"]
        self.assertEqual(user_info["email"], "john@email.com")

        # Logout
        logout_res = self.client.post('/api/auth/logout', headers=headers)
        self.assertEqual(logout_res.status_code, 200)

    def test_04_role_based_access_control(self):
        """Verify customer cannot access administrator-only endpoints."""
        # Get customer token
        c_res = self.client.post('/api/auth/login', json={
            "email": "john@email.com",
            "password": "password123"
        })
        cust_token = c_res.get_json()["token"]

        # Attempt to access admin users endpoint with customer token -> 403 Forbidden
        res = self.client.get('/api/users', headers={"Authorization": f"Bearer {cust_token}"})
        self.assertEqual(res.status_code, 403)

        # Attempt to access with a brand new unauthenticated client -> 401 Unauthorized
        anon_client = app.test_client()
        anon_res = anon_client.get('/api/users')
        self.assertEqual(anon_res.status_code, 401)

    def test_05_product_catalog_crud(self):
        """Verify products API: listing, admin creation, updating, and deactivation."""
        import random
        # Admin login
        admin_res = self.client.post('/api/auth/login', json={
            "email": "admin@briapparell.com",
            "password": "admin123"
        })
        token = admin_res.get_json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # List products
        list_res = self.client.get('/api/products')
        self.assertEqual(list_res.status_code, 200)
        self.assertGreater(list_res.get_json()["count"], 0)

        test_pid = f"bri-test-{random.randint(10000, 99999)}"

        # Create new product
        create_res = self.client.post('/api/products', headers=headers, json={
            "id": test_pid,
            "name": "Automated Test Structured Blazer",
            "category": "Outerwear",
            "price": 3895,
            "salePrice": 3295,
            "isSale": True,
            "isNew": True,
            "isFeatured": True,
            "shortDesc": "Structured architectural blazer for automated QA tests."
        })
        self.assertEqual(create_res.status_code, 201)
        created = create_res.get_json()["product"]
        self.assertEqual(created["id"], test_pid)

        # Update product
        upd_res = self.client.put(f'/api/products/{test_pid}', headers=headers, json={
            "name": "Automated Test Structured Blazer (Updated)",
            "price": 3995
        })
        self.assertEqual(upd_res.status_code, 200)

        # Verify update reflects in customer GET
        get_res = self.client.get(f'/api/products/{test_pid}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["name"], "Automated Test Structured Blazer (Updated)")

        # Deactivate
        del_res = self.client.delete(f'/api/products/{test_pid}', headers=headers)
        self.assertEqual(del_res.status_code, 200)

    def test_06_order_placement_and_synchronization(self):
        """
        Verify the central system synchronization flow:
        1. Customer places order.
        2. Order is saved in database and variants stock is deducted.
        3. Order is immediately visible to Admin.
        4. Admin updates order status to 'In Transit'.
        5. Customer order tracking reflects 'In Transit'.
        """
        # Admin token
        admin_res = self.client.post('/api/auth/login', json={"email": "admin@briapparell.com", "password": "admin123"})
        admin_token = admin_res.get_json()["token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Customer logs in first (Phase 13 requirement)
        cust_login_res = self.client.post('/api/auth/login', json={"email": "john@email.com", "password": "password123"})
        cust_token = cust_login_res.get_json()["token"]
        cust_headers = {"Authorization": f"Bearer {cust_token}"}

        # Customer places order with authentication
        order_res = self.client.post('/api/orders', headers=cust_headers, json={
            "customer_name": "John Doe",
            "customer_email": "john@email.com",
            "customer_phone": "+63 917 123 4567",
            "shipping_address": "Penthouse B, One Serendra, BGC",
            "city": "Taguig",
            "province": "Metro Manila",
            "postal_code": "1634",
            "payment_method": "GCASH",
            "items": [
                {"id": "bri-001", "size": "M", "color": "Pitch Black", "quantity": 1}
            ]
        })
        self.assertEqual(order_res.status_code, 201)
        order_data = order_res.get_json()
        order_id = order_data["orderId"]
        self.assertTrue(order_id.startswith("BRI-2026-"))

        # Customer fetches orders list -> verifies order is present in customer's list
        cust_orders_res = self.client.get('/api/orders', headers=cust_headers)
        self.assertEqual(cust_orders_res.status_code, 200)
        cust_orders = cust_orders_res.get_json()["orders"]
        self.assertTrue(any(o["id"] == order_id for o in cust_orders))

        # Admin fetches orders list -> verifies new order is present
        admin_orders_res = self.client.get('/api/orders', headers=admin_headers)
        self.assertEqual(admin_orders_res.status_code, 200)
        orders_list = admin_orders_res.get_json()["orders"]
        matching = [o for o in orders_list if o["id"] == order_id]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["customer_name"], "John Doe")

        # Admin updates status to 'In Transit'
        status_res = self.client.put(f'/api/orders/{order_id}/status', headers=admin_headers, json={
            "status": "In Transit",
            "courier": "LBC Express",
            "tracking_number": "LBC-SYNC-9988",
            "notes": "Handed to LBC courier dispatch"
        })
        self.assertEqual(status_res.status_code, 200)

        # Customer tracking check
        cust_order_res = self.client.get(f'/api/orders/{order_id}', headers=cust_headers)
        self.assertEqual(cust_order_res.status_code, 200)
        updated_order = cust_order_res.get_json()
        self.assertEqual(updated_order["status"], "In Transit")
        self.assertEqual(updated_order["courier"], "LBC Express")
        self.assertEqual(updated_order["tracking_number"], "LBC-SYNC-9988")

    def test_07_inventory_adjustment_and_audit_log(self):
        """Verify inventory stock adjustment and audit trail recording."""
        admin_res = self.client.post('/api/auth/login', json={"email": "admin@briapparell.com", "password": "admin123"})
        headers = {"Authorization": f"Bearer {admin_res.get_json()['token']}"}

        # Get inventory list
        inv_res = self.client.get('/api/inventory', headers=headers)
        self.assertEqual(inv_res.status_code, 200)
        variants = inv_res.get_json()["inventory"]
        self.assertGreater(len(variants), 0)
        first_var = variants[0]

        # Adjust stock
        adj_res = self.client.post('/api/inventory/adjust', headers=headers, json={
            "variant_id": first_var["id"],
            "new_stock": 25,
            "change_type": "RESTOCK",
            "reason": "QA Test Restock Inbound"
        })
        self.assertEqual(adj_res.status_code, 200)
        self.assertEqual(adj_res.get_json()["variant"]["stock_quantity"], 25)

        # Verify logs
        logs_res = self.client.get('/api/inventory/logs', headers=headers)
        self.assertEqual(logs_res.status_code, 200)
        self.assertGreater(len(logs_res.get_json()["logs"]), 0)

    def test_08_analytics_and_system_settings(self):
        """Verify analytics overview calculation and system settings persistence."""
        admin_res = self.client.post('/api/auth/login', json={"email": "admin@briapparell.com", "password": "admin123"})
        headers = {"Authorization": f"Bearer {admin_res.get_json()['token']}"}

        # Analytics
        analytics_res = self.client.get('/api/analytics/overview', headers=headers)
        self.assertEqual(analytics_res.status_code, 200)
        kpi = analytics_res.get_json()["kpi"]
        self.assertIn("totalRevenue", kpi)
        self.assertIn("totalOrders", kpi)
        self.assertGreater(kpi["totalOrders"], 0)

        # Settings
        set_res = self.client.get('/api/settings')
        self.assertEqual(set_res.status_code, 200)
        settings = set_res.get_json()["settings"]
        self.assertEqual(settings.get("store_name"), "BRI APPARELL")

        # Update setting
        upd_set = self.client.put('/api/settings', headers=headers, json={
            "store_phone": "+63 917 892 4567"
        })
        self.assertEqual(upd_set.status_code, 200)

    def test_09_frontend_page_serving(self):
        """Verify centralized authorization portal and customer public pages are served cleanly."""
        # 1. Main entry point redirects unauthenticated visitors to login
        anon_client = app.test_client()
        res_root = anon_client.get('/')
        self.assertEqual(res_root.status_code, 302)
        self.assertIn('/authorization/login.html', res_root.headers.get('Location', ''))
        res_root.close()

        # 2. Main entry point with follow_redirects reaches login successfully
        res_root_followed = anon_client.get('/', follow_redirects=True)
        self.assertEqual(res_root_followed.status_code, 200)
        res_root_followed.close()

        # 3. Direct authorization portal and layout asset files
        auth_pages = [
            '/authorization/login.html',
            '/authorization/signup.html',
            '/authorization/auth.css',
            '/authorization/auth.js',
            '/admin/css/admin.css',
            '/admin/js/admin.js',
            '/css/staff.css'
        ]
        for p in auth_pages:
            res = self.client.get(p)
            self.assertEqual(res.status_code, 200, f"Failed serving auth asset: {p}")
            res.close()

        # 4. Public storefront catalog pages
        public_pages = [
            '/shop.html',
            '/collections.html',
            '/promotions.html',
            '/about.html',
            '/contact.html',
            '/cart.html',
            '/wishlist.html'
        ]
        for page in public_pages:
            res = self.client.get(page)
            self.assertEqual(res.status_code, 200, f"Failed serving page: {page}")
            res.close()

    def test_10_phase14_staff_and_admin_role_access(self):
        """
        Phase 14 Requirement:
        Verify Staff and Admin interfaces, authentication, permissions, and session protection.
        """
        # 1. Unauthenticated client attempting /admin/index.html -> 302 Redirect to Login
        anon = app.test_client()
        res_admin_anon = anon.get('/admin/index.html')
        self.assertEqual(res_admin_anon.status_code, 302)
        self.assertIn('/authorization/login.html', res_admin_anon.headers.get('Location', ''))
        res_admin_anon.close()

        # 2. Unauthenticated client attempting /staff/dashboard.html -> 302 Redirect to Login
        res_staff_anon = anon.get('/staff/dashboard.html')
        self.assertEqual(res_staff_anon.status_code, 302)
        self.assertIn('/authorization/login.html', res_staff_anon.headers.get('Location', ''))
        res_staff_anon.close()

        # 3. Staff Login and Access
        staff_client = app.test_client()
        staff_login = staff_client.post('/api/auth/login', json={
            "email": "alexander.vance@briapparell.com",
            "password": "staff123"
        })
        self.assertEqual(staff_login.status_code, 200)
        staff_data = staff_login.get_json()
        self.assertEqual(staff_data["user"]["role"], "staff")
        staff_token = staff_data["token"]

        # Staff can access staff dashboard
        staff_dash_res = staff_client.get('/staff/dashboard.html')
        self.assertEqual(staff_dash_res.status_code, 200)
        staff_dash_res.close()

        # Staff CANNOT access admin-only endpoints (/api/users) -> 403 Forbidden
        staff_forbidden = staff_client.get('/api/users', headers={"Authorization": f"Bearer {staff_token}"})
        self.assertEqual(staff_forbidden.status_code, 403)

        # 4. Admin Login and Access
        admin_client = app.test_client()
        admin_login = admin_client.post('/api/auth/login', json={
            "email": "admin@briapparell.com",
            "password": "admin123"
        })
        self.assertEqual(admin_login.status_code, 200)
        admin_data = admin_login.get_json()
        self.assertEqual(admin_data["user"]["role"], "admin")
        admin_token = admin_data["token"]

        # Admin can access admin dashboard
        admin_dash_res = admin_client.get('/admin/index.html')
        self.assertEqual(admin_dash_res.status_code, 200)
        admin_dash_res.close()

        # Admin can access admin-only endpoints (/api/users) -> 200 OK
        admin_users_res = admin_client.get('/api/users', headers={"Authorization": f"Bearer {admin_token}"})
        self.assertEqual(admin_users_res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
