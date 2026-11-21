import os

products_dir = os.path.join(os.path.dirname(__file__), 'app', 'static', 'images', 'products')
branding_dir = os.path.join(os.path.dirname(__file__), 'app', 'static', 'images', 'branding')
os.makedirs(products_dir, exist_ok=True)
os.makedirs(branding_dir, exist_ok=True)

# Logo SVG
logo_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 60" width="320" height="60">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF6B35" />
      <stop offset="100%" stop-color="#FF8C5A" />
    </linearGradient>
  </defs>
  <!-- Geometric Sole icon -->
  <g transform="translate(10, 10)">
    <rect x="0" y="8" width="36" height="24" rx="12" fill="#111111" />
    <path d="M 6 20 C 14 12, 22 28, 30 20" stroke="url(#logoGrad)" stroke-width="3" stroke-linecap="round" fill="none" />
    <circle cx="30" cy="20" r="3" fill="#FF6B35" />
  </g>
  <!-- Text -->
  <text x="58" y="32" font-family="'Inter', 'Montserrat', -apple-system, sans-serif" font-weight="900" font-size="22" letter-spacing="3" fill="#111111">
    SOLE<tspan fill="#FF6B35">CRAFT</tspan>
  </text>
  <text x="60" y="45" font-family="'Inter', -apple-system, sans-serif" font-weight="600" font-size="7.5" letter-spacing="2.5" fill="#888888">
    STUDIO LAB • EST 2026
  </text>
</svg>"""

with open(os.path.join(branding_dir, 'logo.svg'), 'w', encoding='utf-8') as f:
    f.write(logo_svg)

# Favicon SVG
favicon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="16" fill="#111111"/>
  <path d="M 12 36 C 24 20, 40 44, 52 30" stroke="#FF6B35" stroke-width="6" stroke-linecap="round" fill="none" />
  <circle cx="52" cy="30" r="4.5" fill="#FF6B35" />
</svg>"""

with open(os.path.join(branding_dir, 'favicon.svg'), 'w', encoding='utf-8') as f:
    f.write(favicon_svg)

