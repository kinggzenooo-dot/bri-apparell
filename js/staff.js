/**
 * BRI APPARELL — Staff Interface Operations Engine
 * Vanilla JavaScript controller for order workflows, inventory tracking, modals, and navigation
 */

const STAFF = {
  // Format Currency
  formatMoney(amount) {
    return `₱${Number(amount).toLocaleString('en-PH', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
  },

  // Auth Helpers
  getToken() {
    return localStorage.getItem('bri_token') || localStorage.getItem('bri_staff_token') || localStorage.getItem('bri_admin_token');
  },

  getUser() {
    try {
      return JSON.parse(localStorage.getItem('bri_user')) || JSON.parse(localStorage.getItem('bri_staff_user'));
    } catch (e) {
      return null;
    }
  },

  clearAuth() {
    localStorage.removeItem('bri_token');
    localStorage.removeItem('bri_user');
    localStorage.removeItem('bri_staff_token');
    localStorage.removeItem('bri_staff_user');
  },

  // Role & Session Guard
  async guardAuth() {
    const user = this.getUser();
    const token = this.getToken();

    if (!user || !token || (user.role !== 'staff' && user.role !== 'admin')) {
      window.location.href = `/authorization/login.html?redirect=${encodeURIComponent(window.location.pathname)}&reason=staff_required`;
      return false;
    }

    try {
      const res = await fetch('/api/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (!data.authenticated || (data.user.role !== 'staff' && data.user.role !== 'admin')) {
        this.clearAuth();
        window.location.href = `/authorization/login.html?redirect=${encodeURIComponent(window.location.pathname)}&reason=staff_required`;
        return false;
      }
    } catch (e) {}
    return true;
  },

  // Format Date & Time
  formatDateTime(isoStr) {
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
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  },

  // --- LOCAL STORAGE DATA STORE ---
  store: {
    init() {
      if (!localStorage.getItem('bri_staff_orders')) {
        localStorage.setItem('bri_staff_orders', JSON.stringify(INITIAL_STAFF_DATA.orders));
      }
      if (!localStorage.getItem('bri_staff_inventory')) {
        localStorage.setItem('bri_staff_inventory', JSON.stringify(INITIAL_STAFF_DATA.inventoryVariants));
      }
      if (!localStorage.getItem('bri_staff_history')) {
        localStorage.setItem('bri_staff_history', JSON.stringify(INITIAL_STAFF_DATA.stockHistory));
      }
      if (!localStorage.getItem('bri_staff_customers')) {
        localStorage.setItem('bri_staff_customers', JSON.stringify(INITIAL_STAFF_DATA.customers));
      }
      if (!localStorage.getItem('bri_staff_reviews')) {
        localStorage.setItem('bri_staff_reviews', JSON.stringify(INITIAL_STAFF_DATA.reviews));
      }
      if (!localStorage.getItem('bri_staff_notifications')) {
        localStorage.setItem('bri_staff_notifications', JSON.stringify(INITIAL_STAFF_DATA.notifications));
      }
      if (!localStorage.getItem('bri_staff_user')) {
        localStorage.setItem('bri_staff_user', JSON.stringify(INITIAL_STAFF_DATA.user));
      }

      // Synchronize with Centralized Python Backend & Database
      if (typeof window !== 'undefined') {
        const token = STAFF.getToken();
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        fetch('/api/orders', { headers })
          .then(res => res.json())
          .then(data => {
            if (data && data.orders && data.orders.length > 0) {
              localStorage.setItem('bri_staff_orders', JSON.stringify(data.orders));
              if (STAFF.ui && STAFF.ui.updateBadges) STAFF.ui.updateBadges();
            }
          })
          .catch(() => {});

        fetch('/api/inventory', { headers })
          .then(res => res.json())
          .then(data => {
            if (data && data.inventory && data.inventory.length > 0) {
              localStorage.setItem('bri_staff_inventory', JSON.stringify(data.inventory));
            }
          })
          .catch(() => {});
      }
    },

    getOrders() {
      try {
        return JSON.parse(localStorage.getItem('bri_staff_orders')) || [];
      } catch (e) {
        return INITIAL_STAFF_DATA.orders;
      }
    },

    saveOrders(orders) {
      localStorage.setItem('bri_staff_orders', JSON.stringify(orders));
      STAFF.ui.updateBadges();
    },

    getOrderById(id) {
      return this.getOrders().find(o => o.orderId === id || o.orderId.toLowerCase() === id.toLowerCase());
    },

    getInventory() {
      try {
        return JSON.parse(localStorage.getItem('bri_staff_inventory')) || [];
      } catch (e) {
        return INITIAL_STAFF_DATA.inventoryVariants;
      }
    },

    saveInventory(inv) {
      localStorage.setItem('bri_staff_inventory', JSON.stringify(inv));
      STAFF.ui.updateBadges();
    },

    getStockHistory() {
      try {
        return JSON.parse(localStorage.getItem('bri_staff_history')) || [];
      } catch (e) {
        return INITIAL_STAFF_DATA.stockHistory;
      }
    },

    saveStockHistory(hist) {
      localStorage.setItem('bri_staff_history', JSON.stringify(hist));
    },

    getCustomers() {
      try {
        return JSON.parse(localStorage.getItem('bri_staff_customers')) || [];
      } catch (e) {
        return INITIAL_STAFF_DATA.customers;
      }
    },

    saveCustomers(custs) {
      localStorage.setItem('bri_staff_customers', JSON.stringify(custs));
    },

    getReviews() {
      try {
        return JSON.parse(localStorage.getItem('bri_staff_reviews')) || [];
      } catch (e) {
        return INITIAL_STAFF_DATA.reviews;
      }
    },

    saveReviews(revs) {
      localStorage.setItem('bri_staff_reviews', JSON.stringify(revs));
    },

    getNotifications() {
      try {
        return JSON.parse(localStorage.getItem('bri_staff_notifications')) || [];
      } catch (e) {
        return INITIAL_STAFF_DATA.notifications;
      }
    },

    saveNotifications(notifs) {
      localStorage.setItem('bri_staff_notifications', JSON.stringify(notifs));
      STAFF.ui.updateBadges();
    },

    getUser() {
      try {
        return JSON.parse(localStorage.getItem('bri_staff_user')) || INITIAL_STAFF_DATA.user;
      } catch (e) {
        return INITIAL_STAFF_DATA.user;
      }
    },

    saveUser(u) {
      localStorage.setItem('bri_staff_user', JSON.stringify(u));
    }
  },

  // --- ORDER WORKFLOW ENGINE ---
  workflow: {
    // Valid order transitions
    canTransition(currentStatus, nextStatus) {
      const orderFlow = [
        'Pending',
        'Confirmed',
        'Processing',
        'Packed',
        'Ready to Ship',
        'Shipped',
        'Delivered'
      ];
      const currIdx = orderFlow.indexOf(currentStatus);
      const nextIdx = orderFlow.indexOf(nextStatus);
      if (nextStatus === 'Cancelled') return currentStatus !== 'Delivered' && currentStatus !== 'Shipped';
      return nextIdx === currIdx + 1;
    },

    advanceStatus(orderId, nextStatus, customNote = null) {
      const orders = STAFF.store.getOrders();
      const order = orders.find(o => o.orderId === orderId);
      if (!order) return { success: false, message: 'Order not found.' };

      const user = STAFF.store.getUser();
      const prevStatus = order.status;
      order.status = nextStatus;

      const stepMap = {
        'Pending': 1,
        'Confirmed': 2,
        'Processing': 3,
        'Packed': 4,
        'Ready to Ship': 5,
        'Shipped': 6,
        'Delivered': 7,
        'Cancelled': 0
      };
      order.statusStep = stepMap[nextStatus] || 1;

      // Append to audit log
      order.history.push({
        time: new Date().toISOString(),
        event: customNote || `Order status updated from ${prevStatus} to ${nextStatus}`,
        staff: user.name
      });

      // If marked as Shipped, ensure tracking number
      if (nextStatus === 'Shipped' && !order.trackingNumber) {
        order.trackingNumber = `BRI-EXP-${Math.floor(100000 + Math.random() * 900000)}`;
      }

      STAFF.store.saveOrders(orders);

      // Create notification
      const notifs = STAFF.store.getNotifications();
      notifs.unshift({
        id: `NOTIF-${Date.now()}`,
        type: 'order',
        title: `ORDER ${order.orderId} UPDATED`,
        message: `Order #${order.orderId} moved to "${nextStatus}".`,
        timestamp: new Date().toISOString(),
        read: false,
        link: `order-details.html?id=${order.orderId}`
      });
      STAFF.store.saveNotifications(notifs);

      return { success: true, order: order };
    }
  },

  // --- STATUS BADGE GENERATORS ---
  badge(status, type = 'order') {
    const s = (status || '').toLowerCase().trim();
    let badgeClass = 'badge-neutral';

    if (s === 'pending') badgeClass = 'badge-pending';
    else if (s === 'processing' || s === 'packed' || s === 'ready to ship' || s === 'confirmed') badgeClass = 'badge-processing';
    else if (s === 'shipped' || s === 'delivered' || s === 'in stock' || s === 'paid' || s === 'active' || s === 'published') badgeClass = 'badge-delivered';
    else if (s === 'low stock') badgeClass = 'badge-pending';
    else if (s === 'critical' || s === 'out of stock' || s === 'cancelled' || s === 'failed' || s === 'flagged') badgeClass = 'badge-critical';

    return `
      <span class="status-pill ${badgeClass}">
        <span class="status-dot"></span>
        ${status.toUpperCase()}
      </span>
    `;
  },

  // --- TOAST NOTIFICATIONS ---
  toast: {
    show(message, type = 'info') {
      let container = document.getElementById('staff-toast-container');
      if (!container) {
        container = document.createElement('div');
        container.id = 'staff-toast-container';
        container.className = 'staff-toast-container';
        document.body.appendChild(container);
      }

      const toast = document.createElement('div');
      toast.className = 'staff-toast';
      let icon = '<i data-lucide="check-circle" style="width:18px;height:18px;color:#22c55e;"></i>';
      if (type === 'warn') icon = '<i data-lucide="alert-triangle" style="width:18px;height:18px;color:#facc15;"></i>';
      if (type === 'error') icon = '<i data-lucide="alert-circle" style="width:18px;height:18px;color:#ef4444;"></i>';

      toast.innerHTML = `
        ${icon}
        <span>${message}</span>
      `;

      container.appendChild(toast);
      if (window.lucide) window.lucide.createIcons();

      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.25s ease';
        setTimeout(() => toast.remove(), 250);
      }, 3500);
    }
  },

  // --- CONFIRMATION MODAL ---
  modal: {
    confirm({ title, message, confirmText = 'CONFIRM ACTION', onConfirm, isDanger = false }) {
      let backdrop = document.getElementById('staff-confirm-modal');
      if (!backdrop) {
        backdrop = document.createElement('div');
        backdrop.id = 'staff-confirm-modal';
        backdrop.className = 'staff-modal-backdrop';
        backdrop.innerHTML = `
          <div class="staff-modal">
            <div class="staff-modal-header">
              <h3 id="confirm-modal-title" style="font-size:1rem; font-weight:700; text-transform:uppercase;"></h3>
              <button class="btn-staff-icon" id="confirm-modal-close" aria-label="Close modal">
                <i data-lucide="x" style="width:16px;height:16px;"></i>
              </button>
            </div>
            <div class="staff-modal-body">
              <p id="confirm-modal-message" style="font-size:0.875rem; color:var(--staff-gray-700); line-height:1.6;"></p>
            </div>
            <div class="staff-modal-footer">
              <button class="btn-staff btn-staff-outline" id="confirm-modal-cancel">CANCEL</button>
              <button class="btn-staff ${isDanger ? 'btn-staff-danger' : 'btn-staff-primary'}" id="confirm-modal-proceed"></button>
            </div>
          </div>
        `;
        document.body.appendChild(backdrop);
      }

      document.getElementById('confirm-modal-title').textContent = title;
      document.getElementById('confirm-modal-message').textContent = message;
      const proceedBtn = document.getElementById('confirm-modal-proceed');
      proceedBtn.textContent = confirmText;
      proceedBtn.className = `btn-staff ${isDanger ? 'btn-staff-danger' : 'btn-staff-primary'}`;

      backdrop.classList.add('open');
      if (window.lucide) window.lucide.createIcons();

      const closeModal = () => {
        backdrop.classList.remove('open');
      };

      document.getElementById('confirm-modal-close').onclick = closeModal;
      document.getElementById('confirm-modal-cancel').onclick = closeModal;
      backdrop.onclick = (e) => { if (e.target === backdrop) closeModal(); };

      proceedBtn.onclick = () => {
        closeModal();
        if (typeof onConfirm === 'function') onConfirm();
      };
    }
  },

  // --- UI CONTROLLER ---
  ui: {
    init(activeNav = '') {
      STAFF.guardAuth();
      STAFF.store.init();
      this.renderNavigation(activeNav);
      this.updateBadges();
      this.setupHeaderEvents();
      if (window.lucide) window.lucide.createIcons();
    },

    updateBadges() {
      const orders = STAFF.store.getOrders();
      const pendingCount = orders.filter(o => o.status === 'Pending').length;
      const notifs = STAFF.store.getNotifications();
      const unreadCount = notifs.filter(n => !n.read).length;
      const lowStockCount = STAFF.store.getInventory().filter(i => i.stock <= i.threshold).length;

      // Update sidebar badges
      const pendingBadge = document.getElementById('badge-pending-orders');
      if (pendingBadge) {
        pendingBadge.textContent = pendingCount;
        pendingBadge.style.display = pendingCount > 0 ? 'inline-block' : 'none';
      }

      const lowStockBadge = document.getElementById('badge-low-stock');
      if (lowStockBadge) {
        lowStockBadge.textContent = lowStockCount;
        lowStockBadge.style.display = lowStockCount > 0 ? 'inline-block' : 'none';
      }

      const notifDot = document.getElementById('topbar-notif-dot');
      if (notifDot) {
        notifDot.style.display = unreadCount > 0 ? 'block' : 'none';
      }
    },

    setupHeaderEvents() {
      // Populate user info from session
      const user = STAFF.getUser();
      if (user) {
        const nameEl = document.querySelector('.user-name');
        if (nameEl) nameEl.textContent = user.full_name;
        const avatarEl = document.querySelector('.user-avatar-circle');
        if (avatarEl) avatarEl.textContent = user.avatar_initials || 'ST';
        const roleEl = document.querySelector('.user-role-label');
        if (roleEl) roleEl.textContent = `${user.department || 'Retail Operations'} • Staff`;
      }

      // User Profile Menu Toggle
      const userChip = document.getElementById('staff-user-chip');
      const userDropdown = document.getElementById('staff-user-dropdown');
      if (userChip && userDropdown) {
        userChip.addEventListener('click', (e) => {
          e.stopPropagation();
          userDropdown.classList.toggle('show');
        });

        document.addEventListener('click', () => {
          userDropdown.classList.remove('show');
        });

        // Logout handler inside dropdown
        const logoutLinks = userDropdown.querySelectorAll('a[href*="index.html"], .staff-logout-btn');
        logoutLinks.forEach(link => {
          link.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
              await fetch('/api/auth/logout', { method: 'POST' });
            } catch (err) {}
            STAFF.clearAuth();
            window.location.href = '/authorization/login.html';
          });
        });
      }

      // Mobile Menu Toggle
      const mobileToggle = document.getElementById('mobile-menu-toggle');
      const sidebar = document.querySelector('.staff-sidebar');
      if (mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', (e) => {
          e.stopPropagation();
          sidebar.classList.toggle('open');
        });

        document.addEventListener('click', (e) => {
          if (!sidebar.contains(e.target) && e.target !== mobileToggle) {
            sidebar.classList.remove('open');
          }
        });
      }

      // Topbar Global Search
      const searchInput = document.getElementById('topbar-global-search');
      if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
              window.location.href = `orders.html?search=${encodeURIComponent(query)}`;
            }
          }
        });
      }
    },

    renderNavigation(activePage = '') {
      // Injected static sidebar & topbar HTML via page templates for maximum robustness
    }
  }
};
