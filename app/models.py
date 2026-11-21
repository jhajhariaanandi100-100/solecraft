from datetime import datetime, timezone
import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utc_now():
    return datetime.now()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), default='customer') # 'customer' or 'admin'
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    addresses = db.relationship('Address', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, order_by='desc(Order.created_at)')
    reviews = db.relationship('Review', backref='user', lazy=True)
    custom_designs = db.relationship('CustomDesign', backref='user', lazy=True, order_by='desc(CustomDesign.created_at)')
    wishlist_items = db.relationship('Wishlist', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.email}>'


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    apartment = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='United States')
    phone = db.Column(db.String(20), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    def formatted(self):
        parts = [self.street_address]
        if self.apartment:
            parts.append(self.apartment)
        parts.append(f"{self.city}, {self.state} {self.postal_code}")
        parts.append(self.country)
        return ", ".join(parts)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    slug = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), nullable=False, unique=True)
    tagline = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    stock = db.Column(db.Integer, default=50)
    is_featured = db.Column(db.Boolean, default=False)
    is_bestseller = db.Column(db.Boolean, default=False)
    shoe_type = db.Column(db.String(50), default='Sneakers') # Sneakers, Running, Casual, Sports, Formal, Unisex
    gender = db.Column(db.String(20), default='Unisex') # Men, Women, Unisex
    material = db.Column(db.String(100), default='Full-grain Italian Leather')
    colors = db.Column(db.String(255), default='White, Black, Orange') # Comma-separated
    sizes = db.Column(db.String(255), default='US 7, US 8, US 9, US 10, US 11, US 12') # Comma-separated
    main_image = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    variants = db.relationship('ProductVariant', backref='product', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan', order_by='desc(Review.created_at)')

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price and self.discount_price > 0 else self.price

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price > 0 and self.discount_price < self.price

    @property
    def discount_percent(self):
        if self.has_discount:
            return int(round((1 - (self.discount_price / self.price)) * 100))
        return 0

    @property
    def average_rating(self):
        if not self.reviews:
            return 4.8 # Default stellar preview rating
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    @property
    def review_count(self):
        return len(self.reviews)

    @property
    def size_list(self):
        return [s.strip() for s in self.sizes.split(',') if s.strip()]

    @property
    def color_list(self):
        return [c.strip() for c in self.colors.split(',') if c.strip()]


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)


class ProductVariant(db.Model):
    __tablename__ = 'product_variants'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(50), nullable=True)
    stock = db.Column(db.Integer, default=10)


