/**
 * Quirk & Quanta - Product Detail Controller
 * Validates SKU query parameter, fetches public data, renders specifications,
 * related/compatible products, bundle calculators, and customer reviews.
 */

let currentProduct = null;
let allCatalog = [];
let currentQuantity = 1;

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('product-detail-container')) {
    initProductDetail();
  }
});

async function initProductDetail() {
  const params = new URLSearchParams(window.location.search);
  const sku = params.get('sku');

  if (!sku) {
    renderNotFound("No SKU parameter provided in URL.");
    return;
  }

  try {
    const res = await fetch('data/products.public.json');
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    allCatalog = await res.json();
    window.AppState.products = allCatalog;

    currentProduct = allCatalog.find(p => p.sku.toUpperCase() === sku.toUpperCase());

    if (!currentProduct) {
      renderNotFound(`Product with SKU "${escapeHtml(sku)}" was not found in our catalog.`);
      return;
    }

    renderProductContent(currentProduct);
    setupDetailInteractions();
  } catch (err) {
    console.error('Failed to load product details:', err);
    renderNotFound('Error loading catalog data. Ensure the site is running through an HTTP server.');
  }
}

// Render 404 Not Found State
function renderNotFound(message) {
  const container = document.getElementById('product-detail-container');
  if (!container) return;

  container.innerHTML = `
    <div class="empty-state" style="padding: 64px 24px; max-width: 600px; margin: 40px auto;">
      <div class="empty-state-icon">🪐</div>
      <h2 class="empty-state-title">Product Beyond Observable Horizon</h2>
      <p class="empty-state-desc">${message}</p>
      <div style="display: flex; gap: 12px; justify-content: center; margin-top: 24px;">
        <button class="btn btn-outline" onclick="window.history.back()">Go Back</button>
        <a href="products.html" class="btn btn-primary">Browse All 100 Products</a>
      </div>
    </div>
  `;
}

