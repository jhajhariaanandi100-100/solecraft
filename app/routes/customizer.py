import json
import uuid
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from flask_login import current_user
from app.models import db, CustomDesign, Cart, CartItem, Product

customizer_bp = Blueprint('customizer', __name__)

@customizer_bp.route('/')
def studio():
    load_id = request.args.get('load', type=int)
    preset_slug = request.args.get('product')
    initial_specs = None

    if load_id:
        design = db.session.get(CustomDesign, load_id)
        if design:
            initial_specs = design.get_specs()
            initial_specs['id'] = design.id
            initial_specs['title'] = design.title
    elif preset_slug:
        product = Product.query.filter_by(slug=preset_slug).first()
        if product:
            initial_specs = {
                'shoe_type': 'retro_low' if 'low' in product.slug else ('high_top' if 'high' in product.slug else ('aeroknit_runner' if 'runner' in product.slug or 'sprinter' in product.slug else 'urban_slipon')),
                'title': f"Custom {product.name}",
                'base_color': '#FFFFFF',
                'upper_material': product.material.split('&')[0].strip(),
                'upper_color': '#111111',
                'sole_color': '#FFFFFF',
                'lace_color': '#FF6B35',
                'tongue_color': '#111111',
                'heel_color': '#FF6B35',
                'pattern': 'none',
                'custom_text': '',
                'custom_text_color': '#FFFFFF',
                'calculated_price': product.price + 25.0
            }

    return render_template('customizer.html', initial_specs=json.dumps(initial_specs) if initial_specs else None)


@customizer_bp.route('/api/save', methods=['POST'])
def save_design():
    data = request.get_json() or {}
    
    title = data.get('title', 'My Custom SoleCraft').strip()
    shoe_type = data.get('shoe_type', 'retro_low')
    base_color = data.get('base_color', '#FFFFFF')
    upper_material = data.get('upper_material', 'Italian Leather')
    upper_color = data.get('upper_color', '#111111')
    sole_color = data.get('sole_color', '#FFFFFF')
    lace_color = data.get('lace_color', '#FF6B35')
    tongue_color = data.get('tongue_color', '#111111')
    heel_color = data.get('heel_color', '#FF6B35')
    pattern = data.get('pattern', 'none')
    custom_text = data.get('custom_text', '').strip()[:12] # max 12 chars
    custom_text_color = data.get('custom_text_color', '#FFFFFF')
    calculated_price = float(data.get('calculated_price', 185.0))
    preview_image = data.get('preview_image')

    user_id = current_user.id if current_user.is_authenticated else None

    design = CustomDesign(
        user_id=user_id,
        title=title,
        shoe_type=shoe_type,
        base_color=base_color,
        upper_material=upper_material,
        upper_color=upper_color,
        sole_color=sole_color,
        lace_color=lace_color,
        tongue_color=tongue_color,
        heel_color=heel_color,
        pattern=pattern,
        custom_text=custom_text,
        custom_text_color=custom_text_color,
        preview_image=preview_image,
        calculated_price=calculated_price,
        specs_json=json.dumps(data)
    )
    db.session.add(design)
    db.session.commit()

    return jsonify({
        'success': True,
        'design_id': design.id,
        'message': f"Design '{design.title}' successfully saved to your vault!"
    })


@customizer_bp.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json() or {}
    
    title = data.get('title', 'Custom SoleCraft Bespoke').strip()
    shoe_type = data.get('shoe_type', 'retro_low')
    base_color = data.get('base_color', '#FFFFFF')
    upper_material = data.get('upper_material', 'Italian Leather')
    upper_color = data.get('upper_color', '#111111')
    sole_color = data.get('sole_color', '#FFFFFF')
    lace_color = data.get('lace_color', '#FF6B35')
    tongue_color = data.get('tongue_color', '#111111')
    heel_color = data.get('heel_color', '#FF6B35')
    pattern = data.get('pattern', 'none')
    custom_text = data.get('custom_text', '').strip()[:12]
    custom_text_color = data.get('custom_text_color', '#FFFFFF')
    calculated_price = float(data.get('calculated_price', 185.0))
    preview_image = data.get('preview_image')
    size = data.get('size', 'US 9')
    quantity = int(data.get('quantity', 1))

    # Persist CustomDesign
    user_id = current_user.id if current_user.is_authenticated else None
    design = CustomDesign(
        user_id=user_id,
        title=title,
        shoe_type=shoe_type,
        base_color=base_color,
        upper_material=upper_material,
        upper_color=upper_color,
        sole_color=sole_color,
        lace_color=lace_color,
        tongue_color=tongue_color,
        heel_color=heel_color,
        pattern=pattern,
        custom_text=custom_text,
        custom_text_color=custom_text_color,
        preview_image=preview_image,
        calculated_price=calculated_price,
        specs_json=json.dumps(data)
    )
    db.session.add(design)
    db.session.flush()

    # Get or create Cart
    cart = None
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.flush()
    else:
        cart_id = session.get('cart_id')
        if cart_id:
            cart = db.session.get(Cart, cart_id)
        if not cart:
            cart = Cart(session_token=str(uuid.uuid4()))
            db.session.add(cart)
            db.session.flush()
            session['cart_id'] = cart.id

    # Add CartItem
    cart_item = CartItem(
        cart_id=cart.id,
        custom_design_id=design.id,
        size=size,
        quantity=quantity,
        unit_price=calculated_price,
        custom_data_json=json.dumps(data)
    )
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({
        'success': True,
        'cart_count': cart.total_items,
        'message': f"Bespoke '{title}' added to your shopping bag!",
        'cart_url': url_for('cart.view_cart')
    })


@customizer_bp.route('/presets')
def presets():
    # Studio curated bespoke inspiration
    preset_list = [
        {
            "title": "Obsidian Volt Low",
            "type": "retro_low",
            "base_color": "#111111",
            "upper_color": "#1E1E24",
            "sole_color": "#FFFFFF",
            "lace_color": "#FF6B35",
            "heel_color": "#FF6B35",
            "pattern": "racing_stripe",
            "material": "Italian Leather",
            "price": 195.0
        },
        {
            "title": "Alabaster Gold High",
            "type": "high_top",
            "base_color": "#F7F7F5",
            "upper_color": "#E5E5E0",
            "sole_color": "#222222",
            "lace_color": "#D4AF37",
            "heel_color": "#111111",
            "pattern": "geometric",
            "material": "Nubuck Suede",
            "price": 225.0
        },
        {
            "title": "Aero Nitro Racer",
            "type": "aeroknit_runner",
            "base_color": "#FFFFFF",
            "upper_color": "#000000",
            "sole_color": "#FF6B35",
            "lace_color": "#FFFFFF",
            "heel_color": "#FF6B35",
            "pattern": "gradient",
            "material": "AeroKnit Mesh",
            "price": 205.0
        }
    ]
    return jsonify(preset_list)
