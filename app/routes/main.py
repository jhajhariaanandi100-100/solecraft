from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.models import Product, Category, Review, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_products = Product.query.filter_by(is_featured=True).limit(4).all()
    bestseller_products = Product.query.filter_by(is_bestseller=True).limit(8).all()
    latest_reviews = Review.query.order_by(Review.created_at.desc()).limit(3).all()
    categories = Category.query.all()
    
    return render_template(
        'index.html',
        featured_products=featured_products,
        bestsellers=bestseller_products,
        reviews=latest_reviews,
        categories=categories
    )

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not name or not email or not message:
            flash('Please complete all required fields.', 'danger')
        else:
            flash('Thank you for reaching out to SOLECRAFT Concierge. Our bespoke footwear team will respond within 24 hours.', 'success')
            return redirect(url_for('main.contact'))

    return render_template('contact.html')

@main_bp.route('/newsletter', methods=['POST'])
def newsletter():
    email = request.form.get('email')
    if not email or '@' not in email:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Please provide a valid email address.'}), 400
        flash('Please enter a valid email address.', 'danger')
        return redirect(request.referrer or url_for('main.index'))
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': 'Welcome to the SoleCraft Inner Circle! Check your inbox for your 15% VIP welcome code.'})
    
    flash('Welcome to the SoleCraft Inner Circle! Check your inbox for your 15% VIP welcome code.', 'success')
    return redirect(request.referrer or url_for('main.index'))