// Render Valid Product Detail Page
function renderProductContent(p) {
  document.title = `${p.name} | Quirk & Quanta`;

  // Breadcrumbs
  const breadcrumbsEl = document.getElementById('detail-breadcrumbs');
  if (breadcrumbsEl) {
    breadcrumbsEl.innerHTML = `
      <a href="index.html">Home</a>
      <span class="breadcrumbs-sep">/</span>
      <a href="products.html">Catalog</a>
      <span class="breadcrumbs-sep">/</span>
      <a href="products.html?category=${encodeURIComponent(p.categoryId)}">${p.category}</a>
      <span class="breadcrumbs-sep">/</span>
      <span>${p.name}</span>
    `;
  }

  // Gallery
  const galleryEl = document.getElementById('detail-gallery');
  if (galleryEl) {
    galleryEl.innerHTML = `
      <div class="product-gallery-main">
        <span class="badge badge-teal product-card-badge">${p.category}</span>
        <img src="${p.public.images.primary}" alt="${escapeHtml(p.public.images.alt || p.name)}" id="detail-main-img">
      </div>
      <div style="text-align: center; font-size: 0.75rem; color: var(--color-text-light);">
        Interactive Vector Rendering &#8226; Certified Fictional Specification
      </div>
    `;
  }

  // Info Panel
  const infoEl = document.getElementById('detail-info');
  if (infoEl) {
    const isWishlisted = window.AppState.wishlist.includes(p.sku);
    const discountPercent = p.public.listPrice > p.public.sellingPrice
      ? Math.round(((p.public.listPrice - p.public.sellingPrice) / p.public.listPrice) * 100)
      : 0;

    let featuresHtml = '';
    (p.public.features || []).forEach(f => {
      featuresHtml += `<li><span class="feature-check">&#10003;</span> <span>${escapeHtml(f)}</span></li>`;
    });

    infoEl.innerHTML = `
      <div class="product-detail-sku-row">
        <span>SKU: <strong>${p.sku}</strong></span>
        <span>&#8226;</span>
        <span>Collection: <a href="products.html?category=${encodeURIComponent(p.categoryId)}" style="color: var(--color-teal); text-decoration: underline;">${p.collection}</a></span>
      </div>

      <h1 class="product-detail-title">${p.name}</h1>

      <div style="display: flex; align-items: center; gap: 12px;">
        <span class="rating-stars">★★★★★</span>
        <span class="rating-score">${p.public.rating.toFixed(1)} / 5.0</span>
        <a href="#reviews-section" style="font-size: 0.8125rem; color: var(--color-teal); text-decoration: underline;">(${p.public.reviewCount} customer reviews)</a>
      </div>

      <div class="product-detail-price-box">
        <span class="price-large">₹${p.public.sellingPrice.toLocaleString('en-IN')}</span>
        ${p.public.listPrice > p.public.sellingPrice ? `
          <span class="price-list-large">₹${p.public.listPrice.toLocaleString('en-IN')}</span>
          <span class="badge badge-success">Save ₹${(p.public.listPrice - p.public.sellingPrice).toLocaleString('en-IN')} (${discountPercent}%)</span>
        ` : ''}
        <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; margin-top: 8px;">
          <span class="stock-indicator ${p.public.stockStatus === 'in_stock' ? 'stock-in' : 'stock-low'}">
            <span class="stock-dot"></span>
            ${p.public.stockStatus === 'in_stock' ? `In Stock (${p.public.inventoryCount} calibrated units)` : 'Low Stock'}
          </span>
          <span style="font-size: 0.75rem; color: var(--color-text-muted);">
            Estimated transit: ${p.public.shippingDays.minimum}-${p.public.shippingDays.maximum} days
          </span>
        </div>
      </div>

      <p style="font-size: 1rem; color: var(--color-text-main); line-height: 1.6;">
        ${p.public.shortDescription}
      </p>

      <ul class="product-detail-features">
        ${featuresHtml}
      </ul>

      <div class="product-order-controls">
        <div class="quantity-stepper">
          <button class="qty-btn" id="qty-decrement-btn">-</button>
          <span class="qty-input" id="qty-display-val">1</span>
          <button class="qty-btn" id="qty-increment-btn">+</button>
        </div>

        <button class="btn btn-primary btn-lg" id="detail-add-cart-btn" style="flex: 1; min-width: 180px;">
          Add to Cart
        </button>

        <button class="btn btn-outline btn-lg ${isWishlisted ? 'active' : ''}" id="detail-wishlist-btn" title="Add to Wishlist">
          ${isWishlisted ? '♥ Saved' : '♡ Wishlist'}
        </button>
      </div>

      <!-- Educational Storefront Notice -->
      <div style="background-color: var(--color-bg); border-left: 3px solid var(--color-teal); padding: 10px 14px; border-radius: 4px; font-size: 0.75rem; color: var(--color-text-muted); margin-top: 8px;">
        🎓 <strong>Educational Notice:</strong> Quirk & Quanta is a fictional storefront constructed for Advanced RAG, Embeddings, and Graph Retrieval demonstrations. No products are available for purchase.
      </div>
    `;
  }

  // Tabs: Full Description, Specifications, and Policies
  renderTabs(p);

  // Bundle Component (Frequently Bought Together)
  renderBundleSection(p);

  // Related & Compatible Products
  renderRelatedSection(p);

  // Customer Reviews
  renderReviewsSection(p);
}

