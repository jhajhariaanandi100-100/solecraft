import os
from flask import Flask, session
from flask_login import LoginManager, current_user
from .models import db, User, Category, Cart, Product, Coupon, Review, CustomDesign

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Ensure uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register Blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.customizer import customizer_bp
    from .routes.cart import cart_bp
    from .routes.orders import orders_bp
    from .routes.ai_stylist import ai_stylist_bp
    from .routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(customizer_bp, url_prefix='/customizer')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(ai_stylist_bp, url_prefix='/ai-stylist')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Global Context Processor
    @app.context_processor
    def inject_global_vars():
        categories = Category.query.order_by(Category.name).all() if db.session else []
        cart_count = 0
        
        # Check active cart
        cart_id = session.get('cart_id')
        if current_user.is_authenticated:
            user_cart = Cart.query.filter_by(user_id=current_user.id).first()
            if user_cart:
                cart_count = user_cart.total_items
        elif cart_id:
            guest_cart = db.session.get(Cart, cart_id)
            if guest_cart:
                cart_count = guest_cart.total_items

        return dict(
            nav_categories=categories,
            cart_count=cart_count,
            brand_name="SOLECRAFT",
            brand_tagline="Your Style. Your Design. Your Sole.",
            currency_symbol=app.config.get('CURRENCY_SYMBOL', '$')
        )

    # Database Initialization & Seeding
    with app.app_context():
        db.create_all()
        from .seed_data import seed_initial_data
        seed_initial_data(db)

    return app

# Expose app instance so both 'gunicorn app:app' and 'gunicorn run:app' work out-of-the-box
app = create_app()

