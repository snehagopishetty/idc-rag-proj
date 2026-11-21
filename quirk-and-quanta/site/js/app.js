/**
 * Quirk & Quanta - Global Application Controller
 * Handles global state, toasts, navigation, modal management, and persistent cart/wishlist counts.
 */

const AppState = {
  cart: [],
  wishlist: [],
  products: [],
  currentRole: 'customer' // 'customer' or 'admin'
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  initStorage();
  updateHeaderBadges();
  initModals();
  initMobileNav();
  initRolePreview();
  loadPublicProductsFast();
});

// Load public product dataset for search and quick reference
async function loadPublicProductsFast() {
  try {
    const res = await fetch('data/products.public.json');
    if (res.ok) {
      AppState.products = await res.json();
      window.dispatchEvent(new CustomEvent('qq:products-loaded', { detail: AppState.products }));
    }
  } catch (err) {
    console.warn('Could not pre-fetch public products list in app.js:', err);
  }
}

// LocalStorage helpers
function initStorage() {
  try {
    const savedCart = localStorage.getItem('qq_cart');
    if (savedCart) {
      AppState.cart = JSON.parse(savedCart);
    }
    const savedWishlist = localStorage.getItem('qq_wishlist');
    if (savedWishlist) {
      AppState.wishlist = JSON.parse(savedWishlist);
    }
    const savedRole = localStorage.getItem('qq_demo_role');
    if (savedRole) {
      AppState.currentRole = savedRole;
    }
  } catch (e) {
    console.error('Storage access error:', e);
  }
}

function saveCart() {
  localStorage.setItem('qq_cart', JSON.stringify(AppState.cart));
  updateHeaderBadges();
  window.dispatchEvent(new CustomEvent('qq:cart-updated', { detail: AppState.cart }));
}

function saveWishlist() {
  localStorage.setItem('qq_wishlist', JSON.stringify(AppState.wishlist));
  updateHeaderBadges();
  window.dispatchEvent(new CustomEvent('qq:wishlist-updated', { detail: AppState.wishlist }));
}

// Update header badges
function updateHeaderBadges() {
  const cartBadge = document.getElementById('header-cart-count');
  if (cartBadge) {
    const totalCount = AppState.cart.reduce((sum, item) => sum + (item.quantity || 1), 0);
    cartBadge.textContent = totalCount;
  }

  const wishlistBadge = document.getElementById('header-wishlist-count');
  if (wishlistBadge) {
    wishlistBadge.textContent = AppState.wishlist.length;
  }
}

// Toast notification helper
function showToast(message, type = 'teal') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type === 'gold' ? 'toast-gold' : ''}`;
  toast.innerHTML = `<span>⚡</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

// Modal handling
function initModals() {
  // Close modal when clicking on overlay or close button
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay || e.target.closest('.modal-close-btn') || e.target.classList.contains('close-modal-trigger')) {
        closeAllModals();
      }
    });
  });

  // ESC key closes modals
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeAllModals();
    }
  });
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeAllModals() {
  document.querySelectorAll('.modal-overlay').forEach(modal => modal.classList.remove('active'));
  const drawer = document.getElementById('cart-drawer');
  if (drawer) drawer.classList.remove('active');
  document.body.style.overflow = '';
}

// Mobile Navigation
function initMobileNav() {
  const toggleBtn = document.getElementById('mobile-menu-btn');
  const navMenu = document.getElementById('mobile-nav-drawer');
  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('active');
    });
  }
}

// Role preview toggle hookup
function initRolePreview() {
  const roleToggleBtn = document.getElementById('role-toggle-btn');
  if (roleToggleBtn) {
    updateRoleButtonUI(roleToggleBtn);
    roleToggleBtn.addEventListener('click', () => {
      AppState.currentRole = AppState.currentRole === 'customer' ? 'admin' : 'customer';
      localStorage.setItem('qq_demo_role', AppState.currentRole);
      updateRoleButtonUI(roleToggleBtn);
      showToast(
        AppState.currentRole === 'admin' 
          ? 'Switched to Admin Role Preview (Educational Mock)' 
          : 'Switched to Standard Customer View',
        AppState.currentRole === 'admin' ? 'gold' : 'teal'
      );
      window.dispatchEvent(new CustomEvent('qq:role-changed', { detail: AppState.currentRole }));
    });
  }
}

function updateRoleButtonUI(btn) {
  if (AppState.currentRole === 'admin') {
    btn.classList.add('is-admin');
    btn.innerHTML = `<span>🛡️</span> Role: Admin (Demo)`;
  } else {
    btn.classList.remove('is-admin');
    btn.innerHTML = `<span>👤</span> Role: Customer`;
  }
}

// Expose globally
window.AppState = AppState;
window.saveCart = saveCart;
window.saveWishlist = saveWishlist;
window.showToast = showToast;
window.openModal = openModal;
window.closeAllModals = closeAllModals;
