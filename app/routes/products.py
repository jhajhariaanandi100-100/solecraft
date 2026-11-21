from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from app.models import db, Product, Category, Review, Wishlist

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def shop():
    query = Product.query

    # Search keyword
    q = request.args.get('q', '').strip()
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%') | Product.description.ilike(f'%{q}%'))

    # Category filter
    category_slug = request.args.get('category', '').strip()
    selected_category = None
    if category_slug and category_slug != 'all':
        selected_category = Category.query.filter_by(slug=category_slug).first()
        if selected_category:
            query = query.filter_by(category_id=selected_category.id)

    # Shoe Type filter
    shoe_type = request.args.get('type', '').strip()
    if shoe_type and shoe_type != 'all':
        query = query.filter(Product.shoe_type.ilike(f'%{shoe_type}%'))

    # Gender filter
    gender = request.args.get('gender', '').strip()
    if gender and gender != 'all':
        query = query.filter((Product.gender == gender) | (Product.gender == 'Unisex'))

    # Price range
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Sorting
    sort_by = request.args.get('sort', 'popular')
    if sort_by == 'price-asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price-desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    else: # popular
        query = query.order_by(Product.is_bestseller.desc(), Product.is_featured.desc(), Product.id.asc())

    products = query.all()
    categories = Category.query.all()

    # User wishlist product IDs
    user_wishlist_ids = set()
    if current_user.is_authenticated:
        user_wishlist_ids = {w.product_id for w in Wishlist.query.filter_by(user_id=current_user.id).all()}

    return render_template(
        'shop.html',
        products=products,
        categories=categories,
        selected_category=selected_category,
        q=q,
        current_sort=sort_by,
        current_type=shoe_type,
        current_gender=gender,
        min_price=min_price,
        max_price=max_price,
        user_wishlist_ids=user_wishlist_ids,
        total_count=len(products)
    )


@products_bp.route('/<slug>')
def detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()

    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = Wishlist.query.filter_by(user_id=current_user.id, product_id=product.id).first() is not None

    return render_template(
        'product_detail.html',
        product=product,
        related_products=related_products,
        in_wishlist=in_wishlist
    )


@products_bp.route('/quick-view/<int:product_id>')
def quick_view(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'price': product.price,
        'discount_price': product.discount_price,
        'effective_price': product.effective_price,
        'has_discount': product.has_discount,
        'discount_percent': product.discount_percent,
        'description': product.description,
        'tagline': product.tagline,
        'material': product.material,
        'shoe_type': product.shoe_type,
        'sizes': product.size_list,
        'colors': product.color_list,
        'main_image': product.main_image,
        'rating': product.average_rating,
        'reviews_count': product.review_count,
        'detail_url': url_for('products.detail', slug=product.slug)
    })


@products_bp.route('/review/<int:product_id>', methods=['POST'])
@login_required
def submit_review(product_id):
    product = Product.query.get_or_404(product_id)
    rating = request.form.get('rating', 5, type=int)
    title = request.form.get('title', '').strip()
    comment = request.form.get('comment', '').strip()

    if not comment:
        flash('Please provide review comments.', 'danger')
        return redirect(url_for('products.detail', slug=product.slug))

    review = Review(
        product_id=product.id,
        user_id=current_user.id,
        rating=max(1, min(5, rating)),
        title=title,
        comment=comment,
        verified_purchase=True
    )
    db.session.add(review)
    db.session.commit()

    flash('Thank you for submitting your review!', 'success')
    return redirect(url_for('products.detail', slug=product.slug))
