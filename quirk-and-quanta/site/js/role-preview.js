/**
 * Quirk & Quanta - Role Preview Controller
 * Educational Role Switcher demonstrating public vs internal separation.
 * WARNING: Frontend role switching is NOT real security.
 */

document.addEventListener('DOMContentLoaded', () => {
  renderRoleBanner();

  window.addEventListener('qq:role-changed', () => {
    renderRoleBanner();
    updateUIForRole();
  });
});

function renderRoleBanner() {
  let banner = document.getElementById('admin-demo-banner');
  const isAdmin = window.AppState.currentRole === 'admin';

  if (isAdmin) {
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'admin-demo-banner';
      banner.style.cssText = `
        background: #742A2A;
        color: #FFFFFF;
        padding: 8px 16px;
        font-size: 0.8125rem;
        font-weight: 600;
        text-align: center;
        border-bottom: 2px solid #FEB2B2;
        position: relative;
        z-index: 99;
      `;
      document.body.insertBefore(banner, document.body.firstChild);
    }
    banner.innerHTML = `
      <span>🛡️ <strong>DEMO MODE: ADMIN PREVIEW ACTIVE</strong> — Static storefront data is sanitized. Real internal cost prices, margins, and supplier codes reside outside static hosting and will be protected via server-side RBAC in later workshop gates.</span>
      <button onclick="openModal('role-explainer-modal')" style="text-decoration: underline; margin-left: 8px; color: #FEEBC8; cursor: pointer; font-weight: 700;">Why is this a demo?</button>
    `;
    banner.style.display = 'block';
  } else {
    if (banner) {
      banner.style.display = 'none';
    }
  }
}

function updateUIForRole() {
  const isAdmin = window.AppState.currentRole === 'admin';
  document.querySelectorAll('.admin-demo-annotation').forEach(el => {
    el.style.display = isAdmin ? 'block' : 'none';
  });
}

// Global exposure
window.updateUIForRole = updateUIForRole;
