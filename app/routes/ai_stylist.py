import json
from flask import Blueprint, render_template, request, jsonify, url_for
from app.models import Product, Category

ai_stylist_bp = Blueprint('ai_stylist', __name__)

@ai_stylist_bp.route('/')
def assistant():
    categories = Category.query.all()
    return render_template('ai_assistant.html', categories=categories)

@ai_stylist_bp.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json() or request.form

    vibe = data.get('vibe', 'minimalist') # minimalist, streetwear, athletic, luxury_formal, casual
    occasion = data.get('occasion', 'daily') # daily, gym, nightout, work, weekend
    colors = data.get('colors', 'monochrome') # monochrome, volt_orange, earthy, pastel
    budget = data.get('budget', '150_220') # under_150, 150_220, above_220
    footwear_type = data.get('footwear_type', 'all') # sneakers, running-shoes, casual-shoes, formal-shoes, all
    custom_interest = data.get('custom_interest', 'both')

    # Archetype Generator
    archetypes = {
        'minimalist': {
            'title': 'The Urban Purist',
            'quote': 'Understated precision. Architectural silhouettes that let materials speak for themselves.',
            'base_accent': '#FF6B35',
            'base_color': '#FFFFFF'
        },
        'streetwear': {
            'title': 'The Hype Alchemist',
            'quote': 'Bold proportions, high-contrast panels, and graphic statements crafted to command the pavement.',
            'base_accent': '#FF6B35',
            'base_color': '#111111'
        },
        'athletic': {
            'title': 'The Velocity Dynamic',
            'quote': 'Aerodynamic propulsion engineered with high-rebound foams for non-stop energy return.',
            'base_accent': '#FF6B35',
            'base_color': '#FFFFFF'
        },
        'luxury_formal': {
            'title': 'The Bespoke Tastemaker',
            'quote': 'Goodyear-welted tradition fused with brutalist edge. Impeccable leather with an unmistakable presence.',
            'base_accent': '#D4AF37',
            'base_color': '#1A1A1A'
        },
        'casual': {
            'title': 'The Effortless Navigator',
            'quote': 'Unstructured comfort, buttery soft suedes, and easy slip-on transitions from desk to lounge.',
            'base_accent': '#9C8A79',
            'base_color': '#F7F7F5'
        }
    }

    user_archetype = archetypes.get(vibe, archetypes['minimalist'])

    # Query catalog products
    products = Product.query.all()
    scored_products = []

    for p in products:
        score = 60 # Base score

        # Type / Category matching
        if footwear_type != 'all':
            if p.category.slug == footwear_type or footwear_type in p.shoe_type.lower():
                score += 25
            else:
                score -= 15

        # Vibe matching
        p_name = p.name.lower()
        p_desc = p.description.lower()
        if vibe == 'streetwear' and ('high' in p_name or 'retro' in p_name or 'apex' in p_name):
            score += 20
        elif vibe == 'minimalist' and ('court' in p_name or 'zero' in p_name or 'retro' in p_name or 'milano' in p_name):
            score += 20
        elif vibe == 'athletic' and ('runner' in p_name or 'sprinter' in p_name or 'slam' in p_name or 'aero' in p_name):
            score += 20
        elif vibe == 'luxury_formal' and ('derby' in p_name or 'oxford' in p_name or 'boot' in p_name):
            score += 25
        elif vibe == 'casual' and ('slip-on' in p_name or 'court' in p_name or 'cloud' in p_name):
            score += 20

        # Occasion matching
        if occasion == 'gym' and ('runner' in p_name or 'slam' in p_name):
            score += 15
        elif occasion == 'work' and ('derby' in p_name or 'oxford' in p_name or 'court' in p_name):
            score += 15
        elif occasion == 'nightout' and ('apex' in p_name or 'kallisto' in p_name or 'bespoke' in p_name):
            score += 15

        # Budget matching
        if budget == 'under_150':
            if p.effective_price <= 150:
                score += 15
            else:
                score -= 10
        elif budget == '150_220':
            if 140 <= p.effective_price <= 220:
                score += 15
            else:
                score -= 5
        elif budget == 'above_220':
            if p.effective_price >= 200:
                score += 15

        # Color matching
        p_colors = p.colors.lower()
        if colors == 'volt_orange' and ('orange' in p_colors or 'volt' in p_colors):
            score += 10
        elif colors == 'monochrome' and ('black' in p_colors or 'white' in p_colors or 'obsidian' in p_colors):
            score += 10
        elif colors == 'earthy' and ('brown' in p_colors or 'beige' in p_colors or 'green' in p_colors or 'canvas' in p_colors):
            score += 10

        # Bestseller bonus
        if p.is_bestseller:
            score += 5

        match_pct = min(99, max(65, score))

        # Dynamic AI justification sentence
        justification = f"Engineered for your {vibe.title()} aesthetic and {occasion.title()} lifestyle. Features {p.material.split('&')[0].strip()} for lasting durability and a silhouette calibrated for {p.gender} fit."

        scored_products.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'category': p.category.name,
            'price': p.price,
            'effective_price': p.effective_price,
            'has_discount': p.has_discount,
            'image': p.main_image,
            'match_percent': match_pct,
            'reason': justification,
            'url': url_for('products.detail', slug=p.slug)
        })

    # Sort descending by match score
    scored_products.sort(key=lambda x: x['match_percent'], reverse=True)
    top_picks = scored_products[:4]

    # Customizer AI Preset Recipe
    ai_custom_preset = {
        'shoe_type': 'retro_low' if vibe in ['minimalist', 'casual'] else ('high_top' if vibe == 'streetwear' else ('aeroknit_runner' if vibe == 'athletic' else 'urban_slipon')),
        'title': f"AI {user_archetype['title']} Edition",
        'base_color': '#FFFFFF' if colors in ['monochrome', 'pastel'] else ('#111111' if colors == 'volt_orange' else '#EAE7DC'),
        'upper_color': '#111111' if vibe in ['streetwear', 'luxury_formal'] else '#2B2D42',
        'sole_color': '#FFFFFF',
        'lace_color': '#FF6B35' if colors == 'volt_orange' else '#111111',
        'heel_color': '#FF6B35',
        'pattern': 'racing_stripe' if vibe == 'streetwear' else 'none',
        'material': 'Italian Leather',
        'estimated_price': 185.0
    }

    response_data = {
        'success': True,
        'archetype': user_archetype,
        'recommendations': top_picks,
        'custom_preset': ai_custom_preset,
        'summary': f"Based on your preference for {vibe.replace('_', ' ').title()} footwear during {occasion.replace('_', ' ')} moments with a {colors.replace('_', ' ')} palette, our AI Stylist identified your signature silhouette and curated top footwear selections."
    }

    return jsonify(response_data)
