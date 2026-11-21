import uuid
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import current_user
from app.models import db, Cart, CartItem, Product, Coupon

cart_bp = Blueprint('cart', __name__)

def get_current_cart(create=False):
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart and create:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        return cart
    else:
        cart_id = session.get('cart_id')
        cart = db.session.get(Cart, cart_id) if cart_id else None
        if not cart and create:
            cart = Cart(session_token=str(uuid.uuid4()))
            db.session.add(cart)
            db.session.commit()
            session['cart_id'] = cart.id
        return cart

@cart_bp.route('/')
def view_cart():
    cart = get_current_cart(create=False)
    items = cart.items if cart else []
    subtotal = cart.subtotal if cart else 0.0

    # Coupon Calculation
    coupon_code = session.get('coupon_code')
    coupon_discount = 0.0
    applied_coupon = None

    if coupon_code and subtotal > 0:
        applied_coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
        if applied_coupon:
            valid, msg = applied_coupon.is_valid_for(subtotal)
            if valid:
                coupon_discount = applied_coupon.calculate_discount(subtotal)
            else:
                session.pop('coupon_code', None)
                applied_coupon = None
                flash(msg, 'warning')

    # Shipping rule: Free above $150, else $15
    shipping_fee = 0.0 if (subtotal >= 150.0 or subtotal == 0) else 15.0

    # Estimated tax (5%)
    taxable_amount = max(0.0, subtotal - coupon_discount)
    tax_amount = round(taxable_amount * 0.05, 2) if taxable_amount > 0 else 0.0

    final_total = round(taxable_amount + shipping_fee + tax_amount, 2)

    return render_template(
        'cart.html',
        cart=cart,
        items=items,
        subtotal=subtotal,
        coupon_code=coupon_code,
        applied_coupon=applied_coupon,
        coupon_discount=coupon_discount,
        shipping_fee=shipping_fee,
        tax_amount=tax_amount,
        final_total=final_total
    )


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id', type=int)
    size = request.form.get('size', 'US 9')
    quantity = request.form.get('quantity', 1, type=int)

    product = Product.query.get_or_404(product_id)
    cart = get_current_cart(create=True)

    # Check if item with exact product and size already in cart
    existing_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id,
        size=size
    ).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            size=size,
            quantity=quantity,
            unit_price=product.effective_price
        )
        db.session.add(new_item)

    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'cart_count': cart.total_items,
            'message': f"Added {product.name} ({size}) to your bag."
        })

    flash(f"Added {product.name} ({size}) to your bag.", 'success')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    cart = get_current_cart()
    if not cart:
        return redirect(url_for('cart.view_cart'))

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first_or_404()
    quantity = request.form.get('quantity', type=int)
    size = request.form.get('size')

    if quantity is not None:
        if quantity <= 0:
            db.session.delete(item)
        else:
            item.quantity = min(20, quantity)
    if size:
        item.size = size

    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'cart_count': cart.total_items,
            'line_total': item.line_total if quantity > 0 else 0,
            'subtotal': cart.subtotal
        })

    flash('Cart updated.', 'success')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    cart = get_current_cart()
    if not cart:
        return redirect(url_for('cart.view_cart'))

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first_or_404()
    item_name = item.display_name
    db.session.delete(item)
    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'cart_count': cart.total_items,
            'subtotal': cart.subtotal,
            'message': f"Removed {item_name} from your bag."
        })

    flash(f"Removed {item_name} from your shopping bag.", 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/apply-coupon', methods=['POST'])
def apply_coupon():
    code = request.form.get('coupon_code', '').strip().upper()
    cart = get_current_cart()
    subtotal = cart.subtotal if cart else 0.0

    if not code:
        flash('Please enter a promo code.', 'warning')
        return redirect(url_for('cart.view_cart'))

    coupon = Coupon.query.filter_by(code=code, is_active=True).first()
    if not coupon:
        flash(f"Coupon '{code}' is not valid or has expired.", 'danger')
        return redirect(url_for('cart.view_cart'))

    valid, msg = coupon.is_valid_for(subtotal)
    if not valid:
        flash(msg, 'danger')
        return redirect(url_for('cart.view_cart'))

    session['coupon_code'] = code
    discount = coupon.calculate_discount(subtotal)
    flash(f"Coupon '{code}' applied successfully! Saved ${discount:.2f}.", 'success')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/remove-coupon', methods=['POST'])
def remove_coupon():
    session.pop('coupon_code', None)
    flash('Coupon removed.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/count')
def cart_count():
    cart = get_current_cart()
    return jsonify({'count': cart.total_items if cart else 0})
