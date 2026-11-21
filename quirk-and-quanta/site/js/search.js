/**
 * Quirk & Quanta - Global Search Controller
 * Real-time search preview dropdown and form submission handling.
 */

document.addEventListener('DOMContentLoaded', () => {
  initSearch();
});

function initSearch() {
  const searchInput = document.getElementById('global-search-input');
  const searchForm = document.getElementById('global-search-form');
  const dropdown = document.getElementById('search-dropdown');

  if (!searchInput || !dropdown) return;

  // Live input filter
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim().toLowerCase();
    if (query.length < 2) {
      dropdown.classList.remove('active');
      dropdown.innerHTML = '';
      return;
    }

    renderSearchResults(query, dropdown);
  });

  // Close dropdown on click outside
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove('active');
    }
  });

  // Re-open if query is already present when clicking input
  searchInput.addEventListener('focus', () => {
    if (searchInput.value.trim().length >= 2) {
      dropdown.classList.add('active');
    }
  });

  // Handle Enter or Form submit
  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const query = searchInput.value.trim();
      if (query) {
        window.location.href = `products.html?search=${encodeURIComponent(query)}`;
      } else {
        window.location.href = 'products.html';
      }
    });
  }
}

function renderSearchResults(query, dropdown) {
  if (!window.AppState.products || window.AppState.products.length === 0) {
    return;
  }

  // Filter matching products
  const matches = window.AppState.products.filter(p => {
    const nameMatch = p.name.toLowerCase().includes(query);
    const skuMatch = p.sku.toLowerCase().includes(query);
    const catMatch = p.category.toLowerCase().includes(query);
    const descMatch = (p.public.shortDescription || '').toLowerCase().includes(query);
    const tagMatch = (p.public.tags || []).some(t => t.toLowerCase().includes(query));
    return nameMatch || skuMatch || catMatch || descMatch || tagMatch;
  }).slice(0, 6); // Top 6 instant matches

  if (matches.length === 0) {
    dropdown.innerHTML = `
      <div style="padding: 16px; text-align: center; font-size: 0.8125rem; color: var(--color-text-muted);">
        No matching peer-reviewed oddities found for "<strong>${escapeHtml(query)}</strong>"
      </div>
    `;
    dropdown.classList.add('active');
    return;
  }

  let html = '';
  matches.forEach(p => {
    html += `
      <a href="product.html?sku=${p.sku}" class="search-dropdown-item">
        <img src="${p.public.images.thumbnail}" alt="${p.name}" class="search-dropdown-thumb">
        <div style="flex: 1;">
          <div class="search-dropdown-name">${p.name}</div>
          <div style="display: flex; gap: 8px; font-size: 0.6875rem;">
            <span class="search-dropdown-sku">${p.sku}</span>
            <span style="color: var(--color-text-muted);">&#8226; ${p.category}</span>
          </div>
        </div>
        <div style="font-weight: 800; font-size: 0.875rem; color: var(--color-navy);">
          ₹${p.public.sellingPrice.toLocaleString('en-IN')}
        </div>
      </a>
    `;
  });

  html += `
    <div style="padding: 10px 14px; background: var(--color-bg); text-align: center; border-top: 1px solid var(--color-border);">
      <a href="products.html?search=${encodeURIComponent(query)}" style="font-size: 0.8125rem; font-weight: 700; color: var(--color-teal);">
        View all results for "${escapeHtml(query)}" &rarr;
      </a>
    </div>
  `;

  dropdown.innerHTML = html;
  dropdown.classList.add('active');
}

function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
