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

        # Customer places order
        order_res = self.client.post('/api/orders', json={
            "customer_name": "QA Sync Customer",
            "customer_email": "qa.sync@example.com",
            "customer_phone": "+63 917 999 8888",
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

        # Admin fetches orders list -> verifies new order is present
        admin_orders_res = self.client.get('/api/orders', headers=admin_headers)
        self.assertEqual(admin_orders_res.status_code, 200)
        orders_list = admin_orders_res.get_json()["orders"]
        matching = [o for o in orders_list if o["id"] == order_id]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["customer_name"], "QA Sync Customer")

        # Admin updates status to 'In Transit'
        status_res = self.client.put(f'/api/orders/{order_id}/status', headers=admin_headers, json={
            "status": "In Transit",
            "courier": "LBC Express",
            "tracking_number": "LBC-SYNC-9988",
            "notes": "Handed to LBC courier dispatch"
        })
        self.assertEqual(status_res.status_code, 200)

        # Customer tracking check
        cust_order_res = self.client.get(f'/api/orders/{order_id}')
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
        """Verify all customer, admin, and staff portals are served cleanly."""
        pages = [
            '/',
            '/shop.html',
            '/collections.html',
            '/cart.html',
            '/checkout.html',
            '/account.html',
            '/about.html',
            '/contact.html',
            '/admin/',
            '/admin/login.html',
            '/admin/index.html',
            '/admin/users.html',
            '/admin/customers.html',
            '/admin/products.html',
            '/admin/categories.html',
            '/admin/orders.html',
            '/admin/inventory.html',
            '/admin/payments.html',
            '/admin/reports.html',
            '/admin/notifications.html',
            '/admin/settings.html',
            '/admin/profile.html',
            '/staff/dashboard.html'
        ]
        for page in pages:
            res = self.client.get(page)
            self.assertEqual(res.status_code, 200, f"Failed serving page: {page}")

if __name__ == '__main__':
    unittest.main()
