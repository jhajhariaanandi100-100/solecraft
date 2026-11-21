from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Address, Order, CustomDesign, Wishlist, Product, Cart, CartItem

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password. Please verify your credentials.', 'danger')
            return render_template('auth/login.html')

        login_user(user, remember=remember)

        # Merge guest cart if one existed in session
        session_cart_id = session.get('cart_id')
        if session_cart_id:
            guest_cart = db.session.get(Cart, session_cart_id)
            if guest_cart and guest_cart.items:
                user_cart = Cart.query.filter_by(user_id=user.id).first()
                if not user_cart:
                    user_cart = Cart(user_id=user.id)
                    db.session.add(user_cart)
                    db.session.flush()
                
                for item in guest_cart.items:
                    item.cart_id = user_cart.id
                
                db.session.delete(guest_cart)
                db.session.commit()
                session['cart_id'] = user_cart.id

        flash(f'Welcome back, {user.full_name}!', 'success')
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('auth.profile'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()

        if not full_name or not email or not password:
            flash('All required fields must be provided.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please re-enter.', 'danger')
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists. Please log in.', 'warning')
            return redirect(url_for('auth.login'))

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            role='customer'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Account created successfully! Welcome to SOLECRAFT Studio.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    user_designs = CustomDesign.query.filter_by(user_id=current_user.id).order_by(CustomDesign.created_at.desc()).all()
    wishlist_entries = Wishlist.query.filter_by(user_id=current_user.id).all()
    addresses = Address.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'auth/profile.html',
        orders=user_orders,
        designs=user_designs,
        wishlist=wishlist_entries,
        addresses=addresses
    )


@auth_bp.route('/profile/address', methods=['POST'])
@login_required
def add_address():
    full_name = request.form.get('full_name')
    street_address = request.form.get('street_address')
    apartment = request.form.get('apartment')
    city = request.form.get('city')
    state = request.form.get('state')
    postal_code = request.form.get('postal_code')
    country = request.form.get('country', 'United States')
    phone = request.form.get('phone')
    is_default = True if request.form.get('is_default') else False

    if not all([full_name, street_address, city, state, postal_code, phone]):
        flash('Please fill in all required address fields.', 'danger')
        return redirect(url_for('auth.profile'))

    if is_default:
        Address.query.filter_by(user_id=current_user.id).update({'is_default': False})

    address = Address(
        user_id=current_user.id,
        full_name=full_name,
        street_address=street_address,
        apartment=apartment,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
        phone=phone,
        is_default=is_default
    )
    db.session.add(address)
    db.session.commit()

    flash('Shipping address saved successfully.', 'success')
    return redirect(url_for('auth.profile'))


@auth_bp.route('/wishlist/toggle/<int:product_id>', methods=['POST'])
def toggle_wishlist(product_id):
    if not current_user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Please log in to manage your wishlist.', 'require_login': True}), 401
        flash('Please log in to save items to your wishlist.', 'warning')
        return redirect(url_for('auth.login'))

    product = Product.query.get_or_404(product_id)
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product.id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        added = False
        msg = f"Removed '{product.name}' from your wishlist."
    else:
        new_item = Wishlist(user_id=current_user.id, product_id=product.id)
        db.session.add(new_item)
        db.session.commit()
        added = True
        msg = f"Saved '{product.name}' to your wishlist."

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'added': added, 'message': msg})

    flash(msg, 'success')
    return redirect(request.referrer or url_for('products.shop'))