class CustomDesign(db.Model):
    __tablename__ = 'custom_designs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Can be created by guest, assigned on signup
    title = db.Column(db.String(100), default='My Custom SoleCraft')
    shoe_type = db.Column(db.String(50), default='retro_low') # retro_low, high_top, aeroknit_runner, urban_slipon
    base_color = db.Column(db.String(30), default='#FFFFFF')
    upper_material = db.Column(db.String(50), default='Italian Leather')
    upper_color = db.Column(db.String(30), default='#111111')
    sole_color = db.Column(db.String(30), default='#FFFFFF')
    lace_color = db.Column(db.String(30), default='#FF6B35')
    tongue_color = db.Column(db.String(30), default='#111111')
    heel_color = db.Column(db.String(30), default='#FF6B35')
    pattern = db.Column(db.String(50), default='none') # none, racing_stripe, camo, geometric, dots, gradient
    custom_text = db.Column(db.String(20), nullable=True) # Monogram initials or short name (max 10-12 chars)
    custom_text_color = db.Column(db.String(30), default='#FFFFFF')
    preview_image = db.Column(db.Text, nullable=True) # Can store SVG data or data URL
    calculated_price = db.Column(db.Float, default=185.0)
    specs_json = db.Column(db.Text, nullable=True) # Complete JSON string of all layer params
    created_at = db.Column(db.DateTime, default=utc_now)

    def get_specs(self):
        if self.specs_json:
            try:
                return json.loads(self.specs_json)
            except:
                pass
        return {
            'shoe_type': self.shoe_type,
            'base_color': self.base_color,
            'upper_material': self.upper_material,
            'upper_color': self.upper_color,
            'sole_color': self.sole_color,
            'lace_color': self.lace_color,
            'tongue_color': self.tongue_color,
            'heel_color': self.heel_color,
            'pattern': self.pattern,
            'custom_text': self.custom_text,
            'custom_text_color': self.custom_text_color,
            'calculated_price': self.calculated_price
        }


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_token = db.Column(db.String(100), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items)

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items)


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    custom_design_id = db.Column(db.Integer, db.ForeignKey('custom_designs.id'), nullable=True)
    size = db.Column(db.String(20), default='US 9')
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    custom_data_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    # Relationships
    product = db.relationship('Product')
    custom_design = db.relationship('CustomDesign')

    @property
    def line_total(self):
        return round(self.unit_price * self.quantity, 2)

    @property
    def is_custom(self):
        return self.custom_design_id is not None or self.product_id is None

    @property
    def display_name(self):
        if self.custom_design:
            return f"Bespoke {self.custom_design.title}"
        if self.product:
            return self.product.name
        return "Custom SoleCraft Sneaker"

    @property
    def display_image(self):
        if self.custom_design and self.custom_design.preview_image:
            return self.custom_design.preview_image
        if self.product:
            return self.product.main_image
        return "/static/images/products/custom-default.svg"


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(40), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)
    
    # Financial breakdown
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    coupon_code = db.Column(db.String(40), nullable=True)
    shipping_fee = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    final_amount = db.Column(db.Float, nullable=False)

    # Status tracking
    # 'Order Placed', 'Processing', 'Customisation in Progress', 'Shipped', 'Out for Delivery', 'Delivered', 'Cancelled'
    status = db.Column(db.String(50), default='Order Placed')
    payment_method = db.Column(db.String(50), default='Razorpay (Test)') # Razorpay, Credit Card, UPI, COD
    payment_status = db.Column(db.String(30), default='Pending') # Pending, Paid, Failed
    razorpay_order_id = db.Column(db.String(100), nullable=True)
    razorpay_payment_id = db.Column(db.String(100), nullable=True)

    # Customer snapshot
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    shipping_address_text = db.Column(db.Text, nullable=False)
    tracking_number = db.Column(db.String(80), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy=True, cascade='all, delete-orphan')
    shipping_address = db.relationship('Address')

    @property
    def has_custom_items(self):
        return any(item.is_custom for item in self.items)

    @property
    def status_step(self):
        steps = [
            'Order Placed',
            'Processing',
            'Customisation in Progress' if self.has_custom_items else 'Packing & Quality Check',
            'Shipped',
            'Out for Delivery',
            'Delivered'
        ]
        try:
            return steps.index(self.status) + 1
        except ValueError:
            return 1


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    custom_design_id = db.Column(db.Integer, db.ForeignKey('custom_designs.id'), nullable=True)
    product_name = db.Column(db.String(150), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    custom_specs_json = db.Column(db.Text, nullable=True)
    item_image = db.Column(db.Text, nullable=True)

    # Relationships
    product = db.relationship('Product')
    custom_design = db.relationship('CustomDesign')

    @property
    def is_custom(self):
        return self.custom_design_id is not None or self.custom_specs_json is not None

    def get_custom_specs(self):
        if self.custom_specs_json:
            try:
                return json.loads(self.custom_specs_json)
            except:
                pass
        return {}


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='Success')
    gateway_response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    title = db.Column(db.String(150), nullable=True)
    comment = db.Column(db.Text, nullable=False)
    verified_purchase = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)


class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    discount_percent = db.Column(db.Float, default=0.0) # e.g. 15 for 15%
    discount_amount = db.Column(db.Float, default=0.0) # e.g. 25 for $25 off
    min_order_value = db.Column(db.Float, default=0.0)
    max_discount = db.Column(db.Float, nullable=True)
    valid_from = db.Column(db.DateTime, default=utc_now)
    valid_to = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    usage_count = db.Column(db.Integer, default=0)
    max_uses = db.Column(db.Integer, default=1000)

    def is_valid_for(self, order_subtotal):
        if not self.is_active:
            return False, "This coupon is no longer active."
        if self.valid_to:
            val_limit = self.valid_to.replace(tzinfo=None) if hasattr(self.valid_to, 'tzinfo') and self.valid_to.tzinfo else self.valid_to
            if datetime.now() > val_limit:
                return False, "This coupon has expired."
        if self.usage_count >= self.max_uses:
            return False, "This coupon has reached its maximum usage limit."
        if order_subtotal < self.min_order_value:
            return False, f"Minimum order subtotal of ${self.min_order_value:.2f} is required for this coupon."
        return True, "Valid coupon"

    def calculate_discount(self, order_subtotal):
        valid, msg = self.is_valid_for(order_subtotal)
        if not valid:
            return 0.0
        
        discount = 0.0
        if self.discount_percent > 0:
            discount = (self.discount_percent / 100.0) * order_subtotal
        elif self.discount_amount > 0:
            discount = self.discount_amount

        if self.max_discount and discount > self.max_discount:
            discount = self.max_discount

        return round(min(discount, order_subtotal), 2)


class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    product = db.relationship('Product')