def build_sneaker_svg(name, base_color="#FFFFFF", upper_color="#111111", accent_color="#FF6B35", sole_color="#FFFFFF", style="low"):
    if style == "high":
        # High Top Silhouette
        upper_path = "M 90 280 L 110 150 C 120 120, 160 110, 190 120 L 250 140 C 270 170, 310 210, 360 230 L 440 240 C 470 250, 490 270, 500 290 L 90 290 Z"
        collar_path = "M 110 150 C 130 110, 190 100, 240 120 L 230 170 C 180 150, 130 160, 110 150 Z"
        sole_path = "M 80 290 L 510 290 C 515 315, 490 330, 440 330 L 100 330 C 80 330, 75 310, 80 290 Z"
        swoosh_path = "M 160 210 Q 280 180, 380 255 Q 310 250, 210 260 Z"
        lace_x = [230, 250, 275, 305, 335]
        lace_y = [150, 175, 200, 220, 240]
    elif style == "runner":
        # Aerodynamic curved runner
        upper_path = "M 100 270 C 130 200, 190 190, 250 190 L 340 205 C 410 220, 460 240, 505 270 L 100 270 Z"
        collar_path = "M 170 195 C 190 170, 240 170, 260 190 Z"
        sole_path = "M 70 270 C 90 270, 140 270, 200 275 C 320 285, 430 290, 520 265 C 525 295, 480 335, 430 335 L 120 335 C 80 335, 60 305, 70 270 Z"
        swoosh_path = "M 180 230 Q 300 205, 410 250 Q 320 245, 220 255 Z"
        lace_x = [240, 270, 300, 330]
        lace_y = [200, 215, 230, 245]
    elif style == "formal":
        # Classic Derby / Oxford
        upper_path = "M 90 275 C 110 210, 170 210, 230 210 L 340 225 C 420 240, 470 255, 510 275 L 90 275 Z"
        collar_path = "M 160 210 C 190 195, 230 195, 250 210 Z"
        sole_path = "M 80 275 L 515 275 L 505 310 L 400 310 L 390 295 L 190 295 L 180 325 L 85 325 Z"
        swoosh_path = "M 150 260 C 260 250, 360 255, 420 270"
        lace_x = [220, 245, 270, 295]
        lace_y = [215, 225, 235, 245]
    elif style == "slipon":
        # Sleek Slip-on
        upper_path = "M 100 275 C 120 200, 180 185, 250 195 C 330 205, 420 230, 500 275 L 100 275 Z"
        collar_path = "M 180 195 C 210 180, 260 180, 280 200 Z"
        sole_path = "M 90 275 L 510 275 C 510 305, 475 325, 430 325 L 110 325 C 90 325, 85 305, 90 275 Z"
        swoosh_path = "M 200 235 Q 320 225, 430 265"
        lace_x = []
        lace_y = []
    else:
        # Classic Low-top Sneaker
        upper_path = "M 95 275 C 110 190, 175 170, 240 180 L 330 195 C 400 215, 460 240, 505 275 L 95 275 Z"
        collar_path = "M 140 180 C 170 155, 225 155, 250 180 Z"
        sole_path = "M 80 275 L 515 275 C 518 305, 480 330, 440 330 L 100 330 C 80 330, 75 305, 80 275 Z"
        swoosh_path = "M 170 225 Q 300 190, 420 250 Q 330 245, 220 255 Z"
        lace_x = [230, 260, 290, 320, 350]
        lace_y = [185, 200, 215, 230, 245]

    laces_markup = ""
    for x, y in zip(lace_x, lace_y):
        laces_markup += f'<line x1="{x}" y1="{y}" x2="{x+18}" y2="{y+8}" stroke="{accent_color}" stroke-width="4.5" stroke-linecap="round" filter="url(#dropShadow)" />\n'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="100%" height="100%">
  <defs>
    <filter id="dropShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="#000000" flood-opacity="0.14" />
    </filter>
    <filter id="softShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.18" />
    </filter>
    <linearGradient id="soleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{sole_color}" />
      <stop offset="100%" stop-color="#E0E0DC" />
    </linearGradient>
    <linearGradient id="bgGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAFAF9" />
      <stop offset="100%" stop-color="#EFEFEA" />
    </linearGradient>
  </defs>

  <!-- Clean Canvas Background -->
  <rect width="600" height="400" rx="16" fill="url(#bgGlow)"/>

  <!-- Floor Contact Shadow -->
  <ellipse cx="300" cy="340" rx="220" ry="20" fill="#111111" opacity="0.12" filter="blur(8px)" />

  <!-- Shoe Group with shadow -->
  <g filter="url(#dropShadow)">
    <!-- Sole / Outsole & Midsole -->
    <path d="{sole_path}" fill="url(#soleGrad)" stroke="#D4D4CF" stroke-width="1.5" />
    <!-- Tread grooves -->
    <line x1="120" y1="322" x2="470" y2="322" stroke="#B8B8B0" stroke-width="2" stroke-dasharray="12 8" opacity="0.6" />

    <!-- Main Upper -->
    <path d="{upper_path}" fill="{base_color}" stroke="#CCCCCC" stroke-width="1" />

    <!-- Overlay Quarter / Heel Counter -->
    <path d="M 95 275 C 90 220, 130 180, 180 180 L 195 275 Z" fill="{upper_color}" opacity="0.9" />

    <!-- Collar / Lining -->
    <path d="{collar_path}" fill="#222222" />

    <!-- Signature Brand Swoosh / Vector Wave -->
    <path d="{swoosh_path}" fill="{accent_color}" filter="url(#softShadow)" />

    <!-- Heel Tab / Pull Accent -->
    <rect x="85" y="210" width="12" height="40" rx="6" fill="{accent_color}" />

    <!-- Eyestay & Laces -->
    {laces_markup}

    <!-- Contrast Stitching Details -->
    <path d="M 120 270 C 130 200, 180 190, 240 195" fill="none" stroke="{accent_color}" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.75" />
    <path d="M 330 205 C 390 220, 440 245, 480 270" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.5" />

    <!-- Monogram Badge -->
    <g transform="translate(130, 245)">
      <circle cx="12" cy="12" r="10" fill="#111111" opacity="0.8" />
      <text x="12" y="16" font-family="'Inter', sans-serif" font-size="8" font-weight="900" fill="#FFFFFF" text-anchor="middle">SC</text>
    </g>
  </g>
</svg>"""
    return svg

products = [
    ("retro-low-white.svg", "#FFFFFF", "#2B2D42", "#FF6B35", "#FFFFFF", "low"),
    ("apex-high-black.svg", "#111111", "#1E1E24", "#FF6B35", "#222222", "high"),
    ("aero-runner-orange.svg", "#FFFFFF", "#1E2022", "#FF6B35", "#F2F2F2", "runner"),
    ("veloce-sprinter.svg", "#1B1B1B", "#2D3142", "#E63946", "#FFFFFF", "runner"),
    ("milano-slipon.svg", "#D4C5B9", "#9C8A79", "#2B2D42", "#FFFFFF", "slipon"),
    ("soho-court.svg", "#F8F9FA", "#E9ECEF", "#111111", "#FFFFFF", "low"),
    ("courtforce-slam.svg", "#14213D", "#000000", "#FF6B35", "#E5E5E5", "high"),
    ("kallisto-derby.svg", "#1A1A1A", "#262626", "#8B0000", "#111111", "formal"),
    ("oxford-monolith.svg", "#2B1B17", "#3D2B1F", "#D4AF37", "#1E1E1E", "formal"),
    ("aura-platform.svg", "#FFF9F5", "#F8EDEB", "#FFB5A7", "#FFFFFF", "low"),
    ("serena-knit.svg", "#E8E8E4", "#D8E2DC", "#FFCAD4", "#FFFFFF", "runner"),
    ("chronos-vanguard.svg", "#4A3B32", "#362B24", "#FF6B35", "#222222", "formal"),
    ("monolith-zero.svg", "#EDE8F5", "#3D3A45", "#70A9A1", "#F4F1DE", "low"),
    ("custom-default.svg", "#FFFFFF", "#111111", "#FF6B35", "#FFFFFF", "low")
]

for filename, base_c, up_c, acc_c, sole_c, style in products:
    content = build_sneaker_svg(filename, base_c, up_c, acc_c, sole_c, style)
    with open(os.path.join(products_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Generated {len(products)} product graphics and branding SVGs.")
