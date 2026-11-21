from datetime import datetime, timedelta, timezone
import json
from .models import User, Category, Product, ProductImage, ProductVariant, Coupon, Review, CustomDesign, Address

def seed_initial_data(db):
    # Only seed if no users exist
    if User.query.first():
        return

    print("[*] Seeding database with initial SoleCraft store data...")

    # 1. Admin & Customer Users
    admin = User(
        email='admin@solecraft.com',
        full_name='SoleCraft Executive',
        phone='+1 (555) 019-2834',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)

    customer = User(
        email='customer@solecraft.com',
        full_name='Alex Rivera',
        phone='+1 (555) 482-9103',
        role='customer'
    )
    customer.set_password('customer123')
    db.session.add(customer)
    db.session.commit()

    # Customer Address
    address = Address(
        user_id=customer.id,
        full_name='Alex Rivera',
        street_address='742 Evergreen Terrace',
        apartment='Suite 4B',
        city='New York',
        state='NY',
        postal_code='10001',
        country='United States',
        phone='+1 (555) 482-9103',
        is_default=True
    )
    db.session.add(address)

    # 2. Categories
    categories_data = [
        {"name": "Sneakers", "slug": "sneakers", "desc": "Iconic low-top and high-top street silhouettes engineered for bold expression."},
        {"name": "Running Shoes", "slug": "running-shoes", "desc": "High-rebound nitrogen-infused foam trainers built for marathon pacing and track sprints."},
        {"name": "Casual Shoes", "slug": "casual-shoes", "desc": "Effortless weekend slip-ons, minimal court shoes, and daily lifestyle essentials."},
        {"name": "Sports Shoes", "slug": "sports-shoes", "desc": "Court-ready traction, lateral lockdown, and impact-absorption performance shoes."},
        {"name": "Formal Shoes", "slug": "formal-shoes", "desc": "Hand-buffed Italian leather brogues, modern derby shoes, and bespoke dress footwear."},
        {"name": "Women's Footwear", "slug": "womens-footwear", "desc": "Contemporary fashion-forward silhouettes sculpted specifically for feminine proportions."},
        {"name": "Men's Footwear", "slug": "mens-footwear", "desc": "Precision crafted masculine footwear bridging raw streetwear and refined luxury."},
        {"name": "Unisex Collection", "slug": "unisex-collection", "desc": "Timeless, gender-neutral designs celebrating universal form, balance, and pure craft."}
    ]

    cats = {}
    for c in categories_data:
        cat = Category(name=c["name"], slug=c["slug"], description=c["desc"])
        db.session.add(cat)
        cats[c["slug"]] = cat

    db.session.commit()

    # 3. Products
    products_data = [
        {
            "name": "SoleCraft Retro Low '77",
            "slug": "solecraft-retro-low-77",
            "tagline": "The timeless heritage low-top redefined in full-grain calfskin.",
            "desc": "Drawing inspiration from 1970s basketball courts, the Retro Low '77 combines clean lines with hand-stitched detailing. Engineered with an anatomical OrthoLite footbed and vulcanized gum rubber sole.",
            "price": 165.0,
            "discount_price": 140.0,
            "sku": "SC-RL-077",
            "stock": 45,
            "is_featured": True,
            "is_bestseller": True,
            "category": "sneakers",
            "shoe_type": "Sneakers",
            "gender": "Unisex",
            "material": "Full-grain Italian Calfskin & Suede",
            "colors": "Bone White / Onyx, Triple White, Electric Sunset",
            "sizes": "US 7, US 7.5, US 8, US 8.5, US 9, US 9.5, US 10, US 10.5, US 11, US 12",
            "main_image": "/static/images/products/retro-low-white.svg"
        },
        {
            "name": "Apex High-Top Studio Noir",
            "slug": "apex-high-top-studio-noir",
            "tagline": "Architectural high-collar silhouette with magnetic buckle collar.",
            "desc": "Built for urban tastemakers who refuse to blend in. The Apex High-Top boasts reinforced ankle padding, vegetable-tanned nappa leather overlays, and deep herringbone traction soles.",
            "price": 210.0,
            "discount_price": None,
            "sku": "SC-AH-101",
            "stock": 28,
            "is_featured": True,
            "is_bestseller": True,
            "category": "sneakers",
            "shoe_type": "Sneakers",
            "gender": "Men",
            "material": "Nappa Leather & Ballistic Nylon",
            "colors": "Triple Obsidian, Black Volt, Vintage Olive",
            "sizes": "US 8, US 8.5, US 9, US 9.5, US 10, US 10.5, US 11, US 12, US 13",
            "main_image": "/static/images/products/apex-high-black.svg"
        },
        {
            "name": "AeroStrata Hyper-Runner",
            "slug": "aerostrata-hyper-runner",
            "tagline": "Sub-200 gram featherlight road racer with dual-density nitrogen foam.",
            "desc": "Experience weightless propulsion. The AeroStrata features a 3D-knitted upper for dynamic breathability and a curved carbon-composite plate for maximum energy return on every stride.",
            "price": 195.0,
            "discount_price": 175.0,
            "sku": "SC-AR-402",
            "stock": 50,
            "is_featured": True,
            "is_bestseller": True,
            "category": "running-shoes",
            "shoe_type": "Running Shoes",
            "gender": "Unisex",
            "material": "AeroKnit Engineered Mesh & Nitrogen Foam",
            "colors": "Volt Orange / Frost, Lunar Silver, Solar Red",
            "sizes": "US 6, US 6.5, US 7, US 7.5, US 8, US 8.5, US 9, US 9.5, US 10, US 11",
            "main_image": "/static/images/products/aero-runner-orange.svg"
        },
        {
            "name": "Veloce Carbon Sprinter",
            "slug": "veloce-carbon-sprinter",
            "tagline": "Track-inspired aerodynamic silhouette designed for daily pacing.",
            "desc": "Zero compromises between high performance and minimalist Scandinavian design. Lightweight micro-mesh upper with reflective 3M heel accents for dusk runs.",
            "price": 180.0,
            "discount_price": 155.0,
            "sku": "SC-VC-505",
            "stock": 35,
            "is_featured": False,
            "is_bestseller": False,
            "category": "running-shoes",
            "shoe_type": "Running Shoes",
            "gender": "Men",
            "material": "Ripstop Monofilament Mesh & Carbon Fiber",
            "colors": "Stealth Black, Hyper Crimson, Chalk White",
            "sizes": "US 8, US 8.5, US 9, US 9.5, US 10, US 11, US 12",
            "main_image": "/static/images/products/veloce-sprinter.svg"
        },
        {
            "name": "Milano Luxe Slip-On",
            "slug": "milano-luxe-slip-on",
            "tagline": "Pure minimalist luxury crafted from ultra-soft suede velour.",
            "desc": "Seamless, unlined Italian suede slip-on shoe that molds to your feet like a glove. Finished with a natural latex rubber sole and custom monogram heel tab.",
            "price": 175.0,
            "discount_price": None,
            "sku": "SC-ML-204",
            "stock": 30,
            "is_featured": True,
            "is_bestseller": False,
            "category": "casual-shoes",
            "shoe_type": "Casual Shoes",
            "gender": "Unisex",
            "material": "Italian Suede Velour & Natural Latex",
            "colors": "Sand Beige, Espresso Brown, Slate Grey",
            "sizes": "US 7, US 8, US 9, US 10, US 11, US 12",
            "main_image": "/static/images/products/milano-slipon.svg"
        },
        {
            "name": "SoHo Court Minimalist",
            "slug": "soho-court-minimalist",
            "tagline": "The pristine low-profile court sneaker for elevated daily wear.",
            "desc": "Stripped of all external logos for pure architectural clarity. Features gold-foil debossed model numbers on the outer heel and waxed organic cotton laces.",
            "price": 150.0,
            "discount_price": 130.0,
            "sku": "SC-SH-303",
            "stock": 60,
            "is_featured": True,
            "is_bestseller": True,
            "category": "casual-shoes",
            "shoe_type": "Casual Shoes",
            "gender": "Unisex",
            "material": "Full Grain Box Calfskin",
            "colors": "Pristine White, Raw Ecru, Midnight Navy",
            "sizes": "US 6, US 7, US 8, US 9, US 10, US 11, US 12",
            "main_image": "/static/images/products/soho-court.svg"
        },
        {
            "name": "CourtForce Pro Slam",
            "slug": "courtforce-pro-slam",
            "tagline": "Multi-directional herringbone grip for explosive indoor hardwood cuts.",
            "desc": "Engineered for intense lateral cutting and quick stops. TPU midfoot shank prevents torsion while decoupled heel pods disperse high-velocity landing impacts.",
            "price": 185.0,
            "discount_price": None,
            "sku": "SC-CF-901",
            "stock": 40,
            "is_featured": False,
            "is_bestseller": False,
            "category": "sports-shoes",
            "shoe_type": "Sports Shoes",
            "gender": "Men",
            "material": "Fused TPU Mesh & Non-marking Gum",
            "colors": "Electric Orange / Cyber Black, Ice Blue",
            "sizes": "US 8, US 8.5, US 9, US 9.5, US 10, US 11, US 12, US 13",
            "main_image": "/static/images/products/courtforce-slam.svg"
        },
        {
            "name": "Kallisto Derby Bespoke",
            "slug": "kallisto-derby-bespoke",
            "tagline": "Goodyear-welted modern dress shoe with an aggressive lugged commando sole.",
            "desc": "A radical collision between traditional British dress shoemaking and brutalist street fashion. Built from French box calf leather that patinates richly with age.",
            "price": 260.0,
            "discount_price": 225.0,
            "sku": "SC-KD-701",
            "stock": 20,
            "is_featured": True,
            "is_bestseller": False,
            "category": "formal-shoes",
            "shoe_type": "Formal Shoes",
            "gender": "Men",
            "material": "French Box Calfskin & Vibram Lugged Sole",
            "colors": "Polished Black, Burgundy Cordovan, Oxblood",
            "sizes": "US 8, US 8.5, US 9, US 9.5, US 10, US 11, US 12",
            "main_image": "/static/images/products/kallisto-derby.svg"
        },
        {
            "name": "Oxford Monolith Brogue",
            "slug": "oxford-monolith-brogue",
            "tagline": "Laser-perforated wingtip brogueing meet modern anatomical fit.",
            "desc": "Redefining black-tie refinement. Hand-burnished toe medallion, closed lacing system, and Goodyear-welted double oak-bark leather sole with brass heel pegs.",
            "price": 280.0,
            "discount_price": None,
            "sku": "SC-OM-702",
            "stock": 18,
            "is_featured": False,
            "is_bestseller": False,
            "category": "formal-shoes",
            "shoe_type": "Formal Shoes",
            "gender": "Men",
            "material": "Antiqued Calf Leather & Double Oak Sole",
            "colors": "Deep Espresso, Onyx Mirror Polish",
            "sizes": "US 8, US 9, US 10, US 11, US 12",
            "main_image": "/static/images/products/oxford-monolith.svg"
        },
        {
            "name": "Aura Platform Horizon",
            "slug": "aura-platform-horizon",
            "tagline": "Sculpted 45mm platform sneaker designed with feminine proportions.",
            "desc": "Elevate your daily silhouette. The Aura Platform delivers exaggerated height without the heavy weight, using an ultra-light EVA midsole core wrapped in buttery lambskin.",
            "price": 190.0,
            "discount_price": 165.0,
            "sku": "SC-AP-801",
            "stock": 35,
            "is_featured": True,
            "is_bestseller": True,
            "category": "womens-footwear",
            "shoe_type": "Sneakers",
            "gender": "Women",
            "material": "Lambskin Leather & Sculpted EVA",
            "colors": "Alabaster White / Blush, Sage Mist, Metallic Gold",
            "sizes": "US 5, US 5.5, US 6, US 6.5, US 7, US 7.5, US 8, US 8.5, US 9, US 9.5",
            "main_image": "/static/images/products/aura-platform.svg"
        },
        {
            "name": "Serena Knit Cloud Runner",
            "slug": "serena-knit-cloud-runner",
            "tagline": "Slip-on sock knit silhouette that gently hugs the foot like silk.",
            "desc": "Engineered for women on the move. Seamless one-piece stretch knit upper paired with sculpted arch support and bouncy rebound cushioning.",
            "price": 160.0,
            "discount_price": 135.0,
            "sku": "SC-SK-802",
            "stock": 42,
            "is_featured": False,
            "is_bestseller": True,
            "category": "womens-footwear",
            "shoe_type": "Running Shoes",
            "gender": "Women",
            "material": "Recycled Poly Knit & Cloud-Lite Foam",
            "colors": "Rose Quartz, Triple Black, Lavender Mist",
            "sizes": "US 5, US 6, US 7, US 8, US 9, US 10",
            "main_image": "/static/images/products/serena-knit.svg"
        },
        {
            "name": "Chronos Vanguard Boot",
            "slug": "chronos-vanguard-boot",
            "tagline": "Rugged Chelsea hybrid with waterproof tumbled leather and elastic gussets.",
            "desc": "From downtown gallery walks to wet autumn commutes. Built with weather-sealed storm welting, pull tabs front and rear, and slip-resistant tread.",
            "price": 240.0,
            "discount_price": 210.0,
            "sku": "SC-CV-601",
            "stock": 25,
            "is_featured": True,
            "is_bestseller": False,
            "category": "mens-footwear",
            "shoe_type": "Casual Shoes",
            "gender": "Men",
            "material": "Tumbled Waterproof Leather & Vibram Commando",
            "colors": "Oiled Havana Brown, Matte Black",
            "sizes": "US 8, US 9, US 10, US 11, US 12, US 13",
            "main_image": "/static/images/products/chronos-vanguard.svg"
        },
        {
            "name": "Monolith Zero Trainer",
            "slug": "monolith-zero-trainer",
            "tagline": "Zero-drop barefoot-inspired luxury trainer with wide anatomical toe box.",
            "desc": "Natural foot alignment meets high fashion. Strengthen foot muscles and feel grounded with a flexible 4mm outsole and breathable organic cotton canvas lining.",
            "price": 155.0,
            "discount_price": None,
            "sku": "SC-MZ-301",
            "stock": 38,
            "is_featured": False,
            "is_bestseller": False,
            "category": "unisex-collection",
            "shoe_type": "Sneakers",
            "gender": "Unisex",
            "material": "Organic Duck Canvas & Gum Sole",
            "colors": "Raw Canvas, Coal Black, Hunter Green",
            "sizes": "US 6, US 7, US 8, US 9, US 10, US 11, US 12",
            "main_image": "/static/images/products/monolith-zero.svg"
        },
        {
            "name": "SoleCraft Signature Bespoke",
            "slug": "solecraft-signature-bespoke",
            "tagline": "The blank canvas waiting for your signature touch in our Custom Studio.",
            "desc": "Specially calibrated for complete personalized customization. Select every single component: base leather, laces, midsole, outsole, tongue, heel tab, custom patterns, and debossed initials.",
            "price": 185.0,
            "discount_price": None,
            "sku": "SC-BESPOKE-001",
            "stock": 999,
            "is_featured": True,
            "is_bestseller": True,
            "category": "unisex-collection",
            "shoe_type": "Sneakers",
            "gender": "Unisex",
            "material": "Bespoke Multi-Material System",
            "colors": "Custom Palette Configurable",
            "sizes": "US 5, US 6, US 7, US 8, US 9, US 10, US 11, US 12, US 13",
            "main_image": "/static/images/products/custom-default.svg"
        }
    ]

    for p in products_data:
        prod = Product(
            category_id=cats[p["category"]].id,
            name=p["name"],
            slug=p["slug"],
            tagline=p["tagline"],
            description=p["desc"],
            price=p["price"],
            discount_price=p["discount_price"],
            sku=p["sku"],
            stock=p["stock"],
            is_featured=p["is_featured"],
            is_bestseller=p["is_bestseller"],
            shoe_type=p["shoe_type"],
            gender=p["gender"],
            material=p["material"],
            colors=p["colors"],
            sizes=p["sizes"],
            main_image=p["main_image"]
        )
        db.session.add(prod)
        db.session.flush()

        # Add primary image
        img = ProductImage(product_id=prod.id, image_url=p["main_image"], is_primary=True)
        db.session.add(img)

        # Add sample review
        rev = Review(
            product_id=prod.id,
            user_id=customer.id,
            rating=5 if p["is_bestseller"] else 4,
            title="Exceptional craftsmanship and unmatched comfort",
            comment="The leather quality is noticeably superior to mass-market sneakers. Fits true to size and the silhouette gets compliments every single time I wear it.",
            verified_purchase=True
        )
        db.session.add(rev)

    db.session.commit()

    # 4. Coupons
    coupons = [
        Coupon(code="WELCOME20", discount_percent=20.0, min_order_value=100.0, max_discount=60.0, valid_to=datetime.now(timezone.utc) + timedelta(days=90), is_active=True),
        Coupon(code="SOLE10", discount_percent=10.0, min_order_value=50.0, max_discount=30.0, valid_to=datetime.now(timezone.utc) + timedelta(days=60), is_active=True),
        Coupon(code="CRAFT50", discount_amount=50.0, min_order_value=200.0, valid_to=datetime.now(timezone.utc) + timedelta(days=30), is_active=True)
    ]
    for c in coupons:
        db.session.add(c)

    # 5. Sample Custom Design for customer
    sample_design = CustomDesign(
        user_id=customer.id,
        title="Sunset Volt Edition",
        shoe_type="retro_low",
        base_color="#111111",
        upper_material="Italian Leather",
        upper_color="#1A1A1A",
        sole_color="#FFFFFF",
        lace_color="#FF6B35",
        tongue_color="#111111",
        heel_color="#FF6B35",
        pattern="racing_stripe",
        custom_text="AR-77",
        custom_text_color="#FFFFFF",
        calculated_price=197.0,
        specs_json=json.dumps({
            "shoe_type": "retro_low",
            "base_color": "#111111",
            "upper_material": "Italian Leather",
            "upper_color": "#1A1A1A",
            "sole_color": "#FFFFFF",
            "lace_color": "#FF6B35",
            "tongue_color": "#111111",
            "heel_color": "#FF6B35",
            "pattern": "racing_stripe",
            "custom_text": "AR-77",
            "custom_text_color": "#FFFFFF",
            "calculated_price": 197.0
        })
    )
    db.session.add(sample_design)
    db.session.commit()
    print("[*] Database seeded successfully!")
