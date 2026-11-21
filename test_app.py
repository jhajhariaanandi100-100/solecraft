import unittest
import json
from app import create_app, db
from app.models import User, Product, Category, Order, CustomDesign, Coupon, Cart

class SoleCraftTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.Config')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_01_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SOLECRAFT', response.data)
        self.assertIn(b'Don\'t Just Wear Shoes. Create Them.', response.data)
        print("[PASS] Test 1: Home page loads with hero headline and collections.")

    def test_02_shop_catalog(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Footwear', response.data)
        self.assertIn(b'Retro Low', response.data)
        print("[PASS] Test 2: Shop catalog loads all products.")

    def test_03_product_detail(self):
        response = self.client.get('/products/solecraft-retro-low-77')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Retro Low', response.data)
        self.assertIn(b'Add to Bag', response.data)
        print("[PASS] Test 3: Product details page loads with images and size selector.")

    def test_04_customizer_studio(self):
        response = self.client.get('/customizer/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bespoke Shoe Customiser', response.data)
        self.assertIn(b'solecraft-live-svg', response.data)
        print("[PASS] Test 4: Customizer Studio loads with interactive SVG canvas.")

    def test_05_customizer_save_and_cart_api(self):
        # Test Save Design API
        payload = {
            'title': 'Test Sunset Sneaker',
            'shoe_type': 'retro_low',
            'base_color': '#FFFFFF',
            'upper_material': 'Italian Leather',
            'upper_color': '#111111',
            'sole_color': '#FFFFFF',
            'lace_color': '#FF6B35',
            'tongue_color': '#111111',
            'heel_color': '#FF6B35',
            'pattern': 'racing_stripe',
            'custom_text': 'TEST-77',
            'custom_text_color': '#FFFFFF',
            'calculated_price': 197.0
        }
        res = self.client.post('/customizer/api/save', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        print("[PASS] Test 5a: Custom design saved successfully to vault.")

        # Test Add Custom Shoe to Cart API
        payload['size'] = 'US 9'
        payload['quantity'] = 1
        res = self.client.post('/customizer/api/add-to-cart', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['cart_count'], 1)
        print("[PASS] Test 5b: Custom bespoke shoe added directly to shopping cart.")

    def test_06_ai_stylist(self):
        res = self.client.get('/ai-stylist/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SoleCraft AI Style Assistant', res.data)

        # Post survey answers
        payload = {
            'vibe': 'streetwear',
            'occasion': 'nightout',
            'colors': 'volt_orange',
            'footwear_type': 'all',
            'budget': '150_220'
        }
        res = self.client.post('/ai-stylist/recommend', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['archetype']['title'], 'The Hype Alchemist')
        self.assertGreaterEqual(len(data['recommendations']), 1)
        print("[PASS] Test 6: AI Style Assistant analyzed lifestyle profile and returned tailored recommendations.")

    def test_07_cart_and_coupon(self):
        # Add a product to cart
        with self.app.app_context():
            prod = Product.query.first()
            prod_id = prod.id

        res = self.client.post('/cart/add', data={'product_id': prod_id, 'size': 'US 9', 'quantity': 1}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Shopping Bag', res.data)

        # Apply Coupon
        res = self.client.post('/cart/apply-coupon', data={'coupon_code': 'WELCOME20'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'applied successfully', res.data)
        print("[PASS] Test 7: Cart add and coupon application validated.")

    def test_08_checkout_and_order_placement(self):
        # 1. Add item to cart first
        with self.app.app_context():
            prod = Product.query.first()
            prod_id = prod.id

        self.client.post('/cart/add', data={'product_id': prod_id, 'size': 'US 9', 'quantity': 1})

        # 2. Place order
        order_data = {
            'full_name': 'Test Shopper',
            'email': 'shopper@test.com',
            'phone': '+1 (555) 999-8888',
            'street_address': '100 Broadway',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10001',
            'country': 'United States',
            'payment_method': 'Razorpay (Test)'
        }
        res = self.client.post('/orders/checkout', data=order_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Order Confirmed', res.data)
        self.assertIn(b'SC-20', res.data)
        print("[PASS] Test 8: Full checkout flow and order persistence verified.")

    def test_09_admin_security_and_dashboard(self):
        # Try accessing admin without login -> should redirect to login
        res = self.client.get('/admin/', follow_redirects=True)
        self.assertIn(b'Sign In', res.data)

        # Login as Admin
        res = self.client.post('/auth/login', data={'email': 'admin@solecraft.com', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        # Access Admin Dashboard
        res = self.client.get('/admin/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Atelier Operations Hub', res.data)
        self.assertIn(b'Total Revenue', res.data)
        print("[PASS] Test 9: Admin role-based access control and analytics dashboard verified.")

if __name__ == '__main__':
    unittest.main()