// Setup Interactive Stepper and Action Buttons
function setupDetailInteractions() {
  currentQuantity = 1;

  const decBtn = document.getElementById('qty-decrement-btn');
  const incBtn = document.getElementById('qty-increment-btn');
  const qtyDisplay = document.getElementById('qty-display-val');
  const addCartBtn = document.getElementById('detail-add-cart-btn');
  const wishlistBtn = document.getElementById('detail-wishlist-btn');

  if (decBtn && qtyDisplay) {
    decBtn.addEventListener('click', () => {
      if (currentQuantity > 1) {
        currentQuantity--;
        qtyDisplay.textContent = currentQuantity;
      }
    });
  }

  if (incBtn && qtyDisplay) {
    incBtn.addEventListener('click', () => {
      if (currentQuantity < 10) {
        currentQuantity++;
        qtyDisplay.textContent = currentQuantity;
      }
    });
  }

  if (addCartBtn) {
    addCartBtn.addEventListener('click', () => {
      if (currentProduct) {
        window.addToCart(currentProduct, currentQuantity);
      }
    });
  }

  if (wishlistBtn) {
    wishlistBtn.addEventListener('click', () => {
      if (currentProduct) {
        window.toggleWishlist(currentProduct.sku, currentProduct.name);
        const isWishlisted = window.AppState.wishlist.includes(currentProduct.sku);
        wishlistBtn.innerHTML = isWishlisted ? '♥ Saved' : '♡ Wishlist';
        wishlistBtn.classList.toggle('active', isWishlisted);
      }
    });
  }

  // Setup tab switching
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabTarget = btn.getAttribute('data-tab');
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const targetPane = document.getElementById(tabTarget);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

// Render Tabs & Specifications Table
function renderTabs(p) {
  // Long Description Pane
  const descPane = document.getElementById('tab-description');
  if (descPane) {
    descPane.innerHTML = `
      <div style="max-width: 800px; line-height: 1.8; color: var(--color-text-main); font-size: 0.9375rem;">
        <h3 style="font-size: 1.125rem; font-weight: 800; color: var(--color-navy); margin-bottom: 12px;">Theoretical Product Brief</h3>
        <p>${p.public.longDescription}</p>
        <div style="margin-top: 24px; padding: 16px; background-color: var(--color-bg); border-radius: 8px;">
          <h4 style="font-size: 0.875rem; font-weight: 700; color: var(--color-navy); margin-bottom: 8px;">Key Technical Features</h4>
          <ul style="padding-left: 20px; line-height: 1.6; font-size: 0.8125rem;">
            ${(p.public.features || []).map(f => `<li>${escapeHtml(f)}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
  }

  // Specifications Table Pane
  const specsPane = document.getElementById('tab-specs');
  if (specsPane) {
    let rowsHtml = '';
    const attrs = p.public.attributes || {};
    
    // Core attributes
    for (const [key, val] of Object.entries(attrs)) {
      const formattedKey = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
      const formattedVal = Array.isArray(val) ? val.join(', ') : val;
      rowsHtml += `
        <tr>
          <th>${escapeHtml(formattedKey)}</th>
          <td>${escapeHtml(String(formattedVal))}</td>
        </tr>
      `;
    }

    // Standard metadata rows
    rowsHtml += `
      <tr><th>Stock Keeping Unit (SKU)</th><td><code>${p.sku}</code></td></tr>
      <tr><th>Category / Subcategory</th><td>${p.category} &rsaquo; ${p.subcategory}</td></tr>
      <tr><th>Curated Collection</th><td>${p.collection}</td></tr>
      <tr><th>Warranty Period</th><td>${p.public.warrantyMonths > 0 ? `${p.public.warrantyMonths} Months Hardware Warranty` : 'Standard 30-Day Defect Guarantee'}</td></tr>
      <tr><th>Shipping Calibration</th><td>${p.public.shippingDays.minimum} to ${p.public.shippingDays.maximum} Business Days (Ground Velocity)</td></tr>
      <tr><th>Return Window</th><td>${p.public.returnWindowDays} Calendar Days</td></tr>
    `;

    specsPane.innerHTML = `
      <table class="specs-table">
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
    `;
  }

  // Policies Pane
  const policiesPane = document.getElementById('tab-policies');
  if (policiesPane) {
    policiesPane.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 20px; max-width: 800px;">
        <div style="background-color: var(--color-bg); padding: 18px; border-radius: 8px; border: 1px solid var(--color-border);">
          <h4 style="font-size: 1rem; font-weight: 700; color: var(--color-navy); margin-bottom: 6px;">Return &amp; Exchange Policy</h4>
          <p style="font-size: 0.875rem; color: var(--color-text-main); line-height: 1.5;">
            This product is covered by our <strong>${p.public.returnWindowDays}-Day Return Protocol</strong>. Returns are accepted within ${p.public.returnWindowDays} calendar days provided original packaging and atomic integrity are uncompromised.
          </p>
        </div>

        <div style="background-color: var(--color-bg); padding: 18px; border-radius: 8px; border: 1px solid var(--color-border);">
          <h4 style="font-size: 1rem; font-weight: 700; color: var(--color-navy); margin-bottom: 6px;">Warranty Coverage</h4>
          <p style="font-size: 0.875rem; color: var(--color-text-main); line-height: 1.5;">
            ${p.public.warrantyMonths > 0 
              ? `Includes <strong>${p.public.warrantyMonths} Months Manufacturer Integrity Warranty</strong> protecting against mechanical fatigue, bearing friction, and sensor calibration deviation.`
              : `Standard 30-day initial operational verification warranty applies.`}
          </p>
        </div>

        <div style="background-color: var(--color-bg); padding: 18px; border-radius: 8px; border: 1px solid var(--color-border);">
          <h4 style="font-size: 1rem; font-weight: 700; color: var(--color-navy); margin-bottom: 6px;">Shipping &amp; Logistics</h4>
          <p style="font-size: 0.875rem; color: var(--color-text-main); line-height: 1.5;">
            Dispatched via Standard Ground Velocity Logistics with calculated delivery within <strong>${p.public.shippingDays.minimum} to ${p.public.shippingDays.maximum} business days</strong> across all Indian postal zones.
          </p>
        </div>
      </div>
    `;
  }
}

// Render "Frequently Bought Together" Bundle
function renderBundleSection(p) {
  const bundleContainer = document.getElementById('bundle-section-container');
  if (!bundleContainer) return;

  const bundleSkus = p.relationships?.bundleWith || [];
  if (bundleSkus.length === 0) {
    bundleContainer.style.display = 'none';
    return;
  }

  const bundleProducts = allCatalog.filter(item => bundleSkus.includes(item.sku));
  if (bundleProducts.length === 0) {
    bundleContainer.style.display = 'none';
    return;
  }

  const allBundleItems = [p, ...bundleProducts];
  const bundleTotal = allBundleItems.reduce((sum, item) => sum + item.public.sellingPrice, 0);

  let itemsHtml = `
    <div class="bundle-item-card">
      <img src="${p.public.images.thumbnail}" alt="${p.name}" class="bundle-item-thumb">
      <div>
        <div style="font-size: 0.8125rem; font-weight: 700; color: var(--color-navy);">${p.name} (This item)</div>
        <div style="font-size: 0.75rem; color: var(--color-teal); font-weight: 800;">₹${p.public.sellingPrice.toLocaleString('en-IN')}</div>
      </div>
    </div>
  `;

  bundleProducts.forEach(bp => {
    itemsHtml += `
      <span class="bundle-plus-icon">+</span>
      <div class="bundle-item-card">
        <a href="product.html?sku=${bp.sku}">
          <img src="${bp.public.images.thumbnail}" alt="${bp.name}" class="bundle-item-thumb">
        </a>
        <div>
          <a href="product.html?sku=${bp.sku}" style="font-size: 0.8125rem; font-weight: 700; color: var(--color-navy);">${bp.name}</a>
          <div style="font-size: 0.75rem; color: var(--color-teal); font-weight: 800;">₹${bp.public.sellingPrice.toLocaleString('en-IN')}</div>
        </div>
      </div>
    `;
  });

  bundleContainer.style.display = 'block';
  bundleContainer.innerHTML = `
    <div class="bundle-box">
      <h3 class="bundle-title">Frequently Synergized Together</h3>
      <p style="font-size: 0.8125rem; color: var(--color-text-muted); margin-bottom: 16px;">
        Complementary apparatus frequently acquired simultaneously for laboratory and domestic coherence.
      </p>
      
      <div class="bundle-items-row">
        ${itemsHtml}
      </div>

      <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px; border-top: 1px solid var(--color-border); padding-top: 16px;">
        <div>
          <span style="font-size: 0.875rem; color: var(--color-text-muted);">Combined Bundle Price:</span>
          <span style="font-size: 1.5rem; font-weight: 900; color: var(--color-navy); margin-left: 8px;">₹${bundleTotal.toLocaleString('en-IN')}</span>
        </div>
        <button class="btn btn-primary" id="add-bundle-btn" onclick="addEntireBundle(['${allBundleItems.map(i => i.sku).join("','")}'])">
          Add All ${allBundleItems.length} to Cart
        </button>
      </div>
    </div>
  `;
}

function addEntireBundle(skus) {
  let count = 0;
  skus.forEach(sku => {
    const prod = allCatalog.find(item => item.sku === sku);
    if (prod) {
      window.AppState.cart.push({
        sku: prod.sku,
        name: prod.name,
        sellingPrice: prod.public.sellingPrice,
        thumbnail: prod.public.images.thumbnail,
        category: prod.category,
        quantity: 1
      });
      count++;
    }
  });

  window.saveCart();
  window.showToast(`Added ${count} items from bundle to cart!`);
  window.openCartDrawer();
}

// Render Related & Compatible Products
function renderRelatedSection(p) {
  const relatedContainer = document.getElementById('related-products-container');
  if (!relatedContainer) return;

  const relatedSkus = p.relationships?.relatedProducts || [];
  const compatibleSkus = p.relationships?.compatibleWith || [];
  const combinedSkus = Array.from(new Set([...compatibleSkus, ...relatedSkus])).slice(0, 4);

  const relatedItems = allCatalog.filter(item => combinedSkus.includes(item.sku));
  if (relatedItems.length === 0) {
    relatedContainer.style.display = 'none';
    return;
  }

  let cardsHtml = '';
  relatedItems.forEach(item => {
    cardsHtml += `
      <div class="product-card">
        <div class="product-card-thumb-wrapper">
          <span class="badge badge-navy product-card-badge">${item.category}</span>
          <a href="product.html?sku=${item.sku}" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <img src="${item.public.images.thumbnail}" alt="${item.name}" class="product-card-thumb" loading="lazy">
          </a>
        </div>
        <div class="product-card-body">
          <div class="product-card-meta">
            <span>${item.sku}</span>
            <span class="rating-score">★ ${item.public.rating.toFixed(1)}</span>
          </div>
          <h4 class="product-card-title"><a href="product.html?sku=${item.sku}">${item.name}</a></h4>
          <div class="product-card-price-row">
            <span class="price-selling">₹${item.public.sellingPrice.toLocaleString('en-IN')}</span>
          </div>
          <div class="product-card-actions">
            <a href="product.html?sku=${item.sku}" class="btn btn-outline btn-sm">View Details</a>
            <button class="btn btn-primary btn-sm" onclick="quickAddToCart('${item.sku}')">Add</button>
          </div>
        </div>
      </div>
    `;
  });

  relatedContainer.style.display = 'block';
  relatedContainer.innerHTML = `
    <div style="margin-top: 48px;">
      <h3 style="font-size: 1.5rem; font-weight: 800; color: var(--color-navy); margin-bottom: 20px;">
        Theoretically Associated Apparatus
      </h3>
      <div class="product-grid" style="grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));">
        ${cardsHtml}
      </div>
    </div>
  `;
}

// Render Fictional Customer Reviews
function renderReviewsSection(p) {
  const reviewsContainer = document.getElementById('reviews-section');
  if (!reviewsContainer) return;

  const reviews = p.public.reviews || [];

  let reviewsHtml = '';
  reviews.forEach(r => {
    reviewsHtml += `
      <div class="review-card">
        <div class="review-author-row">
          <span class="review-author-name">${escapeHtml(r.displayName)}</span>
          <span class="badge badge-teal">Verified Demo Customer</span>
        </div>
        <div class="rating-stars" style="font-size: 0.75rem;">
          ${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}
          <strong style="color: var(--color-navy); margin-left: 6px;">${escapeHtml(r.title)}</strong>
        </div>
        <p class="review-body">${escapeHtml(r.body)}</p>
      </div>
    `;
  });

  reviewsContainer.innerHTML = `
    <div style="margin-top: 48px; border-top: 1px solid var(--color-border); padding-top: 32px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
          <h3 style="font-size: 1.5rem; font-weight: 800; color: var(--color-navy);">Peer-Reviewed Customer Feedback</h3>
          <p style="font-size: 0.8125rem; color: var(--color-text-muted);">Observations and test telemetry recorded by verified fictional users.</p>
        </div>
        <span class="badge badge-gold" style="font-size: 0.75rem;">${p.public.rating.toFixed(1)} / 5.0 Composite Score</span>
      </div>
      <div class="reviews-grid">
        ${reviewsHtml}
      </div>
    </div>
  `;
}

function escapeHtml(text) {
  return (text || '').replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  })[m]);
}

// Global exposure
window.addEntireBundle = addEntireBundle;
