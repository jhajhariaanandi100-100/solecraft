import os
from functools import wraps
from datetime import datetime, timedelta, timezone
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db, User, Product, Category, Order, OrderItem, Coupon, CustomDesign, Review, Payment

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access restricted. Executive credentials required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
    total_sales = db.session.query(db.func.sum(Order.final_amount)).filter(Order.payment_status == 'Paid').scalar() or 0.0
    total_orders = Order.query.count()
    total_customers = User.query.filter_by(role='customer').count()
    custom_orders_count = OrderItem.query.filter(OrderItem.custom_design_id.isnot(None)).count()
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(7).all()
    recent_customers = User.query.filter_by(role='customer').order_by(User.created_at.desc()).limit(5).all()

    # Sales Analytics data for Chart.js: Revenue by last 7 days
    today = datetime.now().date()
    date_labels = []
    revenue_data = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        
        day_rev = db.session.query(db.func.sum(Order.final_amount)).filter(
            Order.payment_status == 'Paid',
            Order.created_at >= day_start,
            Order.created_at <= day_end
        ).scalar() or 0.0
        
        date_labels.append(day.strftime('%b %d'))
        revenue_data.append(round(day_rev, 2))

    # Category breakdown for donut chart
    categories = Category.query.all()
    cat_labels = [c.name for c in categories]
    cat_counts = [len(c.products) for c in categories]

    return render_template(
        'admin/dashboard.html',
        total_sales=total_sales,
        total_orders=total_orders,
        total_customers=total_customers,
        custom_orders_count=custom_orders_count,
        recent_orders=recent_orders,
        recent_customers=recent_customers,
        date_labels=date_labels,
        revenue_data=revenue_data,
        cat_labels=cat_labels,
        cat_counts=cat_counts
    )


@admin_bp.route('/products')
@admin_required
def products():
    all_products = Product.query.order_by(Product.id.desc()).all()
    categories = Category.query.all()
    return render_template('admin/products.html', products=all_products, categories=categories)


@admin_bp.route('/products/add', methods=['POST'])
@admin_required
def add_product():
    name = request.form.get('name', '').strip()
    category_id = request.form.get('category_id', type=int)
    tagline = request.form.get('tagline', '').strip()
    description = request.form.get('description', '').strip()
    price = request.form.get('price', type=float)
    discount_price = request.form.get('discount_price', type=float)
    sku = request.form.get('sku', '').strip().upper()
    stock = request.form.get('stock', 50, type=int)
    shoe_type = request.form.get('shoe_type', 'Sneakers')
    gender = request.form.get('gender', 'Unisex')
    material = request.form.get('material', 'Italian Calfskin')
    colors = request.form.get('colors', 'White, Black, Orange')
    sizes = request.form.get('sizes', 'US 7, US 8, US 9, US 10, US 11')
    is_featured = True if request.form.get('is_featured') else False
    is_bestseller = True if request.form.get('is_bestseller') else False

    if not name or not price or not sku or not category_id:
        flash('Please fill in required fields: Name, Price, SKU, and Category.', 'danger')
        return redirect(url_for('admin.products'))

    # Slug generator
    slug = name.lower().replace(' ', '-').replace("'", '')
    # Check if slug exists
    if Product.query.filter_by(slug=slug).first():
        slug = f"{slug}-{sku.lower()}"

    # Handle image upload or fallback
    main_image = "/static/images/products/custom-default.svg"
    file = request.files.get('image_file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        main_image = f"/static/uploads/{filename}"

    product = Product(
        name=name,
        slug=slug,
        category_id=category_id,
        tagline=tagline,
        description=description,
        price=price,
        discount_price=discount_price if discount_price and discount_price > 0 else None,
        sku=sku,
        stock=stock,
        shoe_type=shoe_type,
        gender=gender,
        material=material,
        colors=colors,
        sizes=sizes,
        main_image=main_image,
        is_featured=is_featured,
        is_bestseller=is_bestseller
    )
    db.session.add(product)
    db.session.commit()

    flash(f"Product '{product.name}' added to inventory.", 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/products/edit/<int:product_id>', methods=['POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    product.name = request.form.get('name', product.name).strip()
    product.category_id = request.form.get('category_id', product.category_id, type=int)
    product.tagline = request.form.get('tagline', product.tagline)
    product.description = request.form.get('description', product.description)
    product.price = request.form.get('price', product.price, type=float)
    
    disc = request.form.get('discount_price', type=float)
    product.discount_price = disc if disc and disc > 0 else None

    product.stock = request.form.get('stock', product.stock, type=int)
    product.shoe_type = request.form.get('shoe_type', product.shoe_type)
    product.gender = request.form.get('gender', product.gender)
    product.material = request.form.get('material', product.material)
    product.colors = request.form.get('colors', product.colors)
    product.sizes = request.form.get('sizes', product.sizes)
    product.is_featured = True if request.form.get('is_featured') else False
    product.is_bestseller = True if request.form.get('is_bestseller') else False

    file = request.files.get('image_file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        product.main_image = f"/static/uploads/{filename}"

    db.session.commit()
    flash(f"Product '{product.name}' updated.", 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f"Product '{name}' deleted.", 'info')
    return redirect(url_for('admin.products'))


@admin_bp.route('/orders')
@admin_required
def orders():
    status_filter = request.args.get('status')
    query = Order.query
    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)
    all_orders = query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders, current_filter=status_filter)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    valid_statuses = ['Order Placed', 'Processing', 'Customisation in Progress', 'Shipped', 'Out for Delivery', 'Delivered', 'Cancelled']

    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f"Order {order.order_number} status updated to '{new_status}'.", 'success')
    else:
        flash('Invalid status provided.', 'danger')

    return redirect(request.referrer or url_for('admin.orders'))


@admin_bp.route('/custom-orders')
@admin_required
def custom_orders():
    # Fetch all order items with custom footwear
    items = OrderItem.query.filter(OrderItem.custom_design_id.isnot(None)).order_by(OrderItem.id.desc()).all()
    return render_template('admin/custom_orders.html', custom_items=items)


@admin_bp.route('/coupons', methods=['GET', 'POST'])
@admin_required
def coupons():
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
        discount_percent = request.form.get('discount_percent', 0.0, type=float)
        discount_amount = request.form.get('discount_amount', 0.0, type=float)
        min_order = request.form.get('min_order_value', 0.0, type=float)
        max_discount = request.form.get('max_discount', type=float)
        days = request.form.get('valid_days', 60, type=int)

        if not code:
            flash('Coupon code is required.', 'danger')
        else:
            coupon = Coupon(
                code=code,
                discount_percent=discount_percent,
                discount_amount=discount_amount,
                min_order_value=min_order,
                max_discount=max_discount if max_discount and max_discount > 0 else None,
                valid_to=datetime.now(timezone.utc) + timedelta(days=days),
                is_active=True
            )
            db.session.add(coupon)
            db.session.commit()
            flash(f"Coupon '{code}' created.", 'success')
            return redirect(url_for('admin.coupons'))

    all_coupons = Coupon.query.order_by(Coupon.id.desc()).all()
    return render_template('admin/coupons.html', coupons=all_coupons)


@admin_bp.route('/coupons/<int:coupon_id>/toggle', methods=['POST'])
@admin_required
def toggle_coupon(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    coupon.is_active = not coupon.is_active
    db.session.commit()
    flash(f"Coupon '{coupon.code}' is now {'Active' if coupon.is_active else 'Disabled'}.", 'info')
    return redirect(url_for('admin.coupons'))
