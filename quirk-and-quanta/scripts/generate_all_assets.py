#!/usr/bin/env python3
"""
Generate all visual assets for Quirk & Quanta storefront:
1. site/assets/logo.svg (Storefront Logo & Wordmark)
2. site/assets/hero/hero-banner.svg (Hero Banner Illustration)
3. site/assets/products/QQ-XXXX.svg (100 distinct primary product SVGs)
4. site/assets/products/QQ-XXXX-thumb.svg (100 distinct thumbnail SVGs)
"""

import os
import json
import math
import html

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "site", "assets")
PRODUCTS_DIR = os.path.join(ASSETS_DIR, "products")
HERO_DIR = os.path.join(ASSETS_DIR, "hero")

os.makedirs(PRODUCTS_DIR, exist_ok=True)
os.makedirs(HERO_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. STOREFRONT LOGO
# -------------------------------------------------------------
def generate_logo():
    logo_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 120" width="520" height="120">
  <defs>
    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#158D89" />
      <stop offset="100%" stop-color="#F4C95D" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Left Monogram Icon -->
  <g transform="translate(10, 10)">
    <!-- Outer Glow Orbit -->
    <ellipse cx="50" cy="50" rx="46" ry="18" fill="none" stroke="#158D89" stroke-width="2.5" transform="rotate(-30, 50, 50)" opacity="0.85" />
    <ellipse cx="50" cy="50" rx="46" ry="18" fill="none" stroke="#F4C95D" stroke-width="2.5" transform="rotate(30, 50, 50)" opacity="0.85" />
    <ellipse cx="50" cy="50" rx="46" ry="18" fill="none" stroke="#18243A" stroke-width="2" transform="rotate(90, 50, 50)" opacity="0.4" />

    <!-- Central Nucleus Badge -->
    <circle cx="50" cy="50" r="28" fill="#18243A" />
    
    <!-- Stylized Q & Q Monogram -->
    <text x="42" y="58" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="900" fill="#FFFFFF" text-anchor="middle">Q</text>
    <text x="50" y="52" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#F4C95D" text-anchor="middle">&amp;</text>
    <text x="58" y="58" font-family="system-ui, -apple-system, sans-serif" font-size="24" font-weight="900" fill="#158D89" text-anchor="middle">Q</text>
    
    <!-- Quantum electron particles -->
    <circle cx="15" cy="30" r="4.5" fill="#158D89" />
    <circle cx="85" cy="70" r="4.5" fill="#F4C95D" />
    <circle cx="50" cy="96" r="3.5" fill="#18243A" />
  </g>

  <!-- Brand Typography -->
  <g transform="translate(130, 25)">
    <!-- Main Brand Name -->
    <text x="0" y="42" font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="38" font-weight="900" letter-spacing="1.5" fill="#18243A">
      QUIRK <tspan fill="#158D89">&amp;</tspan> QUANTA
    </text>
    
    <!-- Tagline -->
    <text x="2" y="66" font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="600" letter-spacing="2.2" fill="#5A6578">
      PRECISELY UNNECESSARY. SCIENTIFICALLY DELIGHTFUL.
    </text>
    
    <!-- Small sub-badge -->
    <rect x="0" y="74" width="220" height="2" fill="url(#logoGrad)" rx="1" />
  </g>
</svg>"""

    with open(os.path.join(ASSETS_DIR, "logo.svg"), "w", encoding="utf-8") as f:
        f.write(logo_svg)
    print("Generated site/assets/logo.svg")

# -------------------------------------------------------------
# 2. HERO BANNER
# -------------------------------------------------------------
def generate_hero():
    hero_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 500" width="1200" height="500">
  <defs>
    <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#18243A" />
      <stop offset="60%" stop-color="#141E30" />
      <stop offset="100%" stop-color="#0F1724" />
    </linearGradient>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#158D89" />
      <stop offset="100%" stop-color="#2CD4CD" />
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F4C95D" />
      <stop offset="100%" stop-color="#E29F25" />
    </linearGradient>
    <pattern id="gridPattern" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#253550" stroke-width="0.8" opacity="0.6" />
      <circle cx="0" cy="0" r="1.5" fill="#158D89" opacity="0.5" />
    </pattern>
  </defs>

  <!-- Deep Navy Background with Grid Matrix -->
  <rect width="1200" height="500" fill="url(#heroBg)" />
  <rect width="1200" height="500" fill="url(#gridPattern)" />

  <!-- Left Content Column Background Glow -->
  <circle cx="200" cy="250" r="280" fill="#158D89" opacity="0.08" filter="blur(60px)" />
  <circle cx="950" cy="250" r="320" fill="#F4C95D" opacity="0.06" filter="blur(70px)" />

  <!-- Scientific Vector Background Illustrations (Right Hemisphere) -->
  <g transform="translate(680, 50)" opacity="0.95">
    <!-- Huge Keplerian Orbit Geometry -->
    <ellipse cx="260" cy="200" rx="220" ry="80" fill="none" stroke="#158D89" stroke-width="1.8" stroke-dasharray="6,4" transform="rotate(-25, 260, 200)" />
    <ellipse cx="260" cy="200" rx="180" ry="140" fill="none" stroke="#F4C95D" stroke-width="1.5" opacity="0.6" transform="rotate(40, 260, 200)" />
    <circle cx="260" cy="200" r="90" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.2" />

    <!-- Central Glowing Core -->
    <circle cx="260" cy="200" r="38" fill="url(#goldGrad)" opacity="0.9" />
    <circle cx="260" cy="200" r="48" fill="none" stroke="#F4C95D" stroke-width="2" opacity="0.4" />

    <!-- Blackboard Style Math Annotations -->
    <text x="320" y="110" font-family="'Courier New', monospace" font-size="14" fill="#2CD4CD" opacity="0.85">i&#8463; &#8706;&#968;/&#8706;t = &#292;&#968;</text>
    <text x="120" y="320" font-family="'Courier New', monospace" font-size="13" fill="#F4C95D" opacity="0.85">&#8711; &#215; B = &#956;&#8320;J + &#956;&#8320;&#949;&#8320;&#8706;E/&#8706;t</text>
    <text x="360" y="270" font-family="'Courier New', monospace" font-size="14" fill="#FFFFFF" opacity="0.75">R_&#956;&#957; - &#189;Rg_&#956;&#957; = 8&#960;GT_&#956;&#957;</text>

    <!-- Hanging Atomic Lamp Silhouette -->
    <g transform="translate(140, 40)">
      <line x1="80" y1="0" x2="80" y2="70" stroke="#718096" stroke-width="3" />
      <circle cx="80" cy="100" r="30" fill="none" stroke="#F4C95D" stroke-width="3" />
      <circle cx="80" cy="100" r="16" fill="url(#goldGrad)" />
      <ellipse cx="80" cy="100" rx="38" ry="12" fill="none" stroke="#158D89" stroke-width="2" transform="rotate(-30, 80, 100)" />
      <ellipse cx="80" cy="100" rx="38" ry="12" fill="none" stroke="#158D89" stroke-width="2" transform="rotate(30, 80, 100)" />
    </g>

    <!-- Miniature Steam Locomotive Silhouette -->
    <g transform="translate(220, 310)">
      <rect x="0" y="30" width="160" height="50" rx="8" fill="#1F2E47" stroke="#158D89" stroke-width="2" />
      <rect x="110" y="10" width="45" height="70" rx="4" fill="#18243A" stroke="#F4C95D" stroke-width="2" />
      <rect x="25" y="10" width="16" height="25" fill="#158D89" />
      <!-- Wheels -->
      <circle cx="25" cy="85" r="16" fill="#18243A" stroke="#F4C95D" stroke-width="3" />
      <circle cx="65" cy="85" r="16" fill="#18243A" stroke="#F4C95D" stroke-width="3" />
      <circle cx="105" cy="85" r="16" fill="#18243A" stroke="#F4C95D" stroke-width="3" />
      <line x1="25" y1="85" x2="105" y2="85" stroke="#F4C95D" stroke-width="3" />
      <!-- Track -->
      <line x1="-30" y1="102" x2="190" y2="102" stroke="#4A5568" stroke-width="4" />
    </g>

    <!-- Floating Icosahedron Polyhedron -->
    <g transform="translate(420, 60)">
      <polygon points="50,10 90,35 90,80 50,105 10,80 10,35" fill="none" stroke="#2CD4CD" stroke-width="2" />
      <polygon points="50,10 50,105" fill="none" stroke="#2CD4CD" stroke-width="1.2" stroke-dasharray="3,3" />
      <polygon points="10,35 90,35" fill="none" stroke="#2CD4CD" stroke-width="1.2" />
      <polygon points="10,80 90,80" fill="none" stroke="#2CD4CD" stroke-width="1.2" />
      <circle cx="50" cy="10" r="3" fill="#F4C95D" />
      <circle cx="90" cy="35" r="3" fill="#F4C95D" />
      <circle cx="90" cy="80" r="3" fill="#F4C95D" />
      <circle cx="50" cy="105" r="3" fill="#F4C95D" />
      <circle cx="10" cy="80" r="3" fill="#F4C95D" />
      <circle cx="10" cy="35" r="3" fill="#F4C95D" />
    </g>
  </g>

  <!-- Left Hero Copy Content -->
  <g transform="translate(80, 110)">
    <!-- Subtitle Pill -->
    <g>
      <rect x="0" y="0" width="295" height="34" rx="17" fill="#1F2F4A" stroke="#158D89" stroke-width="1.5" />
      <circle cx="18" cy="17" r="5" fill="#F4C95D" />
      <text x="32" y="22" font-family="system-ui, sans-serif" font-size="12" font-weight="700" letter-spacing="1" fill="#E2E8F0">
        THEORETICAL APPAREL &amp; APPARATUS
      </text>
    </g>

    <!-- Main Headline -->
    <text x="0" y="90" font-family="system-ui, -apple-system, sans-serif" font-size="46" font-weight="900" line-height="1.15" fill="#FFFFFF">
      Because Your Desk Deserves
    </text>
    <text x="0" y="145" font-family="system-ui, -apple-system, sans-serif" font-size="46" font-weight="900" fill="url(#tealGrad)">
      A Peer-Reviewed Upgrade.
    </text>

    <!-- Paragraph Description -->
    <text x="0" y="195" font-family="system-ui, sans-serif" font-size="17" font-weight="400" fill="#A0AEC0">
      Discover 100 precisely engineered gadgets, apparel, stationery,
    </text>
    <text x="0" y="222" font-family="system-ui, sans-serif" font-size="17" font-weight="400" fill="#A0AEC0">
      and glorious scientific absurdities for the unapologetic intellect.
    </text>

    <!-- Feature Value Badges -->
    <g transform="translate(0, 260)">
      <g transform="translate(0, 0)">
        <circle cx="10" cy="10" r="7" fill="#158D89" />
        <path d="M 7 10 L 9 12 L 13 8" fill="none" stroke="#FFFFFF" stroke-width="1.8" />
        <text x="25" y="14" font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="#CBD5E0">100 Unique Products</text>
      </g>
      <g transform="translate(190, 0)">
        <circle cx="10" cy="10" r="7" fill="#158D89" />
        <path d="M 7 10 L 9 12 L 13 8" fill="none" stroke="#FFFFFF" stroke-width="1.8" />
        <text x="25" y="14" font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="#CBD5E0">Calculated Margins</text>
      </g>
      <g transform="translate(370, 0)">
        <circle cx="10" cy="10" r="7" fill="#158D89" />
        <path d="M 7 10 L 9 12 L 13 8" fill="none" stroke="#FFFFFF" stroke-width="1.8" />
        <text x="25" y="14" font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="#CBD5E0">RAG &amp; Graph Ready</text>
      </g>
    </g>
  </g>
</svg>"""

    with open(os.path.join(HERO_DIR, "hero-banner.svg"), "w", encoding="utf-8") as f:
        f.write(hero_svg)
    print("Generated site/assets/hero/hero-banner.svg")

# -------------------------------------------------------------
# 3. 100 DISTINCT PRODUCT SVGs GENERATOR
# -------------------------------------------------------------

# Load canonical products to obtain exact metadata
with open(os.path.join(BASE_DIR, "data", "internal", "products.full.json"), "r", encoding="utf-8") as f:
    CANONICAL_PRODUCTS = json.load(f)

# Category color accents
CATEGORY_THEMES = {
    "CAT-APPAREL": {"bg": "#EDF2F7", "accent": "#18243A", "highlight": "#158D89", "tag": "Apparel"},
    "CAT-DESK": {"bg": "#F0F4F8", "accent": "#2B4C7E", "highlight": "#F4C95D", "tag": "Desk &amp; Office"},
    "CAT-KITCHEN": {"bg": "#F7FAFC", "accent": "#2C7A7B", "highlight": "#DD6B20", "tag": "Drinkware &amp; Kitchen"},
    "CAT-HOME": {"bg": "#FAF5FF", "accent": "#44337A", "highlight": "#9F7AEA", "tag": "Home &amp; Decor"},
    "CAT-GADGETS": {"bg": "#E6FFFA", "accent": "#234E52", "highlight": "#319795", "tag": "Science Gadgets"},
    "CAT-PUZZLES": {"bg": "#FFFAF0", "accent": "#7B341E", "highlight": "#DD6B20", "tag": "Puzzles &amp; Games"},
    "CAT-STATIONERY": {"bg": "#F7FAFC", "accent": "#1A365D", "highlight": "#3182CE", "tag": "Stationery &amp; Learning"},
    "CAT-TECH": {"bg": "#EBF8FF", "accent": "#1A202C", "highlight": "#00B4D8", "tag": "Tech Accessories"},
    "CAT-RAILWAY": {"bg": "#F0FFF4", "accent": "#1C4532", "highlight": "#D69E2E", "tag": "Railway &amp; Engineering"},
    "CAT-GIFTS": {"bg": "#FFF5F5", "accent": "#742A2A", "highlight": "#D69E2E", "tag": "Gifts &amp; Collectibles"}
}

def get_product_drawing(sku):
    """
    Returns specific SVG markup for each of the 100 products.
    """
    # Category A: Apparel (QQ-0001 to QQ-0010)
    if sku == "QQ-0001":  # Quantum Uncertainty Hoodie
        return """
        <!-- Hoodie Body -->
        <path d="M 120 180 L 170 120 L 230 120 L 280 180 L 250 200 L 230 180 L 230 330 L 170 330 L 170 180 L 150 200 Z" fill="#18243A" />
        <!-- Hood -->
        <path d="M 170 120 Q 200 60 230 120 Q 200 140 170 120 Z" fill="#243452" stroke="#158D89" stroke-width="2" />
        <!-- Drawstrings with aglets -->
        <path d="M 185 135 Q 185 180 180 210" fill="none" stroke="#FFFFFF" stroke-width="2.5" />
        <rect x="177" y="210" width="6" height="14" fill="#F4C95D" rx="2" />
        <path d="M 215 135 Q 215 180 220 210" fill="none" stroke="#FFFFFF" stroke-width="2.5" />
        <rect x="217" y="210" width="6" height="14" fill="#F4C95D" rx="2" />
        <!-- Kangaroo pocket -->
        <path d="M 180 250 L 220 250 L 230 300 L 170 300 Z" fill="#131D2E" stroke="#158D89" stroke-width="1.5" />
        <!-- Wave equation print on sleeve -->
        <path d="M 130 190 Q 140 220 150 210 T 170 230" fill="none" stroke="#2CD4CD" stroke-width="2" />
        <text x="200" y="275" font-family="'Courier New', monospace" font-size="10" fill="#2CD4CD" text-anchor="middle">&#916;x &#8226; &#916;p &#8805; &#8463;/2</text>
        """
    elif sku == "QQ-0002":  # Periodic Element Pajama Set
        return """
        <!-- Pajama Top -->
        <path d="M 130 140 L 180 110 L 220 110 L 270 140 L 250 170 L 220 150 L 220 250 L 180 250 L 180 150 L 150 170 Z" fill="#2D3748" />
        <!-- Camp collar -->
        <polygon points="180,110 200,140 220,110 200,125" fill="#4A5568" stroke="#F4C95D" stroke-width="1.5" />
        <!-- Buttons -->
        <circle cx="200" cy="160" r="3" fill="#E2E8F0" />
        <circle cx="200" cy="190" r="3" fill="#E2E8F0" />
        <circle cx="200" cy="220" r="3" fill="#E2E8F0" />
        <!-- Periodic Element Tiles printed on shirt -->
        <rect x="185" y="165" width="12" height="12" fill="#1A202C" stroke="#2CD4CD" stroke-width="1" />
        <text x="191" y="174" font-family="sans-serif" font-size="7" fill="#FFFFFF" text-anchor="middle">H</text>
        <rect x="205" y="165" width="12" height="12" fill="#1A202C" stroke="#F4C95D" stroke-width="1" />
        <text x="211" y="174" font-family="sans-serif" font-size="7" fill="#FFFFFF" text-anchor="middle">He</text>
        <!-- Pajama Bottoms -->
        <path d="M 180 260 L 220 260 L 225 350 L 205 350 L 200 290 L 195 350 L 175 350 Z" fill="#2D3748" />
        <line x1="180" y1="260" x2="220" y2="260" stroke="#F4C95D" stroke-width="3" />
        """
    elif sku == "QQ-0003":  # Schrödinger's Laundry T-Shirt
        return """
        <!-- T-Shirt Body -->
        <path d="M 125 150 L 175 115 L 225 115 L 275 150 L 255 180 L 230 165 L 230 330 L 170 330 L 170 165 L 145 180 Z" fill="#718096" />
        <!-- Crew Neck -->
        <path d="M 175 115 Q 200 135 225 115" fill="none" stroke="#4A5568" stroke-width="3" />
        <!-- Box Illustration on Chest -->
        <rect x="175" y="180" width="50" height="42" fill="#2D3748" stroke="#F4C95D" stroke-width="2" rx="4" />
        <!-- Cat Silhouette Ears peeking out -->
        <polygon points="185,180 190,168 198,180" fill="#1A202C" />
        <polygon points="202,180 210,168 215,180" fill="#1A202C" />
        <text x="200" y="205" font-family="'Courier New', monospace" font-size="11" fill="#2CD4CD" text-anchor="middle">|&#968;&#9002; = ?</text>
        <text x="200" y="250" font-family="sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">CLEAN &#8853; DIRTY</text>
        """
    elif sku == "QQ-0004":  # Cosmic Equation Socks
        return """
        <!-- Sock Pair -->
        <g transform="translate(130, 110)">
          <!-- Left Sock -->
          <path d="M 30 20 L 65 20 L 65 140 L 95 180 L 75 200 L 30 155 Z" fill="#18243A" stroke="#158D89" stroke-width="2" />
          <rect x="30" y="20" width="35" height="15" fill="#F4C95D" />
          <text x="48" y="75" font-family="monospace" font-size="7" fill="#2CD4CD" transform="rotate(-90, 48, 75)">G&#956;&#957;=8&#960;T&#956;&#957;</text>
          <!-- Right Sock -->
          <path d="M 90 40 L 125 40 L 125 160 L 155 200 L 135 220 L 90 175 Z" fill="#1A202C" stroke="#F4C95D" stroke-width="2" />
          <rect x="90" y="40" width="35" height="15" fill="#158D89" />
          <text x="108" y="95" font-family="monospace" font-size="7" fill="#F4C95D" transform="rotate(-90, 108, 95)">E=mc&#178;</text>
        </g>
        """
    elif sku == "QQ-0005":  # Theoretical Genius Lab Coat
        return """
        <!-- Coat Body -->
        <path d="M 120 160 L 175 110 L 225 110 L 280 160 L 260 190 L 235 170 L 245 350 L 155 350 L 165 170 L 140 190 Z" fill="#F7FAFC" stroke="#CBD5E0" stroke-width="2" />
        <!-- Lapels -->
        <polygon points="175,110 195,160 200,160 185,110" fill="#EDF2F7" stroke="#A0AEC0" />
        <polygon points="225,110 205,160 200,160 215,110" fill="#EDF2F7" stroke="#A0AEC0" />
        <!-- Snap closures -->
        <circle cx="200" cy="180" r="3" fill="#718096" />
        <circle cx="200" cy="220" r="3" fill="#718096" />
        <circle cx="200" cy="260" r="3" fill="#718096" />
        <circle cx="200" cy="300" r="3" fill="#718096" />
        <!-- Pockets -->
        <rect x="165" y="240" width="28" height="34" fill="#EDF2F7" stroke="#A0AEC0" stroke-width="1.5" rx="2" />
        <rect x="207" y="240" width="28" height="34" fill="#EDF2F7" stroke="#A0AEC0" stroke-width="1.5" rx="2" />
        <!-- Caliper peeking from pocket -->
        <line x1="172" y1="225" x2="172" y2="245" stroke="#F4C95D" stroke-width="2" />
        <line x1="176" y1="225" x2="176" y2="245" stroke="#718096" stroke-width="2" />
        """
    elif sku == "QQ-0006":  # Gravity-Defying Beanie
        return """
        <g transform="translate(130, 140)">
          <!-- Beanie Dome -->
          <path d="M 10 90 Q 70 0 130 90 Z" fill="#2D3748" stroke="#158D89" stroke-width="2" />
          <!-- Vertical Rib lines -->
          <path d="M 35 90 Q 70 20 105 90" fill="none" stroke="#4A5568" stroke-width="1.5" />
          <path d="M 50 90 Q 70 30 90 90" fill="none" stroke="#4A5568" stroke-width="1.5" />
          <!-- Folded Cuff -->
          <rect x="5" y="85" width="130" height="38" rx="6" fill="#1A202C" stroke="#718096" stroke-width="1.5" />
          <!-- Embroidered Subatomic Emblem -->
          <circle cx="70" cy="104" r="10" fill="#158D89" />
          <ellipse cx="70" cy="104" rx="14" ry="5" fill="none" stroke="#F4C95D" stroke-width="1.2" transform="rotate(-30, 70, 104)" />
        </g>
        """
    elif sku == "QQ-0007":  # Mathematical Constants Sweatshirt
        return """
        <!-- Sweatshirt Body -->
        <path d="M 120 170 L 170 120 L 230 120 L 280 170 L 255 195 L 235 175 L 235 330 L 165 330 L 165 175 L 145 195 Z" fill="#E2E8F0" stroke="#A0AEC0" stroke-width="2" />
        <!-- V-notch collar -->
        <polygon points="190,120 200,140 210,120" fill="#CBD5E0" stroke="#A0AEC0" />
        <!-- Printed Constants on Chest -->
        <g transform="translate(175, 175)">
          <text x="25" y="20" font-family="serif" font-size="22" font-weight="bold" fill="#18243A" text-anchor="middle">&#960;</text>
          <text x="25" y="45" font-family="serif" font-size="16" font-style="italic" fill="#158D89" text-anchor="middle">e = 2.71828...</text>
          <text x="25" y="65" font-family="serif" font-size="16" fill="#D69E2E" text-anchor="middle">&#981; = 1.618...</text>
          <text x="25" y="85" font-family="monospace" font-size="12" fill="#718096" text-anchor="middle">&#8463; = 6.626&#215;10&#8315;&#179;&#8308;</text>
        </g>
        """
    elif sku == "QQ-0008":  # Orbital Mechanics Sneakers
        return """
        <g transform="translate(100, 160)">
          <!-- Outsole -->
          <path d="M 10 120 Q 90 135 180 125 Q 195 105 180 95 L 30 95 Q 10 105 10 120 Z" fill="#FFFFFF" stroke="#CBD5E0" stroke-width="2" />
          <!-- Midsole Cushion Nitrogen line -->
          <path d="M 15 108 Q 90 120 175 110" fill="none" stroke="#00B4D8" stroke-width="4" />
          <!-- Shoe Upper -->
          <path d="M 30 95 L 70 45 L 120 55 L 140 70 L 180 95 Z" fill="#4A5568" />
          <!-- Orbital Lines on Side -->
          <ellipse cx="100" cy="80" rx="45" ry="15" fill="none" stroke="#2CD4CD" stroke-width="2" transform="rotate(-15, 100, 80)" />
          <ellipse cx="100" cy="80" rx="35" ry="10" fill="none" stroke="#F4C95D" stroke-width="1.5" transform="rotate(20, 100, 80)" />
          <!-- Laces -->
          <line x1="80" y1="52" x2="95" y2="60" stroke="#FFFFFF" stroke-width="2" />
          <line x1="85" y1="62" x2="100" y2="70" stroke="#FFFFFF" stroke-width="2" />
        </g>
        """
    elif sku == "QQ-0009":  # Nerd Protocol Baseball Cap
        return """
        <g transform="translate(110, 160)">
          <!-- Crown -->
          <path d="M 40 90 Q 90 10 150 90 Z" fill="#18243A" stroke="#2B4C7E" stroke-width="2" />
          <!-- Curved Visor -->
          <path d="M 130 90 Q 180 95 200 115 Q 150 115 115 90 Z" fill="#131D2E" stroke="#158D89" stroke-width="1.5" />
          <!-- Eyelets -->
          <circle cx="70" cy="60" r="2.5" fill="#A0AEC0" />
          <circle cx="100" cy="50" r="2.5" fill="#A0AEC0" />
          <circle cx="130" cy="65" r="2.5" fill="#A0AEC0" />
          <!-- Protocol Checklist Badge -->
          <rect x="75" y="60" width="30" height="26" fill="#1F2F4A" stroke="#F4C95D" stroke-width="1.5" rx="3" />
          <path d="M 80 73 L 85 78 L 95 68" fill="none" stroke="#2CD4CD" stroke-width="2" />
          <!-- Button on top -->
          <circle cx="95" cy="28" r="4" fill="#F4C95D" />
        </g>
        """
    elif sku == "QQ-0010":  # Doppler Effect Graphic Jacket
        return """
        <!-- Coach Jacket Body -->
        <path d="M 120 170 L 175 120 L 225 120 L 280 170 L 260 200 L 235 180 L 235 340 L 165 340 L 165 180 L 140 200 Z" fill="#1A202C" />
        <!-- Compressed Blue Waves on Left Chest (Blueshift) -->
        <path d="M 175 160 Q 185 180 175 200" fill="none" stroke="#00B4D8" stroke-width="3" />
        <path d="M 180 160 Q 190 180 180 200" fill="none" stroke="#00B4D8" stroke-width="3" />
        <path d="M 185 160 Q 195 180 185 200" fill="none" stroke="#00B4D8" stroke-width="3" />
        <path d="M 190 160 Q 200 180 190 200" fill="none" stroke="#00B4D8" stroke-width="3" />
        <!-- Stretched Red Waves on Right Chest (Redshift) -->
        <path d="M 205 160 Q 225 180 205 200" fill="none" stroke="#E53E3E" stroke-width="3" />
        <path d="M 220 160 Q 240 180 220 200" fill="none" stroke="#E53E3E" stroke-width="3" />
        <!-- Central zipper placket -->
        <line x1="200" y1="120" x2="200" y2="340" stroke="#718096" stroke-width="2" />
        """

    # Category B: Desk & Office (QQ-0011 to QQ-0020)
    elif sku == "QQ-0011":  # Atomic Orbit Desk Lamp
        return """
        <g transform="translate(130, 80)">
          <!-- Base -->
          <ellipse cx="70" cy="270" rx="55" ry="16" fill="#18243A" stroke="#CBD5E0" stroke-width="2" />
          <!-- Lamp Post -->
          <path d="M 70 270 L 70 120 Q 70 70 110 70" fill="none" stroke="#718096" stroke-width="6" />
          <!-- Nucleus Light Bulb -->
          <circle cx="110" cy="110" r="22" fill="#F4C95D" opacity="0.9" />
          <circle cx="110" cy="110" r="30" fill="none" stroke="#F4C95D" stroke-width="1.5" opacity="0.5" />
          <!-- Orbit Rings -->
          <ellipse cx="110" cy="110" rx="60" ry="22" fill="none" stroke="#158D89" stroke-width="2.5" transform="rotate(-35, 110, 110)" />
          <ellipse cx="110" cy="110" rx="60" ry="22" fill="none" stroke="#2B4C7E" stroke-width="2.5" transform="rotate(35, 110, 110)" />
          <ellipse cx="110" cy="110" rx="60" ry="22" fill="none" stroke="#F4C95D" stroke-width="2" transform="rotate(85, 110, 110)" />
          <!-- Orbit Electrons -->
          <circle cx="65" cy="75" r="4.5" fill="#158D89" />
          <circle cx="155" cy="145" r="4.5" fill="#F4C95D" />
        </g>
        """
    elif sku == "QQ-0012":  # Precision Workspace Organizer
        return """
        <g transform="translate(100, 150)">
          <!-- Milled Aluminum Block -->
          <polygon points="20,80 180,80 200,40 40,40" fill="#718096" stroke="#4A5568" />
          <rect x="20" y="80" width="160" height="70" fill="#4A5568" stroke="#2D3748" />
          <polygon points="180,80 200,40 200,110 180,150" fill="#2D3748" />
          <!-- Compartment Wells -->
          <rect x="35" y="55" width="30" height="20" fill="#1A202C" rx="2" />
          <rect x="75" y="55" width="40" height="20" fill="#1A202C" rx="2" />
          <rect x="125" y="55" width="55" height="20" fill="#1A202C" rx="2" />
          <!-- Metric Ruler Marks on front face -->
          <line x1="30" y1="90" x2="170" y2="90" stroke="#E2E8F0" stroke-width="1.5" />
          <line x1="40" y1="90" x2="40" y2="100" stroke="#E2E8F0" stroke-width="1" />
          <line x1="60" y1="90" x2="60" y2="100" stroke="#E2E8F0" stroke-width="1" />
          <line x1="80" y1="90" x2="80" y2="105" stroke="#F4C95D" stroke-width="1.5" />
          <line x1="100" y1="90" x2="100" y2="100" stroke="#E2E8F0" stroke-width="1" />
          <line x1="120" y1="90" x2="120" y2="100" stroke="#E2E8F0" stroke-width="1" />
          <line x1="140" y1="90" x2="140" y2="105" stroke="#F4C95D" stroke-width="1.5" />
          <line x1="160" y1="90" x2="160" y2="100" stroke="#E2E8F0" stroke-width="1" />
        </g>
        """
    elif sku == "QQ-0013":  # Magnetic Particle Desk Sculpture
        return """
        <g transform="translate(130, 90)">
          <!-- Glass Chamber Outline -->
          <path d="M 40 40 L 100 40 L 95 110 Q 70 140 95 170 L 100 240 L 40 240 L 45 170 Q 70 140 45 110 Z" fill="none" stroke="#2CD4CD" stroke-width="2.5" />
          <!-- Heavy Brass Base -->
          <rect x="25" y="240" width="90" height="25" fill="#D69E2E" stroke="#B7791F" rx="3" />
          <!-- Magnetic Spikes (Ferrofluid cluster) -->
          <polygon points="70,180 62,240 78,240" fill="#1A202C" />
          <polygon points="55,195 48,240 64,240" fill="#1A202C" />
          <polygon points="85,195 76,240 92,240" fill="#1A202C" />
          <polygon points="45,215 40,240 52,240" fill="#1A202C" />
          <polygon points="95,215 88,240 100,240" fill="#1A202C" />
        </g>
        """
    elif sku == "QQ-0014":  # Infinite Equation Mouse Pad
        return """
        <g transform="translate(80, 150)">
          <!-- Oversized Mat Perspective -->
          <polygon points="10,130 230,130 210,30 30,30" fill="#1A202C" stroke="#158D89" stroke-width="3" />
          <!-- Green Stitched Border Highlight -->
          <polygon points="12,127 228,127 208,33 32,33" fill="none" stroke="#2CD4CD" stroke-width="1.2" stroke-dasharray="4,2" />
          <!-- Typeset Math Formulas on Mat -->
          <text x="60" y="60" font-family="'Courier New', monospace" font-size="10" fill="#FFFFFF">&#8747; e^(-x&#178;) dx = &#8730;&#960;</text>
          <text x="120" y="85" font-family="'Courier New', monospace" font-size="9" fill="#F4C95D">S = k_B ln &#937;</text>
          <text x="70" y="110" font-family="'Courier New', monospace" font-size="11" fill="#2CD4CD">H|&#968;&#9002; = E|&#968;&#9002;</text>
        </g>
        """
    elif sku == "QQ-0015":  # Newton's Cradle Executive Edition
        return """
        <g transform="translate(110, 110)">
          <!-- Wood Base -->
          <rect x="20" y="190" width="140" height="25" fill="#4A2E18" rx="3" stroke="#2D1A0E" />
          <!-- Steel Gantry Rails -->
          <path d="M 30 190 L 30 40 L 150 40 L 150 190" fill="none" stroke="#CBD5E0" stroke-width="5" />
          <!-- Five Wires and Spheres -->
          <!-- Sphere 1 (Swinging left) -->
          <line x1="45" y1="40" x2="25" y2="120" stroke="#A0AEC0" stroke-width="1.2" />
          <circle cx="25" cy="120" r="10" fill="#E2E8F0" stroke="#718096" stroke-width="1.5" />
          <!-- Sphere 2 -->
          <line x1="70" y1="40" x2="70" y2="140" stroke="#A0AEC0" stroke-width="1.2" />
          <circle cx="70" cy="140" r="10" fill="#CBD5E0" stroke="#718096" stroke-width="1.5" />
          <!-- Sphere 3 -->
          <line x1="90" y1="40" x2="90" y2="140" stroke="#A0AEC0" stroke-width="1.2" />
          <circle cx="90" cy="140" r="10" fill="#CBD5E0" stroke="#718096" stroke-width="1.5" />
          <!-- Sphere 4 -->
          <line x1="110" y1="40" x2="110" y2="140" stroke="#A0AEC0" stroke-width="1.2" />
          <circle cx="110" cy="140" r="10" fill="#CBD5E0" stroke="#718096" stroke-width="1.5" />
          <!-- Sphere 5 -->
          <line x1="130" y1="40" x2="130" y2="140" stroke="#A0AEC0" stroke-width="1.2" />
          <circle cx="130" cy="140" r="10" fill="#CBD5E0" stroke="#718096" stroke-width="1.5" />
        </g>
        """
    elif sku == "QQ-0016":  # Scientific Method Desk Clock
        return """
        <g transform="translate(130, 110)">
          <!-- Outer Aluminum Bezel -->
          <circle cx="70" cy="90" r="75" fill="#EDF2F7" stroke="#718096" stroke-width="5" />
          <!-- Inner Dial -->
          <circle cx="70" cy="90" r="65" fill="#FFFFFF" stroke="#CBD5E0" stroke-width="1.5" />
          <!-- Method Stage Indicators around dial -->
          <circle cx="70" cy="35" r="3" fill="#158D89" />
          <circle cx="109" cy="51" r="3" fill="#158D89" />
          <circle cx="125" cy="90" r="3" fill="#F4C95D" />
          <circle cx="109" cy="129" r="3" fill="#158D89" />
          <circle cx="70" cy="145" r="3" fill="#158D89" />
          <circle cx="31" cy="129" r="3" fill="#158D89" />
          <circle cx="15" cy="90" r="3" fill="#F4C95D" />
          <circle cx="31" cy="51" r="3" fill="#158D89" />
          <!-- Clock Hands -->
          <line x1="70" y1="90" x2="70" y2="50" stroke="#18243A" stroke-width="3.5" stroke-linecap="round" />
          <line x1="70" y1="90" x2="105" y2="90" stroke="#18243A" stroke-width="2.5" stroke-linecap="round" />
          <circle cx="70" cy="90" r="4.5" fill="#E53E3E" />
          <!-- Center Text -->
          <text x="70" y="115" font-family="sans-serif" font-size="7" font-weight="bold" fill="#718096" text-anchor="middle">PEER REVIEW</text>
        </g>
        """
    elif sku == "QQ-0017":  # Molecular Structure Pen Holder
        return """
        <g transform="translate(120, 110)">
          <!-- Tetrahedral Solid Brass Node Cluster -->
          <circle cx="80" cy="120" r="24" fill="#D69E2E" stroke="#B7791F" stroke-width="2" />
          <!-- Surrounding Node Arms -->
          <line x1="80" y1="120" x2="30" y2="70" stroke="#D69E2E" stroke-width="8" stroke-linecap="round" />
          <circle cx="30" cy="70" r="16" fill="#ECC94B" stroke="#B7791F" stroke-width="2" />
          <line x1="80" y1="120" x2="130" y2="70" stroke="#D69E2E" stroke-width="8" stroke-linecap="round" />
          <circle cx="130" cy="70" r="16" fill="#ECC94B" stroke="#B7791F" stroke-width="2" />
          <line x1="80" y1="120" x2="80" y2="180" stroke="#D69E2E" stroke-width="8" stroke-linecap="round" />
          <circle cx="80" cy="180" r="16" fill="#ECC94B" stroke="#B7791F" stroke-width="2" />
          <!-- Pens protruding from nodes -->
          <line x1="30" y1="70" x2="5" y2="20" stroke="#18243A" stroke-width="4" stroke-linecap="round" />
          <line x1="130" y1="70" x2="155" y2="20" stroke="#2B6CB0" stroke-width="4" stroke-linecap="round" />
          <line x1="80" y1="120" x2="95" y2="40" stroke="#E53E3E" stroke-width="4" stroke-linecap="round" />
        </g>
        """
    elif sku == "QQ-0018":  # Miniature Observatory Desk Globe
        return """
        <g transform="translate(130, 90)">
          <!-- Wood Base -->
          <ellipse cx="70" cy="240" rx="45" ry="14" fill="#4A2E18" stroke="#2D1A0E" />
          <!-- Stand Pillar -->
          <rect x="66" y="190" width="8" height="52" fill="#D69E2E" />
          <!-- Brass Meridian Ring -->
          <circle cx="70" cy="110" r="65" fill="none" stroke="#D69E2E" stroke-width="4" />
          <!-- Star Globe Sphere -->
          <circle cx="70" cy="110" r="54" fill="#18243A" stroke="#158D89" stroke-width="1.5" />
          <!-- Celestial Equator -->
          <ellipse cx="70" cy="110" rx="54" ry="18" fill="none" stroke="#2CD4CD" stroke-width="1.2" transform="rotate(-23.5, 70, 110)" />
          <!-- Constellation Dots & Lines -->
          <circle cx="50" cy="90" r="2" fill="#F4C95D" />
          <circle cx="65" cy="85" r="2.5" fill="#F4C95D" />
          <circle cx="85" cy="100" r="2" fill="#F4C95D" />
          <circle cx="95" cy="125" r="3" fill="#FFFFFF" />
          <line x1="50" y1="90" x2="65" y2="85" stroke="#FFFFFF" stroke-width="0.8" opacity="0.6" />
          <line x1="65" y1="85" x2="85" y2="100" stroke="#FFFFFF" stroke-width="0.8" opacity="0.6" />
          <line x1="85" y1="100" x2="95" y2="125" stroke="#FFFFFF" stroke-width="0.8" opacity="0.6" />
        </g>
        """
    elif sku == "QQ-0019":  # Adjustable Experiment Book Stand
        return """
        <g transform="translate(110, 110)">
          <!-- Easel Base & Backplate -->
          <polygon points="20,180 160,180 140,50 40,50" fill="#2D3748" stroke="#1A202C" stroke-width="2" />
          <!-- Open Textbook on Stand -->
          <polygon points="35,170 90,170 85,70 30,70" fill="#EDF2F7" stroke="#CBD5E0" />
          <polygon points="90,170 145,170 150,70 95,70" fill="#F7FAFC" stroke="#CBD5E0" />
          <line x1="90" y1="170" x2="90" y2="70" stroke="#A0AEC0" stroke-width="2" />
          <!-- Page text lines -->
          <line x1="40" y1="85" x2="75" y2="85" stroke="#718096" stroke-width="1" />
          <line x1="40" y1="100" x2="75" y2="100" stroke="#718096" stroke-width="1" />
          <line x1="105" y1="85" x2="140" y2="85" stroke="#718096" stroke-width="1" />
          <!-- Spring page clips holding pages down -->
          <line x1="32" y1="150" x2="48" y2="175" stroke="#F4C95D" stroke-width="3" stroke-linecap="round" />
          <line x1="148" y1="150" x2="132" y2="175" stroke="#F4C95D" stroke-width="3" stroke-linecap="round" />
        </g>
        """
    elif sku == "QQ-0020":  # Perfectly Aligned Cable Organizer
        return """
        <g transform="translate(110, 130)">
          <!-- Aluminum Block Dock -->
          <rect x="20" y="70" width="140" height="40" rx="6" fill="#A0AEC0" stroke="#718096" stroke-width="2" />
          <!-- 5 Parallel Channels with Collars -->
          <rect x="35" y="60" width="12" height="60" rx="4" fill="#158D89" />
          <rect x="60" y="60" width="12" height="60" rx="4" fill="#F4C95D" />
          <rect x="85" y="60" width="12" height="60" rx="4" fill="#3182CE" />
          <rect x="110" y="60" width="12" height="60" rx="4" fill="#E53E3E" />
          <rect x="135" y="60" width="12" height="60" rx="4" fill="#48BB78" />
          <!-- Cables running through collars -->
          <line x1="41" y1="20" x2="41" y2="160" stroke="#2D3748" stroke-width="3" />
          <line x1="66" y1="20" x2="66" y2="160" stroke="#2D3748" stroke-width="3" />
          <line x1="91" y1="20" x2="91" y2="160" stroke="#2D3748" stroke-width="3" />
          <line x1="116" y1="20" x2="116" y2="160" stroke="#2D3748" stroke-width="3" />
          <line x1="141" y1="20" x2="141" y2="160" stroke="#2D3748" stroke-width="3" />
        </g>
        """

    # Category C: Drinkware & Kitchen (QQ-0021 to QQ-0030)
    elif sku == "QQ-0021":  # Quantum Soup Mug
        return """
        <g transform="translate(110, 110)">
          <!-- Ceramic Mug Body -->
          <path d="M 40 50 L 140 50 L 130 180 Q 90 200 50 180 Z" fill="#18243A" stroke="#2D3748" stroke-width="2" />
          <!-- Handle -->
          <path d="M 135 70 Q 185 110 125 150" fill="none" stroke="#18243A" stroke-width="12" stroke-linecap="round" />
          <!-- Thermal equation revealed on mug -->
          <path d="M 55 120 Q 70 95 90 120 T 120 120" fill="none" stroke="#2CD4CD" stroke-width="2.5" />
          <text x="90" y="145" font-family="'Courier New', monospace" font-size="10" fill="#F4C95D" text-anchor="middle">i&#8463;&#8706;&#968;/&#8706;t = &#292;&#968;</text>
          <!-- Steam curls -->
          <path d="M 65 35 Q 60 15 70 5" fill="none" stroke="#A0AEC0" stroke-width="2" stroke-linecap="round" opacity="0.6" />
          <path d="M 90 35 Q 95 15 85 5" fill="none" stroke="#A0AEC0" stroke-width="2" stroke-linecap="round" opacity="0.6" />
          <path d="M 115 35 Q 110 15 120 5" fill="none" stroke="#A0AEC0" stroke-width="2" stroke-linecap="round" opacity="0.6" />
        </g>
        """
    elif sku == "QQ-0022":  # Periodic Table Coffee Tumbler
        return """
        <g transform="translate(130, 90)">
          <!-- Tumbler Body -->
          <path d="M 40 40 L 100 40 L 90 220 L 50 220 Z" fill="#2D3748" stroke="#1A202C" stroke-width="2" />
          <!-- Lid with slider -->
          <rect x="35" y="30" width="70" height="12" rx="3" fill="#1A202C" />
          <rect x="60" y="27" width="20" height="5" rx="2" fill="#F4C95D" />
          <!-- Laser etched periodic table pattern -->
          <g transform="translate(48, 60)">
            <rect x="0" y="0" width="10" height="10" fill="none" stroke="#CBD5E0" stroke-width="0.8" />
            <text x="5" y="8" font-family="sans-serif" font-size="6" fill="#E2E8F0" text-anchor="middle">H</text>
            <rect x="34" y="0" width="10" height="10" fill="none" stroke="#CBD5E0" stroke-width="0.8" />
            <text x="39" y="8" font-family="sans-serif" font-size="6" fill="#E2E8F0" text-anchor="middle">He</text>
            <rect x="0" y="15" width="10" height="10" fill="none" stroke="#CBD5E0" stroke-width="0.8" />
            <text x="5" y="23" font-family="sans-serif" font-size="6" fill="#E2E8F0" text-anchor="middle">Li</text>
            <rect x="12" y="15" width="10" height="10" fill="none" stroke="#CBD5E0" stroke-width="0.8" />
            <text x="17" y="23" font-family="sans-serif" font-size="6" fill="#E2E8F0" text-anchor="middle">Be</text>
            <rect x="24" y="15" width="10" height="10" fill="none" stroke="#CBD5E0" stroke-width="0.8" />
            <text x="29" y="23" font-family="sans-serif" font-size="6" fill="#E2E8F0" text-anchor="middle">B</text>
            <rect x="34" y="15" width="10" height="10" fill="none" stroke="#CBD5E0" stroke-width="0.8" />
            <text x="39" y="23" font-family="sans-serif" font-size="6" fill="#E2E8F0" text-anchor="middle">C</text>
          </g>
        </g>
        """
    elif sku == "QQ-0023":  # Particle Collision Coaster Set
        return """
        <g transform="translate(110, 110)">
          <!-- Coaster Stand -->
          <rect x="25" y="180" width="130" height="15" fill="#D69E2E" rx="3" />
          <!-- Coaster Disc Perspective -->
          <circle cx="90" cy="110" r="65" fill="#F7FAFC" stroke="#E2E8F0" stroke-width="3" />
          <!-- Collision Spiral Tracks -->
          <path d="M 90 110 Q 70 80 50 110 T 80 150 T 120 120" fill="none" stroke="#3182CE" stroke-width="2" />
          <path d="M 90 110 Q 110 70 140 85" fill="none" stroke="#E53E3E" stroke-width="2" />
          <path d="M 90 110 L 40 60" fill="none" stroke="#38A169" stroke-width="2" stroke-dasharray="3,2" />
          <circle cx="90" cy="110" r="4" fill="#F4C95D" />
        </g>
        """
    elif sku == "QQ-0024":  # Molecular Measuring Spoon Kit
        return """
        <g transform="translate(110, 110)">
          <!-- Linked Ring -->
          <circle cx="90" cy="40" r="14" fill="none" stroke="#A0AEC0" stroke-width="3" />
          <!-- Spoon Handles and Bowls Fan -->
          <path d="M 85 50 L 50 180" stroke="#CBD5E0" stroke-width="5" />
          <ellipse cx="45" cy="190" rx="14" ry="18" fill="#E2E8F0" stroke="#A0AEC0" />
          <path d="M 90 50 L 90 190" stroke="#CBD5E0" stroke-width="5" />
          <ellipse cx="90" cy="200" rx="18" ry="22" fill="#E2E8F0" stroke="#A0AEC0" />
          <path d="M 95 50 L 135 180" stroke="#CBD5E0" stroke-width="5" />
          <ellipse cx="140" cy="190" rx="12" ry="16" fill="#E2E8F0" stroke="#A0AEC0" />
          <!-- Mole engraving indicator -->
          <text x="90" y="130" font-family="monospace" font-size="7" fill="#4A5568" text-anchor="middle">0.05 mol</text>
        </g>
        """
    elif sku == "QQ-0025":  # Thermodynamic Tea Flask
        return """
        <g transform="translate(130, 90)">
          <!-- Dual-Wall Glass Flask -->
          <rect x="40" y="50" width="60" height="180" rx="10" fill="none" stroke="#2CD4CD" stroke-width="3" />
          <rect x="47" y="58" width="46" height="164" rx="6" fill="#ED8936" opacity="0.3" stroke="#CBD5E0" />
          <!-- Stainless Cap with LED Temp -->
          <rect x="35" y="32" width="70" height="20" rx="4" fill="#2D3748" stroke="#1A202C" />
          <text x="70" y="46" font-family="'Courier New', monospace" font-size="11" font-weight="bold" fill="#48BB78" text-anchor="middle">78&#176;C</text>
          <!-- Internal tea infuser mesh basket -->
          <rect x="52" y="60" width="36" height="60" fill="none" stroke="#718096" stroke-width="1.2" stroke-dasharray="2,2" />
        </g>
        """
    elif sku == "QQ-0026":  # Nebula Ceramic Dinner Plate
        return """
        <g transform="translate(110, 110)">
          <!-- Outer Rim -->
          <circle cx="90" cy="90" r="80" fill="#FFFFFF" stroke="#CBD5E0" stroke-width="3" />
          <circle cx="90" cy="90" r="76" fill="none" stroke="#D69E2E" stroke-width="1.2" />
          <!-- Inner Well with Swirling Nebula Glaze -->
          <circle cx="90" cy="90" r="60" fill="#18243A" />
          <path d="M 60 70 Q 90 50 110 80 T 130 110 T 70 120 Z" fill="#805AD5" opacity="0.6" />
          <path d="M 80 90 Q 110 80 120 100 T 90 125 Z" fill="#319795" opacity="0.7" />
          <!-- Stars -->
          <circle cx="75" cy="75" r="1.5" fill="#FFFFFF" />
          <circle cx="105" cy="85" r="2" fill="#F4C95D" />
          <circle cx="90" cy="110" r="1.5" fill="#FFFFFF" />
        </g>
        """
    elif sku == "QQ-0027":  # Experimental Breakfast Bowl
        return """
        <g transform="translate(110, 120)">
          <!-- Wide Cereal Bowl -->
          <path d="M 20 60 Q 90 160 160 60 Z" fill="#EDF2F7" stroke="#718096" stroke-width="2.5" />
          <ellipse cx="90" cy="60" rx="70" ry="18" fill="#F7FAFC" stroke="#718096" stroke-width="2" />
          <!-- Graduated Rings inside bowl -->
          <ellipse cx="90" cy="75" rx="55" ry="12" fill="none" stroke="#158D89" stroke-width="1.2" stroke-dasharray="4,2" />
          <text x="145" y="77" font-family="monospace" font-size="7" fill="#158D89">450ml</text>
          <ellipse cx="90" cy="88" rx="40" ry="8" fill="none" stroke="#158D89" stroke-width="1.2" stroke-dasharray="4,2" />
          <text x="130" y="90" font-family="monospace" font-size="7" fill="#158D89">300ml</text>
        </g>
        """
    elif sku == "QQ-0028":  # Atomic Structure Water Bottle
        return """
        <g transform="translate(130, 80)">
          <!-- Teal Water Bottle Body -->
          <rect x="45" y="70" width="50" height="170" rx="8" fill="#2C7A7B" stroke="#234E52" stroke-width="2" />
          <!-- Neck & Cap with Loop -->
          <rect x="55" y="45" width="30" height="25" fill="#285E61" />
          <path d="M 60 45 L 60 25 Q 70 15 80 25 L 80 45 Z" fill="#E2E8F0" stroke="#718096" stroke-width="1.5" />
          <!-- Etched Orbitals -->
          <ellipse cx="70" cy="130" rx="20" ry="8" fill="none" stroke="#E2E8F0" stroke-width="1.5" transform="rotate(-30, 70, 130)" />
          <ellipse cx="70" cy="130" rx="20" ry="8" fill="none" stroke="#E2E8F0" stroke-width="1.5" transform="rotate(30, 70, 130)" />
          <ellipse cx="70" cy="180" rx="18" ry="18" fill="none" stroke="#F4C95D" stroke-width="1.5" stroke-dasharray="3,2" />
        </g>
        """
    elif sku == "QQ-0029":  # Precision Pizza Cutting Wheel
        return """
        <g transform="translate(110, 110)">
          <!-- Handle -->
          <path d="M 30 50 L 80 100 L 95 85 L 45 35 Z" fill="#2D3748" rx="4" />
          <rect x="75" y="85" width="25" height="15" fill="#718096" rx="2" />
          <!-- Rotary Circular Blade -->
          <circle cx="120" cy="120" r="50" fill="#E2E8F0" stroke="#718096" stroke-width="2.5" />
          <!-- Bearing center -->
          <circle cx="120" cy="120" r="10" fill="#4A5568" stroke="#F4C95D" stroke-width="2" />
          <!-- Protractor angle lines etched on blade -->
          <line x1="120" y1="70" x2="120" y2="170" stroke="#A0AEC0" stroke-width="1" />
          <line x1="70" y1="120" x2="170" y2="120" stroke="#A0AEC0" stroke-width="1" />
          <line x1="85" y1="85" x2="155" y2="155" stroke="#A0AEC0" stroke-width="1" />
          <text x="140" y="105" font-family="sans-serif" font-size="7" fill="#718096">&#960;/4</text>
        </g>
        """
    elif sku == "QQ-0030":  # Galaxy Pattern Coffee Press
        return """
        <g transform="translate(120, 80)">
          <!-- Borosilicate Glass Beaker -->
          <rect x="40" y="60" width="70" height="160" rx="4" fill="none" stroke="#CBD5E0" stroke-width="2" />
          <!-- Black Metal Constellation Cage -->
          <rect x="38" y="90" width="74" height="120" fill="#1A202C" rx="2" opacity="0.85" />
          <!-- Constellation laser cutouts -->
          <circle cx="55" cy="115" r="2.5" fill="#F4C95D" />
          <circle cx="75" cy="130" r="2.5" fill="#F4C95D" />
          <circle cx="90" cy="115" r="2" fill="#F4C95D" />
          <line x1="55" y1="115" x2="75" y2="130" stroke="#FFFFFF" stroke-width="1" />
          <line x1="75" y1="130" x2="90" y2="115" stroke="#FFFFFF" stroke-width="1" />
          <!-- Plunger rod and handle -->
          <line x1="75" y1="15" x2="75" y2="170" stroke="#A0AEC0" stroke-width="3" />
          <circle cx="75" cy="15" r="8" fill="#1A202C" />
          <ellipse cx="75" cy="170" rx="34" ry="8" fill="#4A5568" stroke="#E2E8F0" />
          <!-- Handle -->
          <path d="M 112 80 Q 150 130 112 180" fill="none" stroke="#1A202C" stroke-width="8" stroke-linecap="round" />
        </g>
        """

    # Category D: Home & Decor (QQ-0031 to QQ-0040)
    elif sku == "QQ-0031":  # Optimal Seating Position Cushion
        return """
        <g transform="translate(100, 120)">
          <!-- Ergonomic Cushion Body -->
          <rect x="20" y="40" width="160" height="120" rx="25" fill="#18243A" stroke="#2B4C7E" stroke-width="3" />
          <!-- Coccyx relief cutout -->
          <path d="M 80 40 Q 100 85 120 40 Z" fill="#EDF2F7" />
          <!-- Gold Embroidered Crosshairs & Target -->
          <circle cx="100" cy="110" r="28" fill="none" stroke="#F4C95D" stroke-width="2" stroke-dasharray="5,3" />
          <circle cx="100" cy="110" r="14" fill="none" stroke="#F4C95D" stroke-width="1.5" />
          <line x1="100" y1="75" x2="100" y2="145" stroke="#F4C95D" stroke-width="1.5" />
          <line x1="65" y1="110" x2="135" y2="110" stroke="#F4C95D" stroke-width="1.5" />
          <text x="100" y="113" font-family="sans-serif" font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle">OPTIMAL</text>
        </g>
        """
    elif sku == "QQ-0032":  # String Theory Throw Blanket
        return """
        <g transform="translate(110, 110)">
          <!-- Folded Woven Blanket -->
          <rect x="25" y="40" width="130" height="110" rx="8" fill="#18243A" stroke="#158D89" stroke-width="2" />
          <!-- Woven Calabi-Yau geometry curves -->
          <path d="M 35 70 Q 75 40 100 80 T 145 70" fill="none" stroke="#F4C95D" stroke-width="2" />
          <path d="M 35 100 Q 80 130 110 95 T 145 110" fill="none" stroke="#2CD4CD" stroke-width="2" />
          <path d="M 45 130 Q 90 90 120 135" fill="none" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="3,2" />
          <!-- Fringed tassel edge -->
          <g transform="translate(25, 150)">
            <line x1="10" y1="0" x2="10" y2="15" stroke="#F4C95D" stroke-width="2" />
            <line x1="30" y1="0" x2="30" y2="15" stroke="#E2E8F0" stroke-width="2" />
            <line x1="50" y1="0" x2="50" y2="15" stroke="#F4C95D" stroke-width="2" />
            <line x1="70" y1="0" x2="70" y2="15" stroke="#E2E8F0" stroke-width="2" />
            <line x1="90" y1="0" x2="90" y2="15" stroke="#F4C95D" stroke-width="2" />
            <line x1="110" y1="0" x2="110" y2="15" stroke="#E2E8F0" stroke-width="2" />
          </g>
        </g>
        """
    elif sku == "QQ-0033":  # Galactic Coordinate Wall Clock
        return """
        <g transform="translate(120, 100)">
          <!-- Clock Frame -->
          <circle cx="80" cy="80" r="75" fill="#18243A" stroke="#718096" stroke-width="4" />
          <!-- Milky way galaxy disc outline -->
          <ellipse cx="80" cy="80" rx="65" ry="25" fill="none" stroke="#2CD4CD" stroke-width="1.5" transform="rotate(-30, 80, 80)" opacity="0.7" />
          <circle cx="80" cy="80" r="12" fill="#F4C95D" opacity="0.8" />
          <!-- Hour markers as right ascension hours -->
          <text x="80" y="25" font-family="monospace" font-size="8" fill="#E2E8F0" text-anchor="middle">0h</text>
          <text x="135" y="83" font-family="monospace" font-size="8" fill="#E2E8F0" text-anchor="middle">6h</text>
          <text x="80" y="142" font-family="monospace" font-size="8" fill="#E2E8F0" text-anchor="middle">12h</text>
          <text x="25" y="83" font-family="monospace" font-size="8" fill="#E2E8F0" text-anchor="middle">18h</text>
          <!-- Hands -->
          <line x1="80" y1="80" x2="80" y2="45" stroke="#FFFFFF" stroke-width="2.5" />
          <line x1="80" y1="80" x2="115" y2="70" stroke="#F4C95D" stroke-width="2" />
        </g>
        """
    elif sku == "QQ-0034":  # Whiteboard Equation Wall Poster
        return """
        <g transform="translate(100, 110)">
          <!-- Aluminum Whiteboard Frame -->
          <rect x="20" y="30" width="160" height="120" fill="#FFFFFF" stroke="#718096" stroke-width="6" rx="2" />
          <!-- Faint isometric grid -->
          <path d="M 30 50 L 170 50 M 30 70 L 170 70 M 30 90 L 170 90 M 30 110 L 170 110 M 30 130 L 170 130" stroke="#E2E8F0" stroke-width="1" />
          <!-- Marker equations -->
          <text x="40" y="65" font-family="'Courier New', monospace" font-size="11" fill="#2B6CB0">E&#178; = (pc)&#178; + (mc&#178;)&#178;</text>
          <text x="40" y="95" font-family="'Courier New', monospace" font-size="10" fill="#C53030">&#8747; B &#8226; dA = 0</text>
          <!-- Magnetic pen rail on bottom -->
          <rect x="50" y="150" width="60" height="5" fill="#4A5568" rx="2" />
        </g>
        """
    elif sku == "QQ-0035":  # Solar System Floor Rug
        return """
        <g transform="translate(110, 110)">
          <!-- Circular Rug Edge with Overlock Stitch -->
          <circle cx="90" cy="90" r="80" fill="#1A202C" stroke="#4A5568" stroke-width="4" stroke-dasharray="6,2" />
          <!-- Sun in center -->
          <circle cx="90" cy="90" r="16" fill="#F4C95D" />
          <!-- Concentric Planetary Orbits -->
          <circle cx="90" cy="90" r="28" fill="none" stroke="#718096" stroke-width="1" stroke-dasharray="3,2" />
          <circle cx="108" cy="73" r="3" fill="#A0AEC0" /> <!-- Mercury -->
          <circle cx="90" cy="90" r="42" fill="none" stroke="#718096" stroke-width="1" stroke-dasharray="3,2" />
          <circle cx="62" cy="62" r="4" fill="#ED8936" /> <!-- Venus -->
          <circle cx="90" cy="90" r="56" fill="none" stroke="#718096" stroke-width="1" stroke-dasharray="3,2" />
          <circle cx="140" cy="105" r="4.5" fill="#3182CE" /> <!-- Earth -->
          <circle cx="90" cy="90" r="70" fill="none" stroke="#718096" stroke-width="1" stroke-dasharray="3,2" />
          <circle cx="45" cy="130" r="3.5" fill="#E53E3E" /> <!-- Mars -->
        </g>
        """
    elif sku == "QQ-0036":  # Molecular Geometry Cushion Set
        return """
        <g transform="translate(100, 110)">
          <!-- Three Overlapping Polyhedral Pillows -->
          <polygon points="60,40 100,55 90,110 45,95" fill="#2B6CB0" stroke="#CBD5E0" stroke-width="2" />
          <polygon points="100,80 150,60 160,120 110,135" fill="#2C7A7B" stroke="#CBD5E0" stroke-width="2" />
          <polygon points="50,110 105,100 120,160 65,170" fill="#C05621" stroke="#CBD5E0" stroke-width="2" />
          <!-- Embroidered vertex lines -->
          <line x1="60" y1="40" x2="90" y2="110" stroke="#FFFFFF" stroke-width="1.5" />
          <line x1="100" y1="80" x2="160" y2="120" stroke="#FFFFFF" stroke-width="1.5" />
          <line x1="50" y1="110" x2="120" y2="160" stroke="#FFFFFF" stroke-width="1.5" />
        </g>
        """
    elif sku == "QQ-0037":  # Supernova Ambient Night Light
        return """
        <g transform="translate(120, 90)">
          <!-- Glowing Sphere -->
          <circle cx="80" cy="90" r="50" fill="#805AD5" />
          <circle cx="80" cy="90" r="40" fill="#ED8936" opacity="0.8" />
          <circle cx="80" cy="90" r="25" fill="#F4C95D" opacity="0.9" />
          <circle cx="80" cy="90" r="60" fill="none" stroke="#D6BCFA" stroke-width="2" opacity="0.4" />
          <!-- Brass Tripod Stand -->
          <line x1="80" y1="140" x2="40" y2="210" stroke="#D69E2E" stroke-width="4" stroke-linecap="round" />
          <line x1="80" y1="140" x2="120" y2="210" stroke="#D69E2E" stroke-width="4" stroke-linecap="round" />
          <line x1="80" y1="140" x2="80" y2="205" stroke="#B7791F" stroke-width="4" stroke-linecap="round" />
        </g>
        """
    elif sku == "QQ-0038":  # Mathematical Wallpaper Art Print
        return """
        <g transform="translate(110, 90)">
          <!-- Picture Frame -->
          <rect x="25" y="25" width="130" height="170" fill="#FFFFFF" stroke="#1A202C" stroke-width="6" rx="2" />
          <rect x="35" y="35" width="110" height="150" fill="#F7FAFC" stroke="#E2E8F0" />
          <!-- Penrose Aperiodic Tiling Tessellation Graphic -->
          <g transform="translate(50, 50)">
            <polygon points="40,20 60,35 40,50 20,35" fill="#EBF8FF" stroke="#3182CE" stroke-width="1.2" />
            <polygon points="60,35 80,20 80,50 60,65" fill="#FEFCBF" stroke="#D69E2E" stroke-width="1.2" />
            <polygon points="20,35 20,65 40,80 40,50" fill="#FEFCBF" stroke="#D69E2E" stroke-width="1.2" />
            <polygon points="40,50 60,65 40,80 20,65" fill="#EBF8FF" stroke="#3182CE" stroke-width="1.2" />
            <polygon points="60,65 80,50 80,80 60,95" fill="#EBF8FF" stroke="#3182CE" stroke-width="1.2" />
          </g>
        </g>
        """
    elif sku == "QQ-0039":  # Cosmic Background Shower Curtain
        return """
        <g transform="translate(110, 100)">
          <!-- Curtain Hanging Bar -->
          <line x1="15" y1="30" x2="165" y2="30" stroke="#718096" stroke-width="4" stroke-linecap="round" />
          <!-- Hanging Rings -->
          <circle cx="35" cy="30" r="5" fill="none" stroke="#CBD5E0" stroke-width="2" />
          <circle cx="65" cy="30" r="5" fill="none" stroke="#CBD5E0" stroke-width="2" />
          <circle cx="95" cy="30" r="5" fill="none" stroke="#CBD5E0" stroke-width="2" />
          <circle cx="125" cy="30" r="5" fill="none" stroke="#CBD5E0" stroke-width="2" />
          <circle cx="150" cy="30" r="5" fill="none" stroke="#CBD5E0" stroke-width="2" />
          <!-- Curtain Body with Planck CMB Speckles -->
          <rect x="25" y="38" width="135" height="150" fill="#1A202C" rx="2" />
          <!-- Speckled Heat Anisotropy Map -->
          <ellipse cx="90" cy="115" rx="55" ry="32" fill="#2B6CB0" opacity="0.8" />
          <circle cx="75" cy="110" r="8" fill="#E53E3E" opacity="0.8" />
          <circle cx="110" cy="120" r="10" fill="#D69E2E" opacity="0.8" />
          <circle cx="95" cy="105" r="6" fill="#38A169" opacity="0.8" />
        </g>
        """
    elif sku == "QQ-0040":  # Symmetry Alignment Wall Shelf
        return """
        <g transform="translate(90, 130)">
          <!-- Shelf Profile -->
          <polygon points="20,100 200,100 180,60 40,60" fill="#4A5568" stroke="#2D3748" />
          <rect x="20" y="100" width="180" height="20" fill="#2D3748" />
          <!-- Dual Green Spirit Bubble Levels -->
          <rect x="55" y="104" width="30" height="10" rx="3" fill="#48BB78" stroke="#22543D" stroke-width="1.5" />
          <circle cx="70" cy="109" r="2.5" fill="#FFFFFF" />
          <rect x="135" y="104" width="30" height="10" rx="3" fill="#48BB78" stroke="#22543D" stroke-width="1.5" />
          <circle cx="150" cy="109" r="2.5" fill="#FFFFFF" />
        </g>
        """

    # Category E: Science Gadgets (QQ-0041 to QQ-0050)
    elif sku == "QQ-0041":  # Pocket Spectroscope Explorer
        return """
        <g transform="translate(100, 120)">
          <!-- Optical Barrel Tube -->
          <rect x="40" y="70" width="120" height="30" rx="4" fill="#2D3748" stroke="#1A202C" stroke-width="2" />
          <rect x="25" y="65" width="15" height="40" fill="#4A5568" rx="2" /> <!-- Eyepiece -->
          <rect x="160" y="73" width="15" height="24" fill="#718096" rx="2" /> <!-- Slit -->
          <!-- Dispersed Spectral Rainbow Beam -->
          <polygon points="175,85 210,50 210,120" fill="url(#rainbowGrad)" opacity="0.85" />
        </g>
        <defs>
          <linearGradient id="rainbowGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#E53E3E" />
            <stop offset="25%" stop-color="#ED8936" />
            <stop offset="50%" stop-color="#ECC94B" />
            <stop offset="75%" stop-color="#48BB78" />
            <stop offset="100%" stop-color="#3182CE" />
          </linearGradient>
        </defs>
        """
    elif sku == "QQ-0042":  # Magnetic Levitation Display Kit
        return """
        <g transform="translate(110, 100)">
          <!-- Electromagnetic Base -->
          <rect x="25" y="160" width="130" height="40" rx="8" fill="#1A202C" stroke="#718096" stroke-width="2" />
          <!-- Upward Ambient Glow Ring -->
          <ellipse cx="90" cy="160" rx="45" ry="12" fill="none" stroke="#2CD4CD" stroke-width="3" />
          <!-- Floating Magnetic Disc Hovering -->
          <g transform="translate(0, -35)">
            <ellipse cx="90" cy="120" rx="35" ry="10" fill="#D69E2E" stroke="#B7791F" stroke-width="2" />
            <rect x="55" y="112" width="70" height="8" fill="#ECC94B" />
            <ellipse cx="90" cy="112" rx="35" ry="10" fill="#F4C95D" />
          </g>
          <!-- Magnetic Flux Lines -->
          <path d="M 60 155 Q 50 120 70 95" fill="none" stroke="#2CD4CD" stroke-width="1.5" stroke-dasharray="3,2" />
          <path d="M 120 155 Q 130 120 110 95" fill="none" stroke="#2CD4CD" stroke-width="1.5" stroke-dasharray="3,2" />
        </g>
        """
    elif sku == "QQ-0043":  # DIY Electromagnet Experiment Box
        return """
        <g transform="translate(100, 110)">
          <!-- Wooden Bench Enclosure -->
          <rect x="20" y="50" width="160" height="110" rx="6" fill="#D69E2E" stroke="#744210" stroke-width="3" />
          <!-- Iron Core Rod with Copper Coil Windings -->
          <rect x="40" y="90" width="120" height="20" rx="3" fill="#718096" />
          <rect x="60" y="85" width="80" height="30" fill="#C05621" stroke="#9C4221" stroke-width="1.5" />
          <!-- Galvanometer Dial -->
          <circle cx="140" cy="75" r="16" fill="#FFFFFF" stroke="#4A5568" stroke-width="1.5" />
          <line x1="140" y1="75" x2="135" y2="65" stroke="#E53E3E" stroke-width="1.5" />
          <!-- Plotting Compass -->
          <circle cx="45" cy="135" r="10" fill="#EDF2F7" stroke="#4A5568" />
          <polygon points="45,127 48,135 42,135" fill="#E53E3E" />
          <polygon points="45,143 48,135 42,135" fill="#3182CE" />
        </g>
        """
    elif sku == "QQ-0044":  # Desktop Plasma Orb
        return """
        <g transform="translate(120, 80)">
          <!-- Black Base -->
          <polygon points="45,230 115,230 105,170 55,170" fill="#1A202C" stroke="#2D3748" />
          <!-- Central Electrode Sphere -->
          <circle cx="80" cy="100" r="65" fill="none" stroke="#A0AEC0" stroke-width="2.5" />
          <circle cx="80" cy="100" r="12" fill="#1A202C" stroke="#805AD5" stroke-width="2" />
          <!-- Plasma Lightning Tendrils -->
          <path d="M 80 100 Q 60 70 45 50 Q 55 40 40 45" fill="none" stroke="#9F7AEA" stroke-width="2" />
          <path d="M 80 100 Q 110 80 125 55 Q 120 45 135 60" fill="none" stroke="#2CD4CD" stroke-width="2" />
          <path d="M 80 100 Q 100 130 120 145" fill="none" stroke="#ED64A6" stroke-width="2" />
          <path d="M 80 100 Q 50 120 30 120" fill="none" stroke="#9F7AEA" stroke-width="2" />
        </g>
        """
    elif sku == "QQ-0045":  # Mini Solar Tracking Kit
        return """
        <g transform="translate(110, 100)">
          <!-- Tabletop Pedestal Base -->
          <rect x="40" y="180" width="100" height="20" rx="4" fill="#2D3748" />
          <!-- Dual Servos Gantry -->
          <rect x="80" y="120" width="20" height="60" fill="#4A5568" />
          <!-- Solar Panel Gimbal Tilted -->
          <polygon points="30,80 150,50 140,110 20,140" fill="#1A365D" stroke="#3182CE" stroke-width="2" />
          <!-- Photovoltaic Grid Matrix -->
          <line x1="60" y1="72" x2="50" y2="132" stroke="#63B3ED" stroke-width="1.5" />
          <line x1="90" y1="65" x2="80" y2="125" stroke="#63B3ED" stroke-width="1.5" />
          <line x1="120" y1="57" x2="110" y2="117" stroke="#63B3ED" stroke-width="1.5" />
          <!-- Light Sensor Cross -->
          <circle cx="85" cy="90" r="4" fill="#F4C95D" />
        </g>
        """
    elif sku == "QQ-0046":  # Precision Digital Microscope
        return """
        <g transform="translate(110, 80)">
          <!-- Base Stage -->
          <rect x="25" y="210" width="130" height="20" rx="4" fill="#2D3748" stroke="#1A202C" />
          <!-- Vertical Focusing Column -->
          <rect x="120" y="50" width="16" height="160" fill="#4A5568" />
          <circle cx="128" cy="130" r="10" fill="#CBD5E0" stroke="#718096" stroke-width="2" />
          <!-- Digital IPS Screen Monitor -->
          <rect x="35" y="30" width="75" height="55" rx="4" fill="#1A202C" stroke="#2B6CB0" stroke-width="2" />
          <rect x="40" y="35" width="65" height="45" fill="#2B6CB0" />
          <circle cx="72" cy="57" r="12" fill="#48BB78" opacity="0.8" /> <!-- Cell image -->
          <!-- Optical Lens Objective -->
          <rect x="62" y="90" width="20" height="50" fill="#718096" rx="2" />
          <circle cx="72" cy="145" r="7" fill="#E2E8F0" />
        </g>
        """
    elif sku == "QQ-0047":  # Gyroscopic Motion Demonstrator
        return """
        <g transform="translate(120, 90)">
          <!-- Brass Pedestal Tower -->
          <path d="M 80 150 L 65 240 L 95 240 Z" fill="#D69E2E" stroke="#B7791F" stroke-width="2" />
          <!-- Brass Flywheel balanced on tip -->
          <g transform="translate(0, -10)">
            <circle cx="80" cy="120" r="45" fill="#ECC94B" stroke="#B7791F" stroke-width="4" />
            <circle cx="80" cy="120" r="25" fill="#D69E2E" />
            <circle cx="80" cy="120" r="6" fill="#1A202C" />
            <!-- Gimbal Ring -->
            <ellipse cx="80" cy="120" rx="55" ry="18" fill="none" stroke="#718096" stroke-width="3" transform="rotate(-25, 80, 120)" />
          </g>
        </g>
        """
    elif sku == "QQ-0048":  # Quantum Probability Spinner
        return """
        <g transform="translate(130, 110)">
          <!-- Glass Concave Base -->
          <ellipse cx="70" cy="180" rx="55" ry="14" fill="#EDF2F7" stroke="#2CD4CD" stroke-width="2" />
          <!-- Titanium Top Body -->
          <polygon points="70,50 95,140 45,140" fill="#718096" stroke="#4A5568" stroke-width="2" />
          <!-- Spindle Stem -->
          <rect x="68" y="25" width="4" height="35" rx="2" fill="#A0AEC0" />
          <!-- Ceramic Ball Tip -->
          <circle cx="70" cy="175" r="4" fill="#FFFFFF" stroke="#4A5568" />
          <!-- Ket Notation on Rim -->
          <text x="70" y="130" font-family="'Courier New', monospace" font-size="9" fill="#F4C95D" text-anchor="middle">|&#968;&#9002; = &#945;|0&#9002;+&#946;|1&#9002;</text>
        </g>
        """
    elif sku == "QQ-0049":  # Digital Astronomy Star Projector
        return """
        <g transform="translate(120, 100)">
          <!-- Spherical Projector Dome -->
          <circle cx="80" cy="100" r="60" fill="#18243A" stroke="#2B4C7E" stroke-width="3" />
          <!-- Projection Lens Emitter -->
          <circle cx="80" cy="60" r="18" fill="#F4C95D" stroke="#FFFFFF" stroke-width="2" />
          <!-- Beamed Star Field Projection -->
          <polygon points="80,60 20,-10 140,-10" fill="#ECC94B" opacity="0.25" />
          <!-- Pedestal Ring -->
          <path d="M 40 145 Q 80 170 120 145" fill="none" stroke="#D69E2E" stroke-width="6" stroke-linecap="round" />
        </g>
        """
    elif sku == "QQ-0050":  # Portable Weather Experiment Station
        return """
        <g transform="translate(130, 90)">
          <!-- Rugged Yellow & Black Handheld Body -->
          <rect x="40" y="70" width="60" height="140" rx="10" fill="#ECC94B" stroke="#1A202C" stroke-width="3" />
          <!-- LCD Display -->
          <rect x="48" y="85" width="44" height="40" fill="#2D3748" rx="2" />
          <text x="70" y="102" font-family="monospace" font-size="9" fill="#48BB78" text-anchor="middle">1013 hPa</text>
          <text x="70" y="116" font-family="monospace" font-size="9" fill="#48BB78" text-anchor="middle">24.5&#176;C</text>
          <!-- Wind Anemometer Cups on top -->
          <line x1="70" y1="70" x2="70" y2="35" stroke="#1A202C" stroke-width="3" />
          <circle cx="50" cy="35" r="8" fill="#1A202C" />
          <circle cx="90" cy="35" r="8" fill="#1A202C" />
          <circle cx="70" cy="25" r="8" fill="#1A202C" />
        </g>
        """

    # Category F: Puzzles & Games (QQ-0051 to QQ-0060)
    elif sku == "QQ-0051":  # Quantum Logic Puzzle Cube
        return """
        <g transform="translate(110, 100)">
          <!-- Isometric 3D Cube View -->
          <!-- Top Face -->
          <polygon points="90,30 140,55 90,80 40,55" fill="#2B6CB0" stroke="#1A202C" stroke-width="2" />
          <text x="90" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="#FFFFFF" text-anchor="middle">H</text>
          <!-- Left Face -->
          <polygon points="40,55 90,80 90,140 40,115" fill="#319795" stroke="#1A202C" stroke-width="2" />
          <text x="65" y="105" font-family="sans-serif" font-size="12" font-weight="bold" fill="#FFFFFF" text-anchor="middle">&#963;_x</text>
          <!-- Right Face -->
          <polygon points="90,80 140,55 140,115 90,140" fill="#D69E2E" stroke="#1A202C" stroke-width="2" />
          <text x="115" y="105" font-family="sans-serif" font-size="12" font-weight="bold" fill="#FFFFFF" text-anchor="middle">&#963;_z</text>
        </g>
        """
    elif sku == "QQ-0052":  # Periodic Table Strategy Game
        return """
        <g transform="translate(100, 110)">
          <!-- Board Game Box / Board -->
          <polygon points="30,60 170,40 180,140 40,160" fill="#2D3748" stroke="#F4C95D" stroke-width="3" />
          <!-- Miniature Erlenmeyer Flask Pawns -->
          <polygon points="70,100 80,100 85,120 65,120" fill="#E53E3E" stroke="#FFFFFF" />
          <polygon points="110,90 120,90 125,110 105,110" fill="#3182CE" stroke="#FFFFFF" />
          <!-- Element Cards -->
          <rect x="50" y="125" width="20" height="28" fill="#FFFFFF" stroke="#1A202C" rx="2" />
          <text x="60" y="142" font-family="sans-serif" font-size="8" font-weight="bold" fill="#1A202C" text-anchor="middle">Au</text>
        </g>
        """
    elif sku == "QQ-0053":  # Mathematical Paradox Card Deck
        return """
        <g transform="translate(110, 100)">
          <!-- Fan of Playing Cards -->
          <g transform="rotate(-15, 60, 100)">
            <rect x="30" y="40" width="60" height="90" rx="4" fill="#FFFFFF" stroke="#1A202C" stroke-width="2" />
            <text x="40" y="58" font-family="serif" font-size="12" fill="#E53E3E">&#9829;</text>
          </g>
          <g transform="rotate(15, 120, 100)">
            <rect x="90" y="40" width="60" height="90" rx="4" fill="#FFFFFF" stroke="#1A202C" stroke-width="2" />
            <text x="140" y="58" font-family="serif" font-size="12" fill="#1A202C">&#9824;</text>
          </g>
          <!-- Center Card Showing Paradox -->
          <rect x="60" y="40" width="60" height="90" rx="4" fill="#18243A" stroke="#F4C95D" stroke-width="2" />
          <text x="90" y="80" font-family="serif" font-size="18" fill="#F4C95D" text-anchor="middle">&#8734;</text>
          <text x="90" y="105" font-family="sans-serif" font-size="7" fill="#FFFFFF" text-anchor="middle">ZENO</text>
        </g>
        """
    elif sku == "QQ-0054":  # Space-Time Escape Puzzle
        return """
        <g transform="translate(120, 100)">
          <!-- Two Intertwined Curved Cast Metal Rings -->
          <circle cx="65" cy="85" r="40" fill="none" stroke="#D69E2E" stroke-width="9" />
          <circle cx="95" cy="95" r="40" fill="none" stroke="#718096" stroke-width="9" />
          <!-- Interlocking key notch -->
          <rect x="75" y="75" width="10" height="20" fill="#ECC94B" rx="2" />
        </g>
        """
    elif sku == "QQ-0055":  # Scientific Deduction Board Game
        return """
        <g transform="translate(100, 110)">
          <!-- Mystery Screen / Lab Board -->
          <rect x="25" y="40" width="150" height="100" rx="4" fill="#1A202C" stroke="#2B6CB0" stroke-width="3" />
          <!-- Particle Collider Circular Track on Board -->
          <circle cx="75" cy="90" r="30" fill="none" stroke="#F4C95D" stroke-width="2.5" />
          <circle cx="75" cy="90" r="10" fill="#E53E3E" />
          <!-- Clue Notebook Cards -->
          <rect x="120" y="65" width="40" height="55" fill="#EDF2F7" stroke="#718096" rx="2" />
          <line x1="125" y1="75" x2="150" y2="75" stroke="#718096" stroke-width="1.5" />
          <line x1="125" y1="85" x2="150" y2="85" stroke="#718096" stroke-width="1.5" />
          <line x1="125" y1="95" x2="140" y2="95" stroke="#718096" stroke-width="1.5" />
        </g>
        """
    elif sku == "QQ-0056":  # Galactic Probability Dice Set
        return """
        <g transform="translate(110, 100)">
          <!-- D20 Icosahedron Die -->
          <polygon points="90,40 135,65 125,120 55,120 45,65" fill="#6B46C1" stroke="#D6BCFA" stroke-width="2" />
          <polygon points="90,40 90,95 125,120" fill="#805AD5" stroke="#D6BCFA" stroke-width="1.5" />
          <polygon points="90,40 90,95 55,120" fill="#553C9A" stroke="#D6BCFA" stroke-width="1.5" />
          <text x="90" y="80" font-family="sans-serif" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">20</text>
          <!-- Secondary D6 Die -->
          <rect x="120" y="110" width="35" height="35" rx="3" fill="#6B46C1" stroke="#D6BCFA" stroke-width="1.5" />
          <circle cx="137" cy="127" r="3" fill="#FFFFFF" />
        </g>
        """
    elif sku == "QQ-0057":  # Magnetic Maze Challenge
        return """
        <g transform="translate(110, 100)">
          <!-- Acrylic Square Labyrinth Base -->
          <rect x="25" y="30" width="130" height="130" rx="8" fill="#E6FFFA" stroke="#319795" stroke-width="4" />
          <!-- Maze Walls -->
          <path d="M 45 50 L 135 50 M 45 75 L 95 75 M 115 75 L 135 75 M 75 75 L 75 125 M 45 105 L 115 105 M 95 105 L 95 140" fill="none" stroke="#234E52" stroke-width="3" stroke-linecap="round" />
          <!-- Steel Bearing Ball -->
          <circle cx="55" cy="62" r="5" fill="#718096" stroke="#4A5568" />
          <!-- Magnetic Stylus Pen navigating ball -->
          <line x1="85" y1="20" x2="60" y2="55" stroke="#D69E2E" stroke-width="4" stroke-linecap="round" />
        </g>
        """
    elif sku == "QQ-0058":  # Advanced Geometry Puzzle Box
        return """
        <g transform="translate(100, 110)">
          <!-- Wooden Secret Box -->
          <polygon points="20,70 140,70 170,40 50,40" fill="#B7791F" stroke="#744210" stroke-width="2" />
          <rect x="20" y="70" width="120" height="70" fill="#744210" stroke="#4A2E18" stroke-width="2" />
          <polygon points="140,70 170,40 170,110 140,140" fill="#5E300B" />
          <!-- Inlaid Geometric Marquetry Tiles -->
          <polygon points="40,85 70,85 55,115" fill="#D69E2E" />
          <polygon points="80,125 110,125 95,95" fill="#ECC94B" />
        </g>
        """
    elif sku == "QQ-0059":  # Train Routing Strategy Game
        return """
        <g transform="translate(100, 110)">
          <!-- Hex Track Board Map -->
          <polygon points="90,30 150,65 150,135 90,170 30,135 30,65" fill="#C6F6D5" stroke="#22543D" stroke-width="3" />
          <!-- Railway Tracks across hex -->
          <path d="M 30 100 Q 90 70 150 100" fill="none" stroke="#276749" stroke-width="4" />
          <line x1="90" y1="30" x2="90" y2="170" stroke="#276749" stroke-width="4" />
          <!-- Wooden Train Car Piece -->
          <rect x="75" y="88" width="30" height="14" rx="2" fill="#E53E3E" stroke="#9B2C2C" stroke-width="1.5" />
        </g>
        """
    elif sku == "QQ-0060":  # Cosmic Constellation Jigsaw
        return """
        <g transform="translate(110, 100)">
          <!-- Circular Jigsaw Boundary -->
          <circle cx="90" cy="90" r="75" fill="#18243A" stroke="#2CD4CD" stroke-width="3" />
          <!-- Jigsaw Interlocking Cut Lines -->
          <path d="M 15 90 Q 50 100 65 90 Q 75 75 90 90 T 165 90" fill="none" stroke="#4A5568" stroke-width="1.5" />
          <path d="M 90 15 Q 100 50 90 65 Q 105 75 90 90 T 90 165" fill="none" stroke="#4A5568" stroke-width="1.5" />
          <!-- Glowing Constellation Stars -->
          <circle cx="60" cy="60" r="3" fill="#F4C95D" />
          <circle cx="120" cy="65" r="3" fill="#F4C95D" />
          <circle cx="80" cy="130" r="3.5" fill="#FFFFFF" />
          <line x1="60" y1="60" x2="120" y2="65" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="2,2" />
        </g>
        """

    # Category G: Stationery & Learning (QQ-0061 to QQ-0070)
    elif sku == "QQ-0061":  # Roommate Protocol Notebook
        return """
        <g transform="translate(115, 100)">
          <!-- Hardbound Leather Notebook -->
          <rect x="25" y="30" width="120" height="160" rx="4" fill="#18243A" stroke="#D69E2E" stroke-width="2.5" />
          <!-- Gilded Page Edge -->
          <rect x="142" y="34" width="6" height="152" fill="#F4C95D" />
          <!-- Gold Embossed Protocol Seal -->
          <circle cx="85" cy="85" r="25" fill="none" stroke="#F4C95D" stroke-width="1.8" />
          <text x="85" y="82" font-family="serif" font-size="10" font-weight="bold" fill="#F4C95D" text-anchor="middle">HOUSEHOLD</text>
          <text x="85" y="94" font-family="serif" font-size="9" fill="#F4C95D" text-anchor="middle">PROTOCOL</text>
          <!-- Bookmark Ribbon hanging out -->
          <path d="M 85 190 L 85 210 L 90 205 L 95 210 L 95 190" fill="#E53E3E" />
        </g>
        """
    elif sku == "QQ-0062":  # Scientific Hypothesis Journal
        return """
        <g transform="translate(115, 100)">
          <!-- Cloth Bound Journal -->
          <rect x="25" y="30" width="120" height="160" rx="4" fill="#234E52" stroke="#1D4044" stroke-width="2" />
          <!-- Spine Tape -->
          <rect x="25" y="30" width="18" height="160" fill="#1A365D" />
          <!-- Cover Title Box -->
          <rect x="55" y="65" width="75" height="40" fill="#F7FAFC" stroke="#A0AEC0" rx="2" />
          <text x="92" y="82" font-family="sans-serif" font-size="7" font-weight="bold" fill="#1A202C" text-anchor="middle">HYPOTHESIS</text>
          <text x="92" y="94" font-family="monospace" font-size="6" fill="#4A5568" text-anchor="middle">LOG: H&#8320; vs H&#8321;</text>
        </g>
        """
    elif sku == "QQ-0063":  # Mathematical Proof Sticky Notes
        return """
        <g transform="translate(110, 110)">
          <!-- Stack of Sticky Notes -->
          <rect x="35" y="45" width="100" height="100" rx="2" fill="#FEFCBF" stroke="#ECC94B" stroke-width="1.5" />
          <rect x="30" y="40" width="100" height="100" rx="2" fill="#FAF089" stroke="#ECC94B" stroke-width="1.5" />
          <!-- Top Note Page -->
          <rect x="25" y="35" width="100" height="100" rx="2" fill="#FFFFF0" stroke="#D69E2E" stroke-width="2" />
          <!-- Printed Lemma & QED -->
          <text x="40" y="60" font-family="serif" font-size="11" font-weight="bold" fill="#744210">LEMMA 3.14:</text>
          <line x1="40" y1="75" x2="110" y2="75" stroke="#CBD5E0" stroke-width="1" />
          <line x1="40" y1="90" x2="110" y2="90" stroke="#CBD5E0" stroke-width="1" />
          <!-- QED Tombstone Symbol -->
          <rect x="105" y="112" width="10" height="10" fill="#18243A" />
        </g>
        """
    elif sku == "QQ-0064":  # Train Timetable Precision Planner
        return """
        <g transform="translate(115, 100)">
          <!-- Hardcover Green Locomotive Planner -->
          <rect x="25" y="30" width="120" height="160" rx="4" fill="#1C4532" stroke="#D69E2E" stroke-width="2" />
          <!-- Locomotive Foil Badge -->
          <circle cx="85" cy="80" r="22" fill="#22543D" stroke="#D69E2E" stroke-width="1.5" />
          <text x="85" y="78" font-family="serif" font-size="8" font-weight="bold" fill="#F4C95D" text-anchor="middle">SCHEDULE</text>
          <text x="85" y="88" font-family="serif" font-size="7" fill="#F4C95D" text-anchor="middle">MANIFEST</text>
          <!-- Elastic Retention Band -->
          <rect x="125" y="30" width="8" height="160" fill="#1A202C" />
        </g>
        """
    elif sku == "QQ-0065":  # Quantum Field Sketchbook
        return """
        <g transform="translate(100, 110)">
          <!-- Square Open Spine Sketchbook -->
          <rect x="30" y="30" width="140" height="140" rx="2" fill="#D69E2E" stroke="#744210" stroke-width="2" />
          <!-- Exposed Swiss thread binding on spine -->
          <line x1="30" y1="45" x2="30" y2="55" stroke="#FFFFFF" stroke-width="3" />
          <line x1="30" y1="75" x2="30" y2="85" stroke="#FFFFFF" stroke-width="3" />
          <line x1="30" y1="105" x2="30" y2="115" stroke="#FFFFFF" stroke-width="3" />
          <line x1="30" y1="135" x2="30" y2="145" stroke="#FFFFFF" stroke-width="3" />
          <!-- Isometric Cube on Cover -->
          <polygon points="100,70 125,85 100,100 75,85" fill="none" stroke="#1A202C" stroke-width="1.5" />
          <polygon points="75,85 100,100 100,130 75,115" fill="none" stroke="#1A202C" stroke-width="1.5" />
          <polygon points="100,100 125,85 125,115 100,130" fill="none" stroke="#1A202C" stroke-width="1.5" />
        </g>
        """
    elif sku == "QQ-0066":  # Periodic Table Bookmark Collection
        return """
        <g transform="translate(100, 100)">
          <!-- Four Brass Bookmarks Fan -->
          <rect x="40" y="30" width="22" height="120" rx="3" fill="#D69E2E" stroke="#B7791F" stroke-width="1" />
          <text x="51" y="60" font-family="sans-serif" font-size="9" font-weight="bold" fill="#744210" text-anchor="middle">He</text>
          <rect x="70" y="30" width="22" height="120" rx="3" fill="#ECC94B" stroke="#B7791F" stroke-width="1" />
          <text x="81" y="60" font-family="sans-serif" font-size="9" font-weight="bold" fill="#744210" text-anchor="middle">Na</text>
          <rect x="100" y="30" width="22" height="120" rx="3" fill="#D69E2E" stroke="#B7791F" stroke-width="1" />
          <text x="111" y="60" font-family="sans-serif" font-size="9" font-weight="bold" fill="#744210" text-anchor="middle">Cl</text>
          <rect x="130" y="30" width="22" height="120" rx="3" fill="#ECC94B" stroke="#B7791F" stroke-width="1" />
          <text x="141" y="60" font-family="sans-serif" font-size="9" font-weight="bold" fill="#744210" text-anchor="middle">Pt</text>
        </g>
        """
    elif sku == "QQ-0067":  # Physics Formula Flashcards
        return """
        <g transform="translate(100, 100)">
          <!-- Rigid Card Slide Box -->
          <rect x="25" y="60" width="130" height="90" rx="4" fill="#2B6CB0" stroke="#1A365D" stroke-width="3" />
          <!-- Flashcards Spanning out -->
          <rect x="45" y="40" width="110" height="75" rx="3" fill="#FFFFFF" stroke="#CBD5E0" stroke-width="1.5" />
          <text x="100" y="68" font-family="'Courier New', monospace" font-size="12" font-weight="bold" fill="#18243A" text-anchor="middle">&#8711; &#8226; E = &#961;/&#949;&#8320;</text>
          <text x="100" y="90" font-family="sans-serif" font-size="7" fill="#718096" text-anchor="middle">Gauss's Law of Electromagnetism</text>
        </g>
        """
    elif sku == "QQ-0068":  # Researcher's Experiment Logbook
        return """
        <g transform="translate(115, 90)">
          <!-- Black Heavy Hardback Ledger -->
          <rect x="25" y="30" width="125" height="170" rx="3" fill="#1A202C" stroke="#718096" stroke-width="2.5" />
          <!-- Brass Title Plate -->
          <rect x="45" y="60" width="85" height="35" fill="#D69E2E" stroke="#B7791F" rx="2" />
          <text x="87" y="76" font-family="serif" font-size="8" font-weight="bold" fill="#1A202C" text-anchor="middle">LABORATORY</text>
          <text x="87" y="87" font-family="serif" font-size="7" fill="#1A202C" text-anchor="middle">OFFICIAL LOG</text>
          <!-- Grid peek on open side -->
          <line x1="148" y1="35" x2="148" y2="195" stroke="#CBD5E0" stroke-width="2" />
        </g>
        """
    elif sku == "QQ-0069":  # Galactic Graph Paper Notebook
        return """
        <g transform="translate(110, 100)">
          <!-- Spiral Bound Pad -->
          <rect x="35" y="30" width="120" height="160" rx="3" fill="#FFFFFF" stroke="#718096" stroke-width="2" />
          <!-- Cyan Millimeter Grid lines -->
          <path d="M 45 40 L 145 40 M 45 55 L 145 55 M 45 70 L 145 70 M 45 85 L 145 85 M 45 100 L 145 100 M 45 115 L 145 115 M 45 130 L 145 130 M 45 145 L 145 145 M 45 160 L 145 160 M 45 175 L 145 175" stroke="#2CD4CD" stroke-width="0.8" opacity="0.6" />
          <!-- Steel Wire-O Spiral -->
          <circle cx="35" cy="45" r="4" fill="none" stroke="#4A5568" stroke-width="2" />
          <circle cx="35" cy="75" r="4" fill="none" stroke="#4A5568" stroke-width="2" />
          <circle cx="35" cy="105" r="4" fill="none" stroke="#4A5568" stroke-width="2" />
          <circle cx="35" cy="135" r="4" fill="none" stroke="#4A5568" stroke-width="2" />
          <circle cx="35" cy="165" r="4" fill="none" stroke="#4A5568" stroke-width="2" />
        </g>
        """
    elif sku == "QQ-0070":  # Advanced Whiteboard Marker Set
        return """
        <g transform="translate(100, 110)">
          <!-- Four Markers Arrayed -->
          <rect x="30" y="40" width="22" height="120" rx="4" fill="#1A202C" stroke="#718096" />
          <rect x="30" y="40" width="22" height="30" fill="#E53E3E" rx="3" />
          <rect x="65" y="40" width="22" height="120" rx="4" fill="#1A202C" stroke="#718096" />
          <rect x="65" y="40" width="22" height="30" fill="#3182CE" rx="3" />
          <rect x="100" y="40" width="22" height="120" rx="4" fill="#1A202C" stroke="#718096" />
          <rect x="100" y="40" width="22" height="30" fill="#38A169" rx="3" />
          <rect x="135" y="40" width="22" height="120" rx="4" fill="#1A202C" stroke="#718096" />
          <rect x="135" y="40" width="22" height="30" fill="#18243A" rx="3" />
        </g>
        """

    # Category H: Tech Accessories (QQ-0071 to QQ-0080)
    elif sku == "QQ-0071":  # Quantum Circuit Laptop Sleeve
        return """
        <g transform="translate(100, 110)">
          <!-- Laptop Sleeve Shell -->
          <rect x="20" y="40" width="160" height="115" rx="10" fill="#18243A" stroke="#2B4C7E" stroke-width="3" />
          <!-- Gold Circuit Traces -->
          <path d="M 35 60 L 70 60 L 85 85 L 130 85" fill="none" stroke="#F4C95D" stroke-width="2" />
          <circle cx="130" cy="85" r="3" fill="#F4C95D" />
          <path d="M 35 120 L 60 120 L 75 95 L 140 95" fill="none" stroke="#2CD4CD" stroke-width="2" />
          <circle cx="140" cy="95" r="3" fill="#2CD4CD" />
          <!-- Corner bumper reinforcement -->
          <path d="M 20 55 L 20 40 L 35 40" fill="none" stroke="#F4C95D" stroke-width="3" />
          <path d="M 180 55 L 180 40 L 165 40" fill="none" stroke="#F4C95D" stroke-width="3" />
        </g>
        """
    elif sku == "QQ-0072":  # Galaxy Nebula Phone Case
        return """
        <g transform="translate(125, 90)">
          <!-- Smartphone Case Profile -->
          <rect x="30" y="30" width="90" height="175" rx="18" fill="#18243A" stroke="#2CD4CD" stroke-width="2.5" />
          <!-- Camera Island -->
          <rect x="40" y="40" width="32" height="36" rx="8" fill="#131D2E" stroke="#718096" />
          <circle cx="50" cy="50" r="4.5" fill="#2D3748" />
          <circle cx="62" cy="62" r="4.5" fill="#2D3748" />
          <!-- MagSafe Magnetic Ring -->
          <circle cx="75" cy="120" r="24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="8,4" opacity="0.8" />
          <line x1="75" y1="144" x2="75" y2="154" stroke="#FFFFFF" stroke-width="3" opacity="0.8" />
        </g>
        """
    elif sku == "QQ-0073":  # Molecular Pattern Mechanical Keyboard
        return """
        <g transform="translate(90, 120)">
          <!-- Slate Aluminum Keyboard Chassis -->
          <rect x="15" y="45" width="190" height="100" rx="8" fill="#2D3748" stroke="#1A202C" stroke-width="3" />
          <!-- Brass Rotary Encoder Knob -->
          <circle cx="188" cy="60" r="8" fill="#D69E2E" stroke="#B7791F" stroke-width="1.5" />
          <!-- Keycap Grid Matrix -->
          <g fill="#EDF2F7" stroke="#CBD5E0" rx="2">
            <rect x="25" y="55" width="12" height="12" />
            <rect x="40" y="55" width="12" height="12" />
            <rect x="55" y="55" width="12" height="12" />
            <rect x="70" y="55" width="12" height="12" />
            <rect x="85" y="55" width="12" height="12" />
            <rect x="100" y="55" width="12" height="12" />
            <rect x="115" y="55" width="12" height="12" fill="#2B6CB0" />
            <rect x="130" y="55" width="12" height="12" fill="#2B6CB0" />
            <!-- Row 2 -->
            <rect x="25" y="72" width="16" height="12" fill="#319795" />
            <rect x="45" y="72" width="12" height="12" />
            <rect x="60" y="72" width="12" height="12" />
            <rect x="75" y="72" width="12" height="12" />
            <rect x="90" y="72" width="12" height="12" />
            <rect x="105" y="72" width="12" height="12" />
            <!-- Spacebar Row -->
            <rect x="65" y="115" width="60" height="14" fill="#D69E2E" />
          </g>
        </g>
        """
    elif sku == "QQ-0074":  # Atomic Orbit Wireless Charger
        return """
        <g transform="translate(110, 110)">
          <!-- Circular Brass Charger Base -->
          <circle cx="90" cy="90" r="70" fill="#18243A" stroke="#D69E2E" stroke-width="5" />
          <!-- Center Qi2 Magnet Ring -->
          <circle cx="90" cy="90" r="28" fill="#131D2E" stroke="#2CD4CD" stroke-width="2" />
          <!-- Orbiting LED Rings -->
          <ellipse cx="90" cy="90" rx="55" ry="18" fill="none" stroke="#2CD4CD" stroke-width="2" transform="rotate(-30, 90, 90)" />
          <ellipse cx="90" cy="90" rx="55" ry="18" fill="none" stroke="#F4C95D" stroke-width="2" transform="rotate(30, 90, 90)" />
          <circle cx="90" cy="90" r="6" fill="#F4C95D" />
        </g>
        """
    elif sku == "QQ-0075":  # Precision Engineer USB-C Hub
        return """
        <g transform="translate(110, 120)">
          <!-- Aluminum Hub Body -->
          <rect x="30" y="50" width="120" height="70" rx="6" fill="#A0AEC0" stroke="#718096" stroke-width="2.5" />
          <!-- Braided USB-C Cable Lead -->
          <path d="M 30 85 L 5 85 L 5 40" fill="none" stroke="#2D3748" stroke-width="5" />
          <rect x="0" y="30" width="10" height="14" rx="2" fill="#CBD5E0" />
          <!-- Ports -->
          <rect x="150" y="60" width="5" height="18" fill="#1A202C" /> <!-- HDMI -->
          <rect x="50" y="120" width="16" height="5" fill="#3182CE" /> <!-- USB 1 -->
          <rect x="75" y="120" width="16" height="5" fill="#3182CE" /> <!-- USB 2 -->
          <rect x="100" y="120" width="16" height="5" fill="#3182CE" /> <!-- USB 3 -->
          <!-- Pinout line graphics -->
          <text x="90" y="75" font-family="monospace" font-size="7" fill="#2D3748" text-anchor="middle">USB-C PD 100W</text>
        </g>
        """
    elif sku == "QQ-0076":  # Scientific Notation Desk Mat
        return """
        <g transform="translate(80, 140)">
          <!-- Desk Mat Perspective -->
          <polygon points="10,130 230,130 210,30 30,30" fill="#2D3748" stroke="#4A5568" stroke-width="3" />
          <!-- SI Unit Tables Printed -->
          <text x="60" y="65" font-family="'Courier New', monospace" font-size="9" fill="#F4C95D">kg &#8226; m &#8226; s &#8226; A &#8226; K &#8226; mol</text>
          <text x="120" y="90" font-family="'Courier New', monospace" font-size="9" fill="#2CD4CD">c = 299,792,458 m/s</text>
          <text x="70" y="115" font-family="'Courier New', monospace" font-size="9" fill="#FFFFFF">&#8463; = 6.62607015&#215;10&#8315;&#179;&#8308;</text>
        </g>
        """
    elif sku == "QQ-0077":  # Orbital Geometry Earbud Case
        return """
        <g transform="translate(130, 110)">
          <!-- Earbuds Charging Case Body -->
          <rect x="30" y="45" width="80" height="90" rx="22" fill="#18243A" stroke="#2CD4CD" stroke-width="2" />
          <!-- Lid Split Line -->
          <line x1="30" y1="75" x2="110" y2="75" stroke="#718096" stroke-width="1.5" />
          <!-- LED Indicator -->
          <circle cx="70" cy="95" r="2.5" fill="#48BB78" />
          <!-- Orbital Geometric Resonance Star -->
          <polygon points="70,105 77,125 58,113 82,113 63,125" fill="none" stroke="#F4C95D" stroke-width="1.5" />
          <!-- Carabiner Clip -->
          <path d="M 110 90 Q 135 90 135 110 Q 135 130 110 130" fill="none" stroke="#718096" stroke-width="4" />
        </g>
        """
    elif sku == "QQ-0078":  # Cosmic Signal Bluetooth Speaker
        return """
        <g transform="translate(110, 110)">
          <!-- Cylindrical Speaker -->
          <rect x="25" y="45" width="130" height="85" rx="16" fill="#1A202C" stroke="#2D3748" stroke-width="3" />
          <!-- Front Pulsar Waveform Grille -->
          <path d="M 40 90 L 70 90 L 75 60 L 80 115 L 85 50 L 90 120 L 95 70 L 100 90 L 140 90" fill="none" stroke="#2CD4CD" stroke-width="2.5" stroke-linecap="round" />
          <!-- Passive Radiator Rings on ends -->
          <ellipse cx="25" cy="87" rx="6" ry="25" fill="#4A5568" />
          <ellipse cx="155" cy="87" rx="6" ry="25" fill="#4A5568" />
        </g>
        """
    elif sku == "QQ-0079":  # Magnetic Flux Phone Stand
        return """
        <g transform="translate(120, 90)">
          <!-- Base Plate -->
          <ellipse cx="80" cy="200" rx="50" ry="15" fill="#4A5568" stroke="#2D3748" stroke-width="2" />
          <!-- Dual Hinge Arm -->
          <line x1="80" y1="200" x2="80" y2="120" stroke="#718096" stroke-width="7" stroke-linecap="round" />
          <line x1="80" y1="120" x2="110" y2="70" stroke="#718096" stroke-width="6" stroke-linecap="round" />
          <!-- Magnetic Circular Head -->
          <circle cx="110" cy="70" r="28" fill="#18243A" stroke="#2CD4CD" stroke-width="2.5" />
          <circle cx="110" cy="70" r="18" fill="none" stroke="#F4C95D" stroke-width="2" stroke-dasharray="5,2" />
        </g>
        """
    elif sku == "QQ-0080":  # Astrophysics Cable Management Kit
        return """
        <g transform="translate(100, 110)">
          <!-- Braided Sleeving Tube -->
          <path d="M 30 60 Q 90 120 170 80" fill="none" stroke="#1A202C" stroke-width="18" stroke-linecap="round" />
          <path d="M 30 60 Q 90 120 170 80" fill="none" stroke="#4A5568" stroke-width="14" stroke-dasharray="4,2" />
          <!-- Color Coded Frequency Collars -->
          <circle cx="60" cy="75" r="7" fill="#805AD5" />
          <circle cx="95" cy="98" r="7" fill="#3182CE" />
          <circle cx="135" cy="92" r="7" fill="#E53E3E" />
          <!-- Conduit Zip Clip Tool -->
          <polygon points="150,50 170,40 180,65 160,75" fill="#D69E2E" />
        </g>
        """

    # Category I: Railway & Engineering (QQ-0081 to QQ-0090)
    elif sku == "QQ-0081":  # Vintage Locomotive Miniature Model
        return """
        <g transform="translate(80, 110)">
          <!-- Track Rail -->
          <line x1="10" y1="165" x2="230" y2="165" stroke="#718096" stroke-width="4" />
          <!-- Locomotive Boiler -->
          <rect x="40" y="70" width="120" height="50" rx="8" fill="#18243A" stroke="#2B4C7E" stroke-width="2" />
          <!-- Cab -->
          <rect x="140" y="45" width="45" height="75" rx="3" fill="#131D2E" stroke="#D69E2E" stroke-width="2" />
          <rect x="150" y="55" width="25" height="20" fill="#E2E8F0" />
          <!-- Smokestack & Cowcatcher -->
          <rect x="55" y="45" width="14" height="25" fill="#D69E2E" />
          <polygon points="20,150 40,110 40,150" fill="#1A202C" />
          <!-- Big Driving Wheels & Rods -->
          <circle cx="65" cy="140" r="20" fill="#18243A" stroke="#D69E2E" stroke-width="3" />
          <circle cx="105" cy="140" r="20" fill="#18243A" stroke="#D69E2E" stroke-width="3" />
          <circle cx="145" cy="140" r="20" fill="#18243A" stroke="#D69E2E" stroke-width="3" />
          <line x1="65" y1="140" x2="145" y2="140" stroke="#F4C95D" stroke-width="4" stroke-linecap="round" />
        </g>
        """
    elif sku == "QQ-0082":  # Railway Signal Desk Ornament
        return """
        <g transform="translate(130, 80)">
          <!-- Cast Iron Base -->
          <rect x="40" y="210" width="60" height="20" rx="3" fill="#1A202C" />
          <!-- Signal Mast -->
          <line x1="70" y1="210" x2="70" y2="40" stroke="#4A5568" stroke-width="5" />
          <!-- Semaphore Spectacle Arm -->
          <rect x="65" y="55" width="65" height="14" fill="#E53E3E" stroke="#FFFFFF" stroke-width="1.5" transform="rotate(-35, 70, 60)" />
          <rect x="90" y="55" width="12" height="14" fill="#FFFFFF" transform="rotate(-35, 70, 60)" />
          <!-- Illuminated Spectacle Lenses -->
          <circle cx="60" cy="55" r="5" fill="#48BB78" stroke="#1A202C" stroke-width="1.5" />
          <circle cx="60" cy="68" r="5" fill="#E53E3E" stroke="#1A202C" stroke-width="1.5" />
        </g>
        """
    elif sku == "QQ-0083":  # Precision Train Schedule Wall Chart
        return """
        <g transform="translate(100, 90)">
          <!-- Teak Hangers Top & Bottom -->
          <rect x="25" y="20" width="150" height="10" rx="2" fill="#744210" />
          <rect x="25" y="190" width="150" height="10" rx="2" fill="#744210" />
          <!-- Blue Schedule Paper -->
          <rect x="30" y="30" width="140" height="160" fill="#1A365D" />
          <!-- Marey String Timetable Velocity Lines -->
          <line x1="40" y1="45" x2="160" y2="175" stroke="#F4C95D" stroke-width="2" />
          <line x1="40" y1="90" x2="160" y2="140" stroke="#2CD4CD" stroke-width="2" />
          <line x1="160" y1="45" x2="40" y2="175" stroke="#FFFFFF" stroke-width="2" />
        </g>
        """
    elif sku == "QQ-0084":  # Magnetic Railway Track Puzzle
        return """
        <g transform="translate(110, 110)">
          <!-- Beechwood Tiles Grid -->
          <rect x="30" y="40" width="60" height="60" rx="4" fill="#ECC94B" stroke="#B7791F" stroke-width="2" />
          <path d="M 60 40 L 60 100" stroke="#4A2E18" stroke-width="5" />
          <rect x="90" y="40" width="60" height="60" rx="4" fill="#ECC94B" stroke="#B7791F" stroke-width="2" />
          <path d="M 90 70 Q 120 70 120 40" fill="none" stroke="#4A2E18" stroke-width="5" />
          <!-- Shunting Wagon Model -->
          <rect x="48" y="60" width="24" height="16" rx="2" fill="#E53E3E" stroke="#1A202C" />
        </g>
        """
    elif sku == "QQ-0085":  # Miniature Suspension Bridge Kit
        return """
        <g transform="translate(80, 110)">
          <!-- Towers -->
          <rect x="50" y="40" width="14" height="120" fill="#4A5568" stroke="#1A202C" />
          <rect x="175" y="40" width="14" height="120" fill="#4A5568" stroke="#1A202C" />
          <!-- Roadway Deck Truss -->
          <rect x="10" y="125" width="220" height="12" fill="#2D3748" stroke="#718096" />
          <!-- Catenary Cables -->
          <path d="M 10 90 Q 57 40 57 40 Q 120 120 182 40 Q 182 40 230 90" fill="none" stroke="#CBD5E0" stroke-width="3" />
          <!-- Vertical Suspenders -->
          <line x1="85" y1="88" x2="85" y2="125" stroke="#CBD5E0" stroke-width="1.2" />
          <line x1="120" y1="105" x2="120" y2="125" stroke="#CBD5E0" stroke-width="1.2" />
          <line x1="155" y1="88" x2="155" y2="125" stroke="#CBD5E0" stroke-width="1.2" />
        </g>
        """
    elif sku == "QQ-0086":  # Railway Engineering Blueprint Poster
        return """
        <g transform="translate(100, 90)">
          <!-- Cyanotype Blueprint Frame -->
          <rect x="20" y="25" width="160" height="135" fill="#1A365D" stroke="#CBD5E0" stroke-width="2" />
          <!-- Locomotive Cross-Section Profile -->
          <path d="M 40 100 L 140 100 L 155 70 L 125 70 L 125 60 L 60 60 L 40 80 Z" fill="none" stroke="#FFFFFF" stroke-width="2" />
          <!-- Firetubes Internal Hatching -->
          <line x1="65" y1="75" x2="120" y2="75" stroke="#2CD4CD" stroke-width="1.2" stroke-dasharray="3,2" />
          <line x1="65" y1="85" x2="120" y2="85" stroke="#2CD4CD" stroke-width="1.2" stroke-dasharray="3,2" />
          <!-- Engineering Title Block -->
          <rect x="110" y="130" width="65" height="25" fill="#18243A" stroke="#FFFFFF" stroke-width="1" />
          <text x="142" y="145" font-family="monospace" font-size="6" fill="#F4C95D" text-anchor="middle">4-6-2 BOILER</text>
        </g>
        """
    elif sku == "QQ-0087":  # Steam Engine Mechanics Model
        return """
        <g transform="translate(100, 100)">
          <!-- Wood Base Plinth -->
          <rect x="20" y="160" width="160" height="20" rx="3" fill="#4A2E18" stroke="#2D1A0E" />
          <!-- Transparent Cylinder Assembly -->
          <rect x="30" y="100" width="55" height="35" rx="3" fill="none" stroke="#2CD4CD" stroke-width="2" />
          <rect x="45" y="105" width="15" height="25" fill="#E2E8F0" stroke="#718096" /> <!-- Piston -->
          <!-- Piston Rod & Crosshead -->
          <line x1="60" y1="117" x2="115" y2="117" stroke="#718096" stroke-width="4" />
          <!-- Connecting Rod to Brass Flywheel -->
          <line x1="115" y1="117" x2="145" y2="95" stroke="#F4C95D" stroke-width="3" stroke-linecap="round" />
          <circle cx="145" cy="115" r="35" fill="none" stroke="#D69E2E" stroke-width="6" />
          <circle cx="145" cy="115" r="8" fill="#D69E2E" />
        </g>
        """
    elif sku == "QQ-0088":  # Railway Switch Demonstration Kit
        return """
        <g transform="translate(100, 110)">
          <!-- Switch Ties & Ground -->
          <rect x="20" y="60" width="160" height="90" fill="#EDF2F7" rx="4" />
          <!-- Main Stock Rails -->
          <line x1="30" y1="80" x2="170" y2="80" stroke="#718096" stroke-width="4" />
          <line x1="30" y1="130" x2="170" y2="130" stroke="#718096" stroke-width="4" />
          <!-- Diverging Route Rails -->
          <path d="M 60 80 Q 110 80 170 110" fill="none" stroke="#D69E2E" stroke-width="4" />
          <!-- Rotating Ground Lantern -->
          <rect x="35" y="100" width="14" height="14" rx="2" fill="#1A202C" />
          <circle cx="42" cy="107" r="4" fill="#48BB78" />
        </g>
        """
    elif sku == "QQ-0089":  # Model Train Display Platform
        return """
        <g transform="translate(100, 110)">
          <!-- Solid Oak Base -->
          <polygon points="10,140 190,140 170,110 30,110" fill="#B7791F" stroke="#744210" stroke-width="2" />
          <rect x="10" y="140" width="180" height="20" fill="#744210" />
          <!-- Ballast & Rails -->
          <rect x="35" y="112" width="130" height="8" fill="#4A5568" />
          <line x1="30" y1="112" x2="170" y2="112" stroke="#CBD5E0" stroke-width="2" />
          <line x1="30" y1="118" x2="170" y2="118" stroke="#CBD5E0" stroke-width="2" />
          <!-- Clear Acrylic Vitrine Glass Case Outline -->
          <polygon points="20,110 180,110 170,30 30,30" fill="none" stroke="#2CD4CD" stroke-width="2" stroke-dasharray="6,2" opacity="0.8" />
          <!-- Brass Dedication Plaque on front -->
          <rect x="80" y="145" width="40" height="10" fill="#F4C95D" rx="2" />
        </g>
        """
    elif sku == "QQ-0090":  # Mechanical Gear Assembly Kit
        return """
        <g transform="translate(100, 100)">
          <!-- Clear Acrylic Stand -->
          <rect x="25" y="30" width="150" height="140" rx="8" fill="#EDF2F7" stroke="#CBD5E0" stroke-width="2" />
          <!-- Interlocking Brass Spur Gears -->
          <circle cx="75" cy="80" r="30" fill="#D69E2E" stroke="#B7791F" stroke-width="3" stroke-dasharray="8,4" />
          <circle cx="75" cy="80" r="8" fill="#4A5568" />
          <circle cx="125" cy="95" r="22" fill="#ECC94B" stroke="#B7791F" stroke-width="3" stroke-dasharray="6,3" />
          <circle cx="125" cy="95" r="6" fill="#4A5568" />
          <!-- Bevel Gear pair on side -->
          <polygon points="75,130 95,130 90,145 80,145" fill="#D69E2E" />
          <!-- Hand crank -->
          <line x1="75" y1="80" x2="45" y2="60" stroke="#718096" stroke-width="4" stroke-linecap="round" />
          <circle cx="45" cy="60" r="5" fill="#E53E3E" />
        </g>
        """

    # Category J: Gifts & Collectibles (QQ-0091 to QQ-0100)
    elif sku == "QQ-0091":  # Limited Edition Cosmic Enamel Pin
        return """
        <g transform="translate(110, 100)">
          <!-- 24K Gold Plated Pin Rim -->
          <circle cx="90" cy="90" r="65" fill="#18243A" stroke="#D69E2E" stroke-width="6" />
          <!-- Black hole event horizon shadow -->
          <circle cx="90" cy="90" r="28" fill="#000000" />
          <!-- Relativistic Accretion Disc -->
          <ellipse cx="90" cy="90" rx="60" ry="16" fill="none" stroke="#ED8936" stroke-width="8" transform="rotate(-25, 90, 90)" />
          <ellipse cx="90" cy="90" rx="60" ry="16" fill="none" stroke="#F4C95D" stroke-width="3" transform="rotate(-25, 90, 90)" />
          <ellipse cx="90" cy="90" rx="40" ry="24" fill="none" stroke="#9F7AEA" stroke-width="4" transform="rotate(35, 90, 90)" />
        </g>
        """
    elif sku == "QQ-0092":  # Genius-Level Achievement Trophy
        return """
        <g transform="translate(120, 80)">
          <!-- Black Marquina Marble Plinth -->
          <rect x="40" y="180" width="80" height="45" rx="3" fill="#1A202C" stroke="#2D3748" stroke-width="2" />
          <!-- Gold Plaque on front -->
          <rect x="50" y="195" width="60" height="18" fill="#D69E2E" rx="2" />
          <text x="80" y="207" font-family="serif" font-size="7" font-weight="bold" fill="#1A202C" text-anchor="middle">PEER REVIEWED</text>
          <!-- Crystal Glass Atom Sphere -->
          <circle cx="80" cy="110" r="42" fill="#E6FFFA" stroke="#2CD4CD" stroke-width="2" opacity="0.8" />
          <!-- Laser Etched Atomic Orbitals inside crystal -->
          <ellipse cx="80" cy="110" rx="35" ry="12" fill="none" stroke="#D69E2E" stroke-width="2" transform="rotate(-30, 80, 110)" />
          <ellipse cx="80" cy="110" rx="35" ry="12" fill="none" stroke="#D69E2E" stroke-width="2" transform="rotate(30, 80, 110)" />
          <circle cx="80" cy="110" r="7" fill="#F4C95D" />
        </g>
        """
    elif sku == "QQ-0093":  # Atomic Element Keychain Set
        return """
        <g transform="translate(100, 100)">
          <!-- Gold Element Fob -->
          <g transform="translate(10, 30)">
            <rect x="10" y="30" width="38" height="50" rx="4" fill="#ECC94B" stroke="#B7791F" stroke-width="2" />
            <text x="29" y="58" font-family="sans-serif" font-size="16" font-weight="bold" fill="#744210" text-anchor="middle">Au</text>
            <circle cx="29" cy="20" r="7" fill="none" stroke="#A0AEC0" stroke-width="2" />
          </g>
          <!-- Titanium Element Fob -->
          <g transform="translate(65, 30)">
            <rect x="10" y="30" width="38" height="50" rx="4" fill="#A0AEC0" stroke="#4A5568" stroke-width="2" />
            <text x="29" y="58" font-family="sans-serif" font-size="16" font-weight="bold" fill="#1A202C" text-anchor="middle">Ti</text>
            <circle cx="29" cy="20" r="7" fill="none" stroke="#A0AEC0" stroke-width="2" />
          </g>
          <!-- Platinum Element Fob -->
          <g transform="translate(120, 30)">
            <rect x="10" y="30" width="38" height="50" rx="4" fill="#EDF2F7" stroke="#718096" stroke-width="2" />
            <text x="29" y="58" font-family="sans-serif" font-size="16" font-weight="bold" fill="#2B4C7E" text-anchor="middle">Pt</text>
            <circle cx="29" cy="20" r="7" fill="none" stroke="#A0AEC0" stroke-width="2" />
          </g>
        </g>
        """
    elif sku == "QQ-0094":  # Galactic Knowledge Gift Box
        return """
        <g transform="translate(100, 100)">
          <!-- Luxury Presentation Box -->
          <rect x="25" y="40" width="150" height="110" rx="6" fill="#18243A" stroke="#D69E2E" stroke-width="2.5" />
          <!-- Acrylic Meteorite Cube inside -->
          <rect x="45" y="70" width="40" height="40" fill="#E6FFFA" stroke="#2CD4CD" rx="2" />
          <polygon points="60,82 72,85 70,98 55,95" fill="#4A5568" />
          <!-- Brass Planisphere Coin -->
          <circle cx="125" cy="90" r="20" fill="#D69E2E" stroke="#B7791F" stroke-width="2" />
          <circle cx="125" cy="90" r="14" fill="#ECC94B" />
        </g>
        """
    elif sku == "QQ-0095":  # Miniature Scientist Figurine
        return """
        <g transform="translate(120, 80)">
          <!-- Hexagonal Slate Base -->
          <polygon points="50,225 110,225 130,205 90,205 30,205" fill="#4A5568" stroke="#1A202C" />
          <!-- Professor Silhouette -->
          <!-- Slacks and Shoes -->
          <rect x="65" y="150" width="12" height="60" fill="#18243A" />
          <rect x="85" y="150" width="12" height="60" fill="#18243A" />
          <!-- Tweed Jacket -->
          <rect x="58" y="90" width="46" height="65" rx="4" fill="#744210" stroke="#5E300B" />
          <!-- Head with Glasses and Wild Hair -->
          <circle cx="80" cy="70" r="16" fill="#FEEBC8" />
          <!-- Wild Chalk Dusted Hair -->
          <circle cx="68" cy="62" r="8" fill="#E2E8F0" />
          <circle cx="80" cy="54" r="8" fill="#E2E8F0" />
          <circle cx="92" cy="62" r="8" fill="#E2E8F0" />
          <!-- Round Glasses -->
          <circle cx="75" cy="70" r="4.5" fill="none" stroke="#D69E2E" stroke-width="1.5" />
          <circle cx="85" cy="70" r="4.5" fill="none" stroke="#D69E2E" stroke-width="1.5" />
          <!-- Arm holding piece of chalk up -->
          <line x1="104" y1="100" x2="125" y2="70" stroke="#744210" stroke-width="6" stroke-linecap="round" />
          <rect x="123" y="66" width="6" height="4" fill="#FFFFFF" />
        </g>
        """
    elif sku == "QQ-0096":  # Mathematical Constants Collectible Coins
        return """
        <g transform="translate(100, 100)">
          <!-- Four Proof Coins Display -->
          <circle cx="55" cy="65" r="28" fill="#D69E2E" stroke="#B7791F" stroke-width="3" />
          <text x="55" y="73" font-family="serif" font-size="20" font-weight="bold" fill="#744210" text-anchor="middle">&#960;</text>
          <circle cx="125" cy="65" r="28" fill="#C05621" stroke="#9C4221" stroke-width="3" />
          <text x="125" y="73" font-family="serif" font-size="20" font-weight="bold" fill="#FFFFFF" text-anchor="middle">e</text>
          <circle cx="55" cy="135" r="28" fill="#CBD5E0" stroke="#718096" stroke-width="3" />
          <text x="55" y="143" font-family="serif" font-size="20" font-weight="bold" fill="#2D3748" text-anchor="middle">&#981;</text>
          <circle cx="125" cy="135" r="28" fill="#ECC94B" stroke="#B7791F" stroke-width="3" />
          <text x="125" y="141" font-family="serif" font-size="12" font-weight="bold" fill="#1A202C" text-anchor="middle">e^(i&#960;)+1</text>
        </g>
        """
    elif sku == "QQ-0097":  # Science Humor Fridge Magnet Set
        return """
        <g transform="translate(100, 100)">
          <!-- Three Fun Magnets -->
          <rect x="25" y="40" width="85" height="40" rx="4" fill="#ECC94B" stroke="#B7791F" stroke-width="2" />
          <text x="67" y="58" font-family="sans-serif" font-size="7" font-weight="bold" fill="#1A202C" text-anchor="middle">CAUTION: ENTROPY</text>
          <text x="67" y="70" font-family="sans-serif" font-size="6" fill="#1A202C" text-anchor="middle">IS NON-DECREASING</text>

          <rect x="80" y="90" width="90" height="40" rx="4" fill="#319795" stroke="#234E52" stroke-width="2" />
          <text x="125" y="108" font-family="sans-serif" font-size="7" font-weight="bold" fill="#FFFFFF" text-anchor="middle">WARNING: OBSERVER</text>
          <text x="125" y="120" font-family="sans-serif" font-size="6" fill="#FFFFFF" text-anchor="middle">COLLAPSES SNACKS</text>
        </g>
        """
    elif sku == "QQ-0098":  # Theoretical Physics Gift Hamper
        return """
        <g transform="translate(100, 100)">
          <!-- Laser Engraved Wooden Crate -->
          <rect x="20" y="60" width="160" height="90" rx="4" fill="#ECC94B" stroke="#B7791F" stroke-width="3" />
          <!-- Wooden Slats -->
          <line x1="20" y1="90" x2="180" y2="90" stroke="#B7791F" stroke-width="2" />
          <line x1="20" y1="120" x2="180" y2="120" stroke="#B7791F" stroke-width="2" />
          <!-- Items peeking out of crate -->
          <circle cx="65" cy="50" r="18" fill="#18243A" /> <!-- Mug -->
          <rect x="95" y="35" width="25" height="35" fill="#3182CE" rx="2" /> <!-- Card Deck -->
          <circle cx="140" cy="50" r="10" fill="#D69E2E" /> <!-- Pin -->
        </g>
        """
    elif sku == "QQ-0099":  # Cosmic Curiosity Mystery Box
        return """
        <g transform="translate(100, 100)">
          <!-- Sealed Kraft Cardboard Box -->
          <polygon points="30,80 150,55 170,120 50,150" fill="#D69E2E" stroke="#744210" stroke-width="2.5" />
          <polygon points="30,80 150,55 120,35 15,55" fill="#ECC94B" stroke="#744210" />
          <!-- Tamper Evident Caution Tape -->
          <polygon points="20,105 160,78 162,94 22,120" fill="#E53E3E" opacity="0.9" />
          <text x="85" y="103" font-family="monospace" font-size="7" font-weight="bold" fill="#FFFFFF" transform="rotate(-10, 85, 103)">SUPERPOSITION SEAL</text>
          <text x="95" y="125" font-family="serif" font-size="28" font-weight="bold" fill="#18243A">?</text>
        </g>
        """
    elif sku == "QQ-0100":  # Precision Enthusiast Collector's Edition Set
        return """
        <g transform="translate(100, 90)">
          <!-- Fitted Walnut Hardwood Instrument Chest -->
          <polygon points="20,60 160,35 180,135 40,165" fill="#4A2E18" stroke="#2D1A0E" stroke-width="3" />
          <rect x="40" y="65" width="130" height="90" fill="#1A202C" rx="3" />
          <!-- Fitted Stainless Digital Caliper in foam -->
          <line x1="55" y1="120" x2="145" y2="85" stroke="#CBD5E0" stroke-width="5" stroke-linecap="round" />
          <rect x="85" y="96" width="22" height="15" fill="#4A5568" rx="2" />
          <!-- Micrometer Anvil -->
          <circle cx="70" cy="140" r="12" fill="none" stroke="#D69E2E" stroke-width="3" />
          <!-- Optical Flat Glass Disc -->
          <circle cx="140" cy="115" r="14" fill="#E6FFFA" stroke="#2CD4CD" stroke-width="2" />
        </g>
        """

    # Fallback generic (should not be reached)
    return """
    <circle cx="200" cy="200" r="80" fill="#18243A" stroke="#158D89" stroke-width="4" />
    <text x="200" y="208" font-family="sans-serif" font-size="22" fill="#FFFFFF" text-anchor="middle">Q &amp; Q</text>
    """

def generate_product_svg(product, is_thumb=False):
    sku = product["sku"]
    name = html.escape(product["name"])
    category_id = product["categoryId"]
    theme = CATEGORY_THEMES.get(category_id, {"bg": "#F7FAFC", "accent": "#18243A", "highlight": "#158D89", "tag": "General"})
    tag = theme["tag"]
    if "&" in tag and "&amp;" not in tag:
        tag = tag.replace("&", "&amp;")

    width = 160 if is_thumb else 400
    height = 160 if is_thumb else 400
    id_suffix = "_thumb" if is_thumb else ""
    drawing_markup = get_product_drawing(sku)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="{width}" height="{height}">
  <defs>
    <linearGradient id="bgGrad_{sku}{id_suffix}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{theme['bg']}" />
      <stop offset="100%" stop-color="#FFFFFF" />
    </linearGradient>
    <filter id="shadow_{sku}{id_suffix}" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#18243A" flood-opacity="0.08" />
    </filter>
  </defs>

  <!-- Clean Subtle Background -->
  <rect width="400" height="400" fill="url(#bgGrad_{sku}{id_suffix})" />
  
  <!-- Subtle Technical Grid Lines -->
  <g opacity="0.15" stroke="{theme['accent']}" stroke-width="0.8">
    <line x1="40" y1="0" x2="40" y2="400" stroke-dasharray="4,4" />
    <line x1="360" y1="0" x2="360" y2="400" stroke-dasharray="4,4" />
    <line x1="0" y1="40" x2="400" y2="40" stroke-dasharray="4,4" />
    <line x1="0" y1="360" x2="400" y2="360" stroke-dasharray="4,4" />
  </g>

  <!-- Category & SKU Header Tag -->
  <g transform="translate(25, 25)">
    <rect x="0" y="0" width="75" height="22" rx="4" fill="{theme['accent']}" />
    <text x="37.5" y="15" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">{sku}</text>
    
    <text x="85" y="15" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="{theme['highlight']}">{tag}</text>
  </g>

  <!-- Circular Pedestal Ground Shadow -->
  <ellipse cx="200" cy="315" rx="120" ry="22" fill="#E2E8F0" opacity="0.6" filter="url(#shadow_{sku}{id_suffix})" />

  <!-- Distinct Centered Product Vector Illustration -->
  <g id="product-art">
    {drawing_markup}
  </g>

  <!-- Product Title Label at Bottom -->
  <g transform="translate(200, 368)">
    <text x="0" y="0" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700" fill="{theme['accent']}" text-anchor="middle">
      {name}
    </text>
    <text x="0" y="16" font-family="monospace" font-size="9.5" fill="#718096" text-anchor="middle">
      Quirk &amp; Quanta &#8226; Certified Fictional
    </text>
  </g>
</svg>"""
    return svg

def main():
    print("==================================================")
    print("QUIRK & QUANTA: Generating Vector Image Assets")
    print("==================================================")

    generate_logo()
    generate_hero()

    print(f"Generating 100 primary images and 100 thumbnail SVGs for {len(CANONICAL_PRODUCTS)} products...")
    for idx, p in enumerate(CANONICAL_PRODUCTS, start=1):
        sku = p["sku"]

        # Primary
        primary_svg = generate_product_svg(p, is_thumb=False)
        primary_path = os.path.join(PRODUCTS_DIR, f"{sku}.svg")
        with open(primary_path, "w", encoding="utf-8") as f:
            f.write(primary_svg)

        # Thumbnail
        thumb_svg = generate_product_svg(p, is_thumb=True)
        thumb_path = os.path.join(PRODUCTS_DIR, f"{sku}-thumb.svg")
        with open(thumb_path, "w", encoding="utf-8") as f:
            f.write(thumb_svg)

        if idx % 20 == 0 or idx == 100:
            print(f"Generated {idx}/100 products (up to {sku})")

    print("\nAsset generation completed successfully!")
    print(f"Total product image files: 200 (100 primary + 100 thumbnails)")

if __name__ == "__main__":
    main()
