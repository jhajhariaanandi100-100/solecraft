# SOLECRAFT – Personalise Your Every Step

> **"Your Style. Your Design. Your Sole."**

**SOLECRAFT** is a modern, premium, fully functional end-to-end e-commerce footwear brand platform. It seamlessly unifies ready-to-wear luxury footwear shopping with an interactive **3D/SVG Shoe Customisation Studio** and an **AI Style Recommendation Assistant**.

---

## 🌟 Key Features

### 1. Ready-To-Wear Footwear Boutique
- **Full Catalog**: Sneakers, Running Shoes, Casual Shoes, Sports Shoes, Formal Shoes, Women's, Men's, and Unisex collections.
- **Search & Advanced Filtering**: Filter by category, shoe type, gender fit, and price range. Real-time sorting by popularity, price (asc/desc), and newest arrivals.
- **Product Details**: Multi-angle image gallery, dynamic rating & verified customer reviews, size selector with size conversion guide, quantity controls, "Add to Bag", and direct **"Customise This Design"** button.
- **Wishlist**: Real-time heart bookmarking for registered and guest clients.
- **Quick View Modal**: Instant AJAX-powered product previews without page reloads.

### 2. Interactive 3D / SVG Shoe Customisation Studio (Hero Feature)
- **4 Iconic Silhouettes**:
  1. *Retro Low '77* (Heritage court low-top)
  2. *Apex High-Top* (Architectural street high-collar)
  3. *AeroStrata Runner* (Sub-200g aerodynamic trainer)
  4. *Milano Slip-On* (Minimalist Italian velour slip-on)
- **Multi-Component Layer Colorways**:
  - Base Upper, Quarter Panel, Outsole & Midsole, Laces, Tongue, Heel Counter, Signature Wave.
  - 12+ curated atelier shades with real-time SVG DOM updates.
- **Material Finishes**:
  - Full-Grain Italian Calfskin (+$20.00)
  - Velour Nubuck Suede (+$15.00)
  - AeroKnit Engineered Mesh (+$10.00)
  - Organic Duck Canvas (Included)
  - Platinum Sheen Metallic (+$30.00)
- **Graphic Pattern Overlays**:
  - Solid Clean, Racing Stripe, Urban Camo, Geometric Grid, Sunset Glow (+$12.00).
- **Personalized Monogram Debossing**:
  - Laser-engraved custom text or initials (up to 10 characters) stamped directly onto the heel counter with custom foil color selection (+$10.00).
- **Studio Tools**:
  - Undo & Redo history stacks (up to 25 states)
  - Reset to baseline
  - Multi-angle views (Lateral Side View and Mirrored Medial Profile)
  - Dynamic Live Price Calculation ticker
  - "Save to Vault" (persists custom design to user profile)
  - "Add Bespoke to Bag" (creates bespoke CartItem with full SVG specifications)

### 3. AI Style Assistant
- **5-Step Lifestyle Questionnaire**:
  - Style Aesthetic (Minimalist, Streetwear, Athletic, Luxury Formal, Casual)
  - Occasion (Daily Street, Gym/Track, Office/Studio, Night Out)
  - Color Mood (Monochrome, Electric Volt, Earthy, Pastel)
  - Preferred Category
  - Budget Tolerance
- **Algorithmic Profiling**:
  - Calculates compatibility match scores (65% – 99%).
  - Assigns an **AI Style Archetype** (*The Urban Purist*, *The Hype Alchemist*, *The Velocity Dynamic*, etc.) with tailored philosophical rationale.
  - Curates top matching silhouettes.
  - Automatically synthesizes a bespoke customizer preset and launches it directly in the 3D Studio!

### 4. Shopping Bag & Checkout
- **Real Cart Calculations**: Line item totals, quantity stepper, removal.
- **Coupon & Promo Engine**: Real database coupon validation (e.g., `WELCOME20`, `SOLE10`, `CRAFT50`) with min-order thresholds and savings breakdown.
- **Shipping Rules**: Free bespoke shipping on orders over $150, else $15.
- **Taxes**: Automated sales tax calculation.
- **Payment Gateway Simulation**:
  - Razorpay Test Mode Simulator (with test key integration)
  - Credit / Debit Card test simulator
  - UPI ID test simulator
  - Cash on Delivery (COD)

