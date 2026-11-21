/**
 * Quirk & Quanta - Shopping Cart & Wishlist Module
 * LocalStorage persistence, drawer rendering, and checkout demonstration modal.
 */

document.addEventListener('DOMContentLoaded', () => {
  initCartDrawer();
  renderCartItems();
});

// Initialize Cart Drawer Triggers
function initCartDrawer() {
  const openCartBtn = document.getElementById('header-cart-btn');
  const closeCartBtn = document.getElementById('close-cart-btn');
  const cartDrawer = document.getElementById('cart-drawer');
  const cartOverlay = document.getElementById('cart-drawer-overlay');
  const checkoutBtn = document.getElementById('checkout-action-btn');

  if (openCartBtn && cartDrawer) {
    openCartBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openCartDrawer();
    });
  }

  if (closeCartBtn && cartDrawer) {
    closeCartBtn.addEventListener('click', closeCartDrawer);
  }

  if (cartOverlay) {
    cartOverlay.addEventListener('click', closeCartDrawer);
  }

  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      closeCartDrawer();
      window.openModal('checkout-demo-modal');
    });
  }

  // Listen to cart update events
  window.addEventListener('qq:cart-updated', () => {
    renderCartItems();
  });
}

function openCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-drawer-overlay');
  if (drawer && overlay) {
    renderCartItems();
    drawer.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeCartDrawer() {
  const drawer = document.getElementById('cart-drawer');
  const overlay = document.getElementById('cart-drawer-overlay');
  if (drawer) drawer.classList.remove('active');
  if (overlay) overlay.classList.remove('active');
  document.body.style.overflow = '';
}

// Add item to cart
function addToCart(product, quantity = 1) {
  const existing = window.AppState.cart.find(item => item.sku === product.sku);
  if (existing) {
    existing.quantity = (existing.quantity || 1) + quantity;
  } else {
    window.AppState.cart.push({
      sku: product.sku,
      name: product.name,
      sellingPrice: product.public.sellingPrice,
      thumbnail: product.public.images.thumbnail,
      category: product.category,
      quantity: quantity
    });
  }

  window.saveCart();
  window.showToast(`Added ${quantity}x "${product.name}" to cart!`);
  openCartDrawer();
}

// Remove item from cart
function removeFromCart(sku) {
  window.AppState.cart = window.AppState.cart.filter(item => item.sku !== sku);
  window.saveCart();
  window.showToast('Item removed from cart');
}

// Update quantity
function updateCartQuantity(sku, delta) {
  const item = window.AppState.cart.find(item => item.sku === sku);
  if (item) {
    item.quantity = (item.quantity || 1) + delta;
    if (item.quantity <= 0) {
      removeFromCart(sku);
      return;
    }
    window.saveCart();
  }
}

// Toggle Wishlist
function toggleWishlist(sku, name = '') {
  const idx = window.AppState.wishlist.indexOf(sku);
  if (idx > -1) {
    window.AppState.wishlist.splice(idx, 1);
    window.showToast(`Removed from Wishlist`);
  } else {
    window.AppState.wishlist.push(sku);
    window.showToast(`Saved "${name || sku}" to Wishlist!`, 'gold');
  }
  window.saveWishlist();
}

// Render Cart Drawer Contents
function renderCartItems() {
  const container = document.getElementById('cart-items-container');
  const subtotalEl = document.getElementById('cart-subtotal-price');
  const checkoutBtn = document.getElementById('checkout-action-btn');

  if (!container) return;

  if (window.AppState.cart.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 48px 16px; color: var(--color-text-muted);">
        <div style="font-size: 3rem; margin-bottom: 12px;">🛒</div>
        <p style="font-weight: 700; color: var(--color-navy); margin-bottom: 4px;">Your Cart is in Ground State</p>
        <p style="font-size: 0.8125rem;">No peer-reviewed items selected yet.</p>
        <a href="products.html" class="btn btn-primary btn-sm" style="margin-top: 16px;" onclick="closeCartDrawer()">Explore Catalog</a>
      </div>
    `;
    if (subtotalEl) subtotalEl.textContent = '₹0';
    if (checkoutBtn) checkoutBtn.disabled = true;
    return;
  }

  let total = 0;
  let html = '';

  window.AppState.cart.forEach(item => {
    const itemTotal = (item.sellingPrice || 0) * (item.quantity || 1);
    total += itemTotal;

    html += `
      <div class="cart-item-card">
        <img src="${item.thumbnail}" alt="${item.name}" class="cart-item-thumb">
        <div class="cart-item-details">
          <a href="product.html?sku=${item.sku}" class="cart-item-title" onclick="closeCartDrawer()">${item.name}</a>
          <span style="font-size: 0.6875rem; color: var(--color-text-light); font-family: var(--font-mono);">${item.sku}</span>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
            <div class="quantity-stepper" style="transform: scale(0.85); transform-origin: left center;">
              <button class="qty-btn" onclick="updateCartQuantity('${item.sku}', -1)">-</button>
              <span class="qty-input" style="line-height: 42px;">${item.quantity || 1}</span>
              <button class="qty-btn" onclick="updateCartQuantity('${item.sku}', 1)">+</button>
            </div>
            <div style="text-align: right;">
              <div class="cart-item-price">₹${itemTotal.toLocaleString('en-IN')}</div>
              <button onclick="removeFromCart('${item.sku}')" style="font-size: 0.6875rem; color: var(--color-danger); text-decoration: underline;">Remove</button>
            </div>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
  if (subtotalEl) subtotalEl.textContent = `₹${total.toLocaleString('en-IN')}`;
  if (checkoutBtn) checkoutBtn.disabled = false;
}

// Global exposures
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.updateCartQuantity = updateCartQuantity;
window.toggleWishlist = toggleWishlist;
window.openCartDrawer = openCartDrawer;
window.closeCartDrawer = closeCartDrawer;
