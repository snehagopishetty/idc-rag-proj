/**
 * Quirk & Quanta - Product Catalog Controller
 * Loads public products, handles client-side filtering, sorting, pagination/rendering, and URL synchronization.
 */

let allProducts = [];
let filteredProducts = [];

const filterState = {
  searchQuery: '',
  category: 'ALL',
  minPrice: null,
  maxPrice: null,
  inStockOnly: false,
  minRating: 0,
  sortBy: 'featured'
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('catalog-products-grid')) {
    initCatalog();
  }
});

async function initCatalog() {
  readUrlParams();
  setupFilterControls();

  try {
    const res = await fetch('data/products.public.json');
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    allProducts = await res.json();
    window.AppState.products = allProducts;
    applyFilters();
  } catch (err) {
    console.error('Failed to load products:', err);
    const grid = document.getElementById('catalog-products-grid');
    if (grid) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-state-icon">⚠️</div>
          <h3 class="empty-state-title">Data Loading Experiment Failed</h3>
          <p class="empty-state-desc">Could not load <code>data/products.public.json</code>. Ensure the site is served via an HTTP server (e.g. <code>python3 -m http.server 8000</code>).</p>
        </div>
      `;
    }
  }
}

// Read URL Query Parameters
function readUrlParams() {
  const params = new URLSearchParams(window.location.search);
  
  if (params.has('category')) {
    filterState.category = params.get('category');
  }
  if (params.has('search')) {
    filterState.searchQuery = params.get('search');
    const searchInput = document.getElementById('catalog-search-input');
    if (searchInput) searchInput.value = filterState.searchQuery;
  }
  if (params.has('sort')) {
    filterState.sortBy = params.get('sort');
    const sortSelect = document.getElementById('catalog-sort-select');
    if (sortSelect) sortSelect.value = filterState.sortBy;
  }
  if (params.has('minPrice')) {
    filterState.minPrice = parseFloat(params.get('minPrice')) || null;
  }
  if (params.has('maxPrice')) {
    filterState.maxPrice = parseFloat(params.get('maxPrice')) || null;
  }
}

// Update URL parameters without reloading
function updateUrlParams() {
  const params = new URLSearchParams();
  if (filterState.category && filterState.category !== 'ALL') {
    params.set('category', filterState.category);
  }
  if (filterState.searchQuery) {
    params.set('search', filterState.searchQuery);
  }
  if (filterState.sortBy && filterState.sortBy !== 'featured') {
    params.set('sort', filterState.sortBy);
  }
  if (filterState.minPrice) {
    params.set('minPrice', filterState.minPrice);
  }
  if (filterState.maxPrice) {
    params.set('maxPrice', filterState.maxPrice);
  }

  const newUrl = `${window.location.pathname}${params.toString() ? '?' + params.toString() : ''}`;
  window.history.replaceState({}, '', newUrl);
}

// Setup Event Listeners for Filters
function setupFilterControls() {
  // Search input
  const searchInput = document.getElementById('catalog-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      filterState.searchQuery = e.target.value.trim();
      applyFilters();
    });
  }

  // Category radio / options
  document.querySelectorAll('input[name="category-filter"]').forEach(radio => {
    if (radio.value === filterState.category) {
      radio.checked = true;
    }
    radio.addEventListener('change', (e) => {
      filterState.category = e.target.value;
      applyFilters();
    });
  });

  // Price inputs
  const minPriceInput = document.getElementById('filter-min-price');
  const maxPriceInput = document.getElementById('filter-max-price');
  const applyPriceBtn = document.getElementById('apply-price-filter-btn');

  if (applyPriceBtn) {
    applyPriceBtn.addEventListener('click', () => {
      filterState.minPrice = minPriceInput && minPriceInput.value ? parseFloat(minPriceInput.value) : null;
      filterState.maxPrice = maxPriceInput && maxPriceInput.value ? parseFloat(maxPriceInput.value) : null;
      applyFilters();
    });
  }

  // In-stock checkbox
  const inStockCheckbox = document.getElementById('filter-in-stock');
  if (inStockCheckbox) {
    inStockCheckbox.addEventListener('change', (e) => {
      filterState.inStockOnly = e.target.checked;
      applyFilters();
    });
  }

  // Rating select
  const ratingSelect = document.getElementById('filter-rating-select');
  if (ratingSelect) {
    ratingSelect.addEventListener('change', (e) => {
      filterState.minRating = parseFloat(e.target.value) || 0;
      applyFilters();
    });
  }

  // Sort dropdown
  const sortSelect = document.getElementById('catalog-sort-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      filterState.sortBy = e.target.value;
      applyFilters();
    });
  }

  // Clear filters button
  const clearBtn = document.getElementById('clear-filters-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', clearAllFilters);
  }
}

// Clear all active filters
function clearAllFilters() {
  filterState.searchQuery = '';
  filterState.category = 'ALL';
  filterState.minPrice = null;
  filterState.maxPrice = null;
  filterState.inStockOnly = false;
  filterState.minRating = 0;
  filterState.sortBy = 'featured';

  const searchInput = document.getElementById('catalog-search-input');
  if (searchInput) searchInput.value = '';

  const minPriceInput = document.getElementById('filter-min-price');
  if (minPriceInput) minPriceInput.value = '';

  const maxPriceInput = document.getElementById('filter-max-price');
  if (maxPriceInput) maxPriceInput.value = '';

  const inStockCheckbox = document.getElementById('filter-in-stock');
  if (inStockCheckbox) inStockCheckbox.checked = false;

  const ratingSelect = document.getElementById('filter-rating-select');
  if (ratingSelect) ratingSelect.value = '0';

  const sortSelect = document.getElementById('catalog-sort-select');
  if (sortSelect) sortSelect.value = 'featured';

  const allCategoryRadio = document.querySelector('input[name="category-filter"][value="ALL"]');
  if (allCategoryRadio) allCategoryRadio.checked = true;

  applyFilters();
}

// Filter and Sort Engine
function applyFilters() {
  const query = filterState.searchQuery.toLowerCase();

  filteredProducts = allProducts.filter(p => {
    // 1. Category Filter
    if (filterState.category !== 'ALL') {
      if (p.categoryId !== filterState.category && p.category !== filterState.category) {
        return false;
      }
    }

    // 2. Search Text
    if (query) {
      const matchName = p.name.toLowerCase().includes(query);
      const matchSku = p.sku.toLowerCase().includes(query);
      const matchCat = p.category.toLowerCase().includes(query);
      const matchDesc = (p.public.shortDescription || '').toLowerCase().includes(query);
      const matchTags = (p.public.tags || []).some(t => t.toLowerCase().includes(query));
      if (!matchName && !matchSku && !matchCat && !matchDesc && !matchTags) {
        return false;
      }
    }

    // 3. Price Filter
    const price = p.public.sellingPrice;
    if (filterState.minPrice !== null && price < filterState.minPrice) {
      return false;
    }
    if (filterState.maxPrice !== null && price > filterState.maxPrice) {
      return false;
    }

    // 4. Stock Filter
    if (filterState.inStockOnly && p.public.stockStatus !== 'in_stock') {
      return false;
    }

    // 5. Rating Filter
    if (filterState.minRating > 0 && p.public.rating < filterState.minRating) {
      return false;
    }

    return true;
  });

  // Sorting
  sortProducts(filteredProducts, filterState.sortBy);

  // Render
  renderCatalogGrid(filteredProducts);
  updateCounterAndChips(filteredProducts.length);
  updateUrlParams();
}

function sortProducts(list, sortBy) {
  switch (sortBy) {
    case 'price-asc':
      list.sort((a, b) => a.public.sellingPrice - b.public.sellingPrice);
      break;
    case 'price-desc':
      list.sort((a, b) => b.public.sellingPrice - a.public.sellingPrice);
      break;
    case 'rating-desc':
      list.sort((a, b) => b.public.rating - a.public.rating);
      break;
    case 'name-asc':
      list.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case 'name-desc':
      list.sort((a, b) => b.name.localeCompare(a.name));
      break;
    case 'sku-asc':
      list.sort((a, b) => a.sku.localeCompare(b.sku));
      break;
    case 'featured':
    default:
      // Default order by ID
      list.sort((a, b) => a.id.localeCompare(b.id));
      break;
  }
}

// Render Products Grid
function renderCatalogGrid(products) {
  const grid = document.getElementById('catalog-products-grid');
  if (!grid) return;

  if (products.length === 0) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <div class="empty-state-icon">🔬</div>
        <h3 class="empty-state-title">No Experiments Match Your Hypothesis</h3>
        <p class="empty-state-desc">Your query parameters yielded zero peer-reviewed products in this domain. Try broadening your criteria or reset all filters.</p>
        <button class="btn btn-primary" onclick="clearAllFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  let html = '';
  products.forEach(p => {
    const isWishlisted = window.AppState.wishlist.includes(p.sku);
    const discountPercent = p.public.listPrice > p.public.sellingPrice
      ? Math.round(((p.public.listPrice - p.public.sellingPrice) / p.public.listPrice) * 100)
      : 0;

    html += `
      <div class="product-card" id="card-${p.sku}">
        <div class="product-card-thumb-wrapper">
          <span class="badge badge-navy product-card-badge">${p.category}</span>
          <button class="wishlist-btn-toggle ${isWishlisted ? 'active' : ''}" 
                  onclick="toggleWishlist('${p.sku}', '${escapeHtml(p.name)}'); this.classList.toggle('active');" 
                  title="Save to Wishlist" aria-label="Save to Wishlist">
            ♥
          </button>
          <a href="product.html?sku=${p.sku}" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
            <img src="${p.public.images.thumbnail}" 
                 alt="${escapeHtml(p.public.images.alt || p.name)}" 
                 class="product-card-thumb" 
                 loading="lazy">
          </a>
        </div>
        <div class="product-card-body">
          <div class="product-card-meta">
            <span>${p.sku}</span>
            <span class="stock-indicator ${p.public.stockStatus === 'in_stock' ? 'stock-in' : 'stock-low'}">
              <span class="stock-dot"></span>
              ${p.public.stockStatus === 'in_stock' ? 'In Stock' : 'Low Stock'}
            </span>
          </div>

          <h3 class="product-card-title">
            <a href="product.html?sku=${p.sku}">${p.name}</a>
          </h3>

          <div class="product-card-rating">
            <span class="rating-stars">★</span>
            <span class="rating-score">${p.public.rating.toFixed(1)}</span>
            <span class="review-count-label">(${p.public.reviewCount})</span>
          </div>

          <p class="product-card-desc">${p.public.shortDescription}</p>

          <div class="product-card-price-row">
            <span class="price-selling">₹${p.public.sellingPrice.toLocaleString('en-IN')}</span>
            ${p.public.listPrice > p.public.sellingPrice ? `
              <span class="price-list">₹${p.public.listPrice.toLocaleString('en-IN')}</span>
              <span class="price-savings">-${discountPercent}%</span>
            ` : ''}
          </div>

          <div class="product-card-actions">
            <a href="product.html?sku=${p.sku}" class="btn btn-outline btn-sm">View Details</a>
            <button class="btn btn-primary btn-sm" onclick="quickAddToCart('${p.sku}')">Add</button>
          </div>
        </div>
      </div>
    `;
  });

  grid.innerHTML = html;
  if (window.updateUIForRole) window.updateUIForRole();
}

function quickAddToCart(sku) {
  const p = allProducts.find(item => item.sku === sku);
  if (p) {
    window.addToCart(p, 1);
  }
}

// Update Results Counter and Active Filter Tags
function updateCounterAndChips(count) {
  const countEl = document.getElementById('catalog-results-count');
  if (countEl) {
    countEl.textContent = `Showing ${count} of ${allProducts.length} peer-reviewed items`;
  }

  const chipsContainer = document.getElementById('active-filter-chips-container');
  if (!chipsContainer) return;

  let chips = '';
  if (filterState.category !== 'ALL') {
    chips += `
      <span class="filter-chip">
        Category: ${filterState.category}
        <button class="chip-remove-btn" onclick="clearCategoryFilter()">&times;</button>
      </span>
    `;
  }

  if (filterState.searchQuery) {
    chips += `
      <span class="filter-chip">
        Query: "${filterState.searchQuery}"
        <button class="chip-remove-btn" onclick="clearSearchFilter()">&times;</button>
      </span>
    `;
  }

  if (filterState.minPrice || filterState.maxPrice) {
    chips += `
      <span class="filter-chip">
        Price: ₹${filterState.minPrice || 0} - ₹${filterState.maxPrice || 'Max'}
        <button class="chip-remove-btn" onclick="clearPriceFilter()">&times;</button>
      </span>
    `;
  }

  chipsContainer.innerHTML = chips;
}

function clearCategoryFilter() {
  filterState.category = 'ALL';
  const allRadio = document.querySelector('input[name="category-filter"][value="ALL"]');
  if (allRadio) allRadio.checked = true;
  applyFilters();
}

function clearSearchFilter() {
  filterState.searchQuery = '';
  const searchInput = document.getElementById('catalog-search-input');
  if (searchInput) searchInput.value = '';
  applyFilters();
}

function clearPriceFilter() {
  filterState.minPrice = null;
  filterState.maxPrice = null;
  const minInput = document.getElementById('filter-min-price');
  const maxInput = document.getElementById('filter-max-price');
  if (minInput) minInput.value = '';
  if (maxInput) maxInput.value = '';
  applyFilters();
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
window.clearAllFilters = clearAllFilters;
window.clearCategoryFilter = clearCategoryFilter;
window.clearSearchFilter = clearSearchFilter;
window.clearPriceFilter = clearPriceFilter;
window.quickAddToCart = quickAddToCart;