### 5. Live Order Tracking
- **Interactive 6-Stage Timeline Stepper**:
  1. *Order Placed*
  2. *Processing*
  3. *Customisation in Progress* (Artisan Lasting & Monogram Debossing)
  4. *Shipped* (FedEx Priority tracking ID)
  5. *Out for Delivery*
  6. *Delivered*
- Searchable by Order Number (e.g., `SC-2026-XXXXX`).

### 6. Executive Admin Operations Hub
- **Executive Analytics**: Total sales, total orders, custom shoes crafted count, registered client base.
- **Chart.js Visualizations**: Daily revenue trend line chart and category distribution doughnut chart.
- **Product Management (CRUD)**: Add new shoes with image upload, edit prices, update descriptions, manage stock alerts, delete silhouettes.
- **Order Pipeline**: Filter orders by status and transition orders through fulfillment stages.
- **Bespoke Workbench**: Specialized inspector for custom footwear orders showing full color hexes, material choices, and debossed monogram initials.
- **Coupon Manager**: Launch new promo codes, configure discounts, set expiry, and toggle active status.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.14+, Flask 3.1+, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Werkzeug
- **Database**: SQLite (local development) / PostgreSQL or MySQL (production via `DATABASE_URL`)
- **Frontend**: HTML5, CSS3 (Tailored Luxury Design System), Vanilla JavaScript (ES6+), Bootstrap 5.3
- **Graphics & Customizer**: Layered SVG Vector Engine, HTML5 Canvas
- **Data Visualization**: Chart.js 4.4
- **Deployment Ready**: Gunicorn, `Procfile`, `render.yaml` for Render 1-click deploy

---

## 🚀 Quickstart & Local Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/solecraft.git
cd solecraft
```

### 2. Create and activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate SVG Brand & Product Assets (if needed)
```bash
python generate_assets.py
```

### 5. Run the Application
```bash
python run.py
```
Open your browser at **`http://localhost:5000`**

The database will be automatically initialized and pre-seeded with 14 footwear silhouettes, sample customer reviews, demo coupons, and accounts!

---

## 🔑 Demo Credentials

| Role | Email | Password |
|---|---|---|
| **Executive Admin** | `admin@solecraft.com` | `admin123` |
| **Customer Client** | `customer@solecraft.com` | `customer123` |

### Active Promo Codes:
- `WELCOME20` — 20% discount on orders over $100
- `SOLE10` — 10% discount on orders over $50
- `CRAFT50` — $50 off orders over $200

---

## ☁️ Deployment Guide (Render)

This repository includes `render.yaml` and `Procfile` configured for Render web services:

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: SoleCraft Bespoke Footwear Platform"
   git remote add origin https://github.com/<your-username>/solecraft.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com).
   - Click **New +** &rarr; **Blueprint** (or **Web Service**).
   - Connect your GitHub repository `solecraft`.
   - Render will automatically read `render.yaml` or you can configure:
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app`
   - Click **Deploy**.

---

## 📐 Relational Database Schema

- `users` (id, email, password_hash, full_name, phone, role, created_at)
- `addresses` (id, user_id, full_name, street_address, city, state, postal_code, country, phone, is_default)
- `categories` (id, name, slug, description, image_url)
- `products` (id, category_id, name, slug, tagline, description, price, discount_price, sku, stock, is_featured, is_bestseller, shoe_type, gender, material, colors, sizes, main_image)
- `product_images` (id, product_id, image_url, is_primary)
- `product_variants` (id, product_id, size, color, stock)
- `custom_designs` (id, user_id, title, shoe_type, base_color, upper_material, upper_color, sole_color, lace_color, tongue_color, heel_color, pattern, custom_text, custom_text_color, preview_image, calculated_price, specs_json)
- `carts` & `cart_items` (id, cart_id, product_id, custom_design_id, size, quantity, unit_price, custom_data_json)
- `orders` & `order_items` (id, order_number, user_id, total_amount, discount_amount, coupon_code, shipping_fee, tax_amount, final_amount, status, payment_method, payment_status, tracking_number)
- `payments` (id, order_id, transaction_id, payment_method, amount, status, gateway_response)
- `reviews` (id, product_id, user_id, rating, title, comment, verified_purchase)
- `coupons` (id, code, discount_percent, discount_amount, min_order_value, max_discount, valid_to, is_active, usage_count)
- `wishlists` (id, user_id, product_id)

---

## 📄 License
Crafted with precision for **SOLECRAFT Atelier Inc.** &copy; 2026. All rights reserved.
