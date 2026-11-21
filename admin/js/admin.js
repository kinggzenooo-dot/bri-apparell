/**
 * BRI APPARELL — Enterprise Admin Operations Controller
 * Connected directly to Python Flask REST API & PostgreSQL / SQLite Database
 */

const Admin = {
  API_BASE: '/api',

  // Currency Formatter
  formatMoney(amount) {
    return `₱${Number(amount || 0).toLocaleString('en-PH', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
  },

  // Date Formatter
  formatDate(isoStr) {
    if (!isoStr) return '—';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  },

  formatDateOnly(isoStr) {
    if (!isoStr) return '—';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  },

  // Auth Helpers
  getToken() {
    return localStorage.getItem('bri_admin_token') || localStorage.getItem('bri_token');
  },

  getUser() {
    try {
      return JSON.parse(localStorage.getItem('bri_admin_user')) || JSON.parse(localStorage.getItem('bri_user'));
    } catch (e) {
      return null;
    }
  },

  setAuth(token, user) {
    localStorage.setItem('bri_admin_token', token);
    localStorage.setItem('bri_admin_user', JSON.stringify(user));
  },

  clearAuth() {
    localStorage.removeItem('bri_admin_token');
    localStorage.removeItem('bri_admin_user');
  },

  // Unified Fetch Wrapper with Auth Bearer
  async api(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${this.API_BASE}${endpoint}`;
    const token = this.getToken();

    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const res = await fetch(url, { ...options, headers });
      const data = await res.json().catch(() => ({}));

      if (res.status === 401) {
        // Expired or unauthorized
        this.clearAuth();
        if (!window.location.pathname.includes('login.html')) {
          window.location.href = 'login.html';
        }
        throw new Error(data.error || 'Authentication expired. Please sign in again.');
      }

      if (!res.ok) {
        throw new Error(data.error || `Request failed with status ${res.status}`);
      }

      return data;
    } catch (err) {
      console.error(`[API Error] ${endpoint}:`, err);
      throw err;
    }
  },

  // Toast Notification
  toast(message, type = 'info') {
    let container = document.getElementById('admin-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'admin-toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    let icon = '<i data-lucide="info" style="width:18px;height:18px;"></i>';
    if (type === 'success') icon = '<i data-lucide="check-circle" style="width:18px;height:18px;color:#15803d;"></i>';
    if (type === 'error') icon = '<i data-lucide="alert-circle" style="width:18px;height:18px;color:#b91c1c;"></i>';

    toast.innerHTML = `
      <div style="display:flex;align-items:center;gap:0.75rem;">
        ${icon}
        <span style="font-size:0.875rem;font-weight:600;">${message}</span>
      </div>
    `;

    container.appendChild(toast);
    if (window.lucide) window.lucide.createIcons();

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  },

  // Check Auth & Guard Admin Routes
  async guardAuth() {
    if (window.location.pathname.includes('login.html')) return;

    const user = this.getUser();
    const token = this.getToken();

    if (!user || !token || user.role !== 'admin') {
      window.location.href = 'login.html';
      return;
    }

    // Verify token with backend
    try {
      const res = await this.api('/auth/me');
      if (!res.authenticated || res.user.role !== 'admin') {
        this.clearAuth();
        window.location.href = 'login.html';
      }
    } catch (e) {
      // If server unreachable, proceed with cached credentials
    }
  },

  // Setup Common Shell (Sidebar, Topbar, User Menu, Lucide Icons)
  initShell() {
    const user = this.getUser();
    if (user) {
      const nameEls = document.querySelectorAll('.admin-user-name');
      nameEls.forEach(el => el.textContent = user.full_name);

      const avatarEls = document.querySelectorAll('.admin-user-avatar');
      avatarEls.forEach(el => el.textContent = user.avatar_initials || 'AD');

      const roleEls = document.querySelectorAll('.admin-user-role');
      roleEls.forEach(el => el.textContent = `${user.department || 'Executive'} • Super Admin`);
    }

    // Mobile menu toggle
    const toggleBtn = document.getElementById('mobile-menu-toggle');
    const sidebar = document.querySelector('.staff-sidebar');
    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('mobile-open');
      });
    }

    // User dropdown toggle
    const userChip = document.getElementById('admin-user-chip');
    const userDropdown = document.getElementById('admin-user-dropdown');
    if (userChip && userDropdown) {
      userChip.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('open');
      });
      document.addEventListener('click', () => userDropdown.classList.remove('open'));
    }

    // Logout Handler
    const logoutBtns = document.querySelectorAll('.admin-logout-btn');
    logoutBtns.forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        try {
          await this.api('/auth/logout', { method: 'POST' });
        } catch (e) {}
        this.clearAuth();
        window.location.href = 'login.html';
      });
    });

    // Load Notification Count
    this.updateNotificationBadge();

    if (window.lucide) window.lucide.createIcons();
  },

  async updateNotificationBadge() {
    try {
      const res = await this.api('/notifications?unread_only=true');
      const badge = document.getElementById('topbar-notif-dot');
      if (badge) {
        badge.style.display = (res.unreadCount > 0) ? 'block' : 'none';
      }
    } catch (e) {}
  }
};

// Auto-run guard on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  Admin.guardAuth();
  Admin.initShell();
});
