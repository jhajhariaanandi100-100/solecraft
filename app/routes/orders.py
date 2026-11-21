import uuid
import random
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user
from app.models import db, Order, OrderItem, Payment, Cart, CartItem, Address, Coupon, CustomDesign

orders_bp = Blueprint('orders', __name__)

def generate_order_number():
    year = datetime.now(timezone.utc).year
    suffix = random.randint(10000, 99999)
    return f"SC-{year}-{suffix}"

@orders_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Retrieve active cart
    cart = None
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
    else:
        cart_id = session.get('cart_id')
        if cart_id:
            cart = db.session.get(Cart, cart_id)

    if not cart or not cart.items:
        flash('Your shopping bag is empty. Please select products first.', 'warning')
        return redirect(url_for('products.shop'))

    subtotal = cart.subtotal
    coupon_code = session.get('coupon_code')
    coupon_discount = 0.0
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
        if coupon:
            coupon_discount = coupon.calculate_discount(subtotal)

    shipping_fee = 0.0 if (subtotal >= 150.0) else 15.0
    taxable_amount = max(0.0, subtotal - coupon_discount)
    tax_amount = round(taxable_amount * 0.05, 2)
    final_total = round(taxable_amount + shipping_fee + tax_amount, 2)

    # Saved address for logged in user
    default_address = None
    if current_user.is_authenticated:
        default_address = Address.query.filter_by(user_id=current_user.id, is_default=True).first()
        if not default_address:
            default_address = Address.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        street_address = request.form.get('street_address', '').strip()
        apartment = request.form.get('apartment', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        postal_code = request.form.get('postal_code', '').strip()
        country = request.form.get('country', 'United States').strip()
        notes = request.form.get('notes', '').strip()
        payment_method = request.form.get('payment_method', 'Razorpay (Test)')

        if not all([full_name, email, phone, street_address, city, state, postal_code]):
            flash('Please complete all required customer & shipping address fields.', 'danger')
            return redirect(url_for('orders.checkout'))

        # Formatted shipping address
        addr_parts = [street_address]
        if apartment:
            addr_parts.append(apartment)
        addr_parts.append(f"{city}, {state} {postal_code}")
        addr_parts.append(country)
        formatted_address = ", ".join(addr_parts)

        # Generate unique order number
        order_number = generate_order_number()
        user_id = current_user.id if current_user.is_authenticated else None

        # Payment status determination
        payment_status = 'Paid' if payment_method != 'Cash on Delivery (COD)' else 'Pending'

        order = Order(
            order_number=order_number,
            user_id=user_id,
            total_amount=subtotal,
            discount_amount=coupon_discount,
            coupon_code=coupon_code if coupon_discount > 0 else None,
            shipping_fee=shipping_fee,
            tax_amount=tax_amount,
            final_amount=final_total,
            status='Order Placed',
            payment_method=payment_method,
            payment_status=payment_status,
            customer_name=full_name,
            customer_email=email,
            customer_phone=phone,
            shipping_address_text=formatted_address,
            tracking_number=f"TRK{random.randint(100000000, 999999999)}",
            notes=notes
        )
        db.session.add(order)
        db.session.flush()

        # Transfer items from Cart to Order
        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                custom_design_id=item.custom_design_id,
                product_name=item.display_name,
                size=item.size,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.line_total,
                custom_specs_json=item.custom_data_json if item.custom_design_id else (item.custom_design.specs_json if item.custom_design else None),
                item_image=item.display_image
            )
            db.session.add(order_item)

        # Record Payment
        payment = Payment(
            order_id=order.id,
            transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            payment_method=payment_method,
            amount=final_total,
            status='Success' if payment_status == 'Paid' else 'Pending',
            gateway_response=f"Verified through {payment_method} simulator."
        )
        db.session.add(payment)

        # Update coupon usage count
        if coupon_code and coupon_discount > 0:
            coupon_obj = Coupon.query.filter_by(code=coupon_code).first()
            if coupon_obj:
                coupon_obj.usage_count += 1

        # Clear Cart Items & Coupon
        for item in list(cart.items):
            db.session.delete(item)
        session.pop('coupon_code', None)

        db.session.commit()

        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('orders.success', order_number=order.order_number))

    return render_template(
        'checkout.html',
        cart=cart,
        subtotal=subtotal,
        coupon_discount=coupon_discount,
        coupon_code=coupon_code,
        shipping_fee=shipping_fee,
        tax_amount=tax_amount,
        final_total=final_total,
        default_address=default_address,
        razorpay_key=current_app.config.get('RAZORPAY_KEY_ID')
    )


@orders_bp.route('/success/<order_number>')
def success(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template('order_success.html', order=order)


@orders_bp.route('/track')
@orders_bp.route('/track/<order_number>')
def track(order_number=None):
    if not order_number:
        query_number = request.args.get('order_number', '').strip()
        if query_number:
            return redirect(url_for('orders.track', order_number=query_number))
        return render_template('order_tracking.html', order=None)

    order = Order.query.filter_by(order_number=order_number).first()
    if not order:
        flash(f"Order '{order_number}' not found. Please verify your order ID.", 'danger')
        return render_template('order_tracking.html', order=None)

    # Calculate status progression percentage
    # Steps: Order Placed -> Processing -> Customisation in Progress -> Shipped -> Out for Delivery -> Delivered
    steps = [
        'Order Placed',
        'Processing',
        'Customisation in Progress',
        'Shipped',
        'Out for Delivery',
        'Delivered'
    ]
    current_idx = 0
    try:
        current_idx = steps.index(order.status)
    except ValueError:
        current_idx = 1

    progress_percent = int(((current_idx + 1) / len(steps)) * 100)

    return render_template(
        'order_tracking.html',
        order=order,
        steps=steps,
        current_step_index=current_idx,
        progress_percent=progress_percent
    )
