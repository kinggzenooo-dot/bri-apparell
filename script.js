/**
 * BRI APPARELL - Global JavaScript Engine
 * Modular Vanilla JS for state management, UI interactions, and e-commerce flows
 */

// Global State Controller
const BRI = {
  // Format currency in Philippine Peso
  formatPrice(amount) {
    return `₱${Number(amount).toLocaleString('en-PH', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
  },

  // --- LOCAL STORAGE STATE MANAGERS ---
  cart: {
    getItems() {
      try {
        return JSON.parse(localStorage.getItem('bri_cart')) || [];
      } catch (e) {
        return [];
      }
    },
    saveItems(items) {
      localStorage.setItem('bri_cart', JSON.stringify(items));
      BRI.ui.updateHeaderCounts();
    },
    addItem(productId, size = 'M', color = null, quantity = 1) {
      const items = this.getItems();
      const product = PRODUCTS.find(p => p.id === productId);
      if (!product) return;

      const chosenColor = color || (product.colors && product.colors[0] ? product.colors[0].name : 'Standard');
      const existingIndex = items.findIndex(item => item.id === productId && item.size === size && item.color === chosenColor);

      if (existingIndex > -1) {
        items[existingIndex].quantity += quantity;
      } else {
        items.push({
          id: productId,
          size: size,
          color: chosenColor,
          quantity: quantity,
          addedAt: new Date().toISOString()
        });
      }
      this.saveItems(items);
      BRI.toast.show(`${product.name} (${size}) added to your bag.`, 'bag', 'View Bag', 'cart.html');
    },
    updateQuantity(index, quantity) {
      const items = this.getItems();
      if (items[index]) {
        if (quantity <= 0) {
          items.splice(index, 1);
        } else {
          items[index].quantity = quantity;
        }
        this.saveItems(items);
      }
    },
    removeItem(index) {
      const items = this.getItems();
      if (items[index]) {
        const removed = items.splice(index, 1)[0];
        this.saveItems(items);
        const prod = PRODUCTS.find(p => p.id === removed.id);
        BRI.toast.show(`Removed ${prod ? prod.name : 'item'} from bag.`);
      }
    },
    clear() {
      localStorage.removeItem('bri_cart');
      BRI.ui.updateHeaderCounts();
    },
    getCount() {
      return this.getItems().reduce((acc, item) => acc + item.quantity, 0);
    },
    getSubtotal() {
      const items = this.getItems();
      return items.reduce((sum, item) => {
        const product = PRODUCTS.find(p => p.id === item.id);
        if (!product) return sum;
        const price = product.isSale && product.salePrice ? product.salePrice : product.price;
        return sum + (price * item.quantity);
      }, 0);
    }
  },

  wishlist: {
    getItems() {
      try {
        return JSON.parse(localStorage.getItem('bri_wishlist')) || [];
      } catch (e) {
        return [];
      }
    },
    saveItems(items) {
      localStorage.setItem('bri_wishlist', JSON.stringify(items));
      BRI.ui.updateHeaderCounts();
    },
    has(productId) {
      return this.getItems().includes(productId);
    },
    toggle(productId) {
      let items = this.getItems();
      const product = PRODUCTS.find(p => p.id === productId);
      const isAdding = !items.includes(productId);

      if (isAdding) {
        items.push(productId);
        BRI.toast.show(`Saved ${product ? product.name : 'item'} to your wishlist.`, 'heart', 'View Wishlist', 'wishlist.html');
      } else {
        items = items.filter(id => id !== productId);
        BRI.toast.show(`Removed from wishlist.`, 'heart');
      }
      this.saveItems(items);
      return isAdding;
    },
    remove(productId) {
      let items = this.getItems().filter(id => id !== productId);
      this.saveItems(items);
      BRI.toast.show('Removed item from wishlist.');
    },
    getCount() {
      return this.getItems().length;
    }
  },

  promo: {
    getApplied() {
      try {
        return JSON.parse(localStorage.getItem('bri_promo')) || null;
      } catch (e) {
        return null;
      }
    },
    apply(code) {
      const found = PROMO_CODES.find(p => p.code.toUpperCase() === code.trim().toUpperCase());
      if (!found) {
        return { success: false, message: 'Invalid promo code.' };
      }
      localStorage.setItem('bri_promo', JSON.stringify(found));
      return { success: true, promo: found, message: `Promo code ${found.code} applied!` };
    },
    remove() {
      localStorage.removeItem('bri_promo');
    }
  },

  // Unified API Client for Centralized Python Backend
  async api(endpoint, options = {}) {
    const token = localStorage.getItem('bri_token');
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
      const res = await fetch(endpoint, { ...options, headers });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
      return data;
    } catch (err) {
      console.warn(`[BRI API] ${endpoint} request failed:`, err.message);
      throw err;
    }
  },

  auth: {
    getToken() {
      return localStorage.getItem('bri_token');
    },
    getUser() {
      try {
        return JSON.parse(localStorage.getItem('bri_user')) || null;
      } catch (e) {
        return null;
      }
    },
    async login(email, password = 'password123') {
      try {
        const res = await BRI.api('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email, password })
        });
        localStorage.setItem('bri_token', res.token);
        localStorage.setItem('bri_user', JSON.stringify(res.user));
        BRI.toast.show(`Welcome back, ${res.user.full_name}.`);
        return res.user;
      } catch (err) {
        // Fallback for offline simulation if backend is down
        const user = {
          name: email.split('@')[0],
          full_name: email.split('@')[0],
          email: email,
          phone: '+63 917 892 4567',
          city: 'Taguig',
          province: 'Metro Manila',
          postal_code: '1634'
        };
        localStorage.setItem('bri_user', JSON.stringify(user));
        BRI.toast.show(`Welcome, ${user.name}.`);
        return user;
      }
    },
    async register(name, email, password = 'password123', phone = '') {
      try {
        const res = await BRI.api('/api/auth/register', {
          method: 'POST',
          body: JSON.stringify({ full_name: name, email, password, phone })
        });
        localStorage.setItem('bri_token', res.token);
        localStorage.setItem('bri_user', JSON.stringify(res.user));
        BRI.toast.show(`Account created! Welcome, ${res.user.full_name}.`);
        return res.user;
      } catch (err) {
        throw err;
      }
    },
    async logout() {
      try {
        await BRI.api('/api/auth/logout', { method: 'POST' });
      } catch (e) {}
      localStorage.removeItem('bri_token');
      localStorage.removeItem('bri_user');
      localStorage.removeItem('bri_admin_token');
      localStorage.removeItem('bri_admin_user');
      localStorage.removeItem('bri_staff_token');
      localStorage.removeItem('bri_staff_user');
      BRI.toast.show('You have been signed out.');
    },
    isLoggedIn() {
      return !!this.getUser();
    }
  },

  orders: {
    async getAll() {
      const user = BRI.auth.getUser();
      const token = BRI.auth.getToken();
      try {
        const url = user ? `/api/orders?email=${encodeURIComponent(user.email)}` : '/api/orders';
        const res = await BRI.api(url);
        if (res && res.orders) {
          localStorage.setItem('bri_orders', JSON.stringify(res.orders));
          return res.orders;
        }
      } catch (e) {}

      // Fallback to local cache
      try {
        return JSON.parse(localStorage.getItem('bri_orders')) || [];
      } catch (e) {
        return [];
      }
    },
    async addOrder(orderData) {
      try {
        const res = await BRI.api('/api/orders', {
          method: 'POST',
          body: JSON.stringify(orderData)
        });
        if (res && res.order) {
          const cached = JSON.parse(localStorage.getItem('bri_orders') || '[]');
          cached.unshift(res.order);
          localStorage.setItem('bri_orders', JSON.stringify(cached));
          return res.order;
        }
      } catch (e) {
        console.warn('Backend order placement failed, falling back to local store:', e);
      }

      // Local fallback
      const orders = JSON.parse(localStorage.getItem('bri_orders') || '[]');
      orders.unshift(orderData);
      localStorage.setItem('bri_orders', JSON.stringify(orders));
      return orderData;
    }
  },

  // --- TOAST NOTIFICATION SYSTEM ---
  toast: {
    show(message, iconType = 'info', actionText = null, actionUrl = null) {
      let container = document.getElementById('bri-toast-container');
      if (!container) {
        container = document.createElement('div');
        container.id = 'bri-toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
      }

      const toast = document.createElement('div');
      toast.className = 'toast';

      let iconSvg = '<i data-lucide="check" style="width:18px;height:18px;"></i>';
      if (iconType === 'bag') iconSvg = '<i data-lucide="shopping-bag" style="width:18px;height:18px;"></i>';
      if (iconType === 'heart') iconSvg = '<i data-lucide="heart" style="width:18px;height:18px;"></i>';
      if (iconType === 'alert') iconSvg = '<i data-lucide="alert-circle" style="width:18px;height:18px;"></i>';

      toast.innerHTML = `
        <div style="display:flex;align-items:center;gap:0.75rem;">
          ${iconSvg}
          <span>${message}</span>
        </div>
        ${actionText && actionUrl ? `<a href="${actionUrl}" class="toast-action-btn">${actionText}</a>` : ''}
      `;

      container.appendChild(toast);
      if (window.lucide) window.lucide.createIcons();

      setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }
  },

  // --- UI CONTROLLER & MODALS ---
  ui: {
    init() {
      this.renderHeaderAndFooter();
      this.updateHeaderCounts();
      this.updateAuthNavigation();
      this.setupSearchOverlay();
      this.setupQuickViewModal();
      this.setupMobileMenu();
      this.setupHeaderScroll();
      if (window.lucide) window.lucide.createIcons();
    },

    updateAuthNavigation() {
      const user = BRI.auth.getUser();
      const utilityNavs = document.querySelectorAll('.utility-nav');
      const mobileFooters = document.querySelectorAll('.mobile-drawer-footer');

      if (user) {
        document.querySelectorAll('a[href="account.html"], a[href="/account.html"]').forEach(link => {
          link.title = `Signed in as ${user.full_name || user.email}`;
        });

        utilityNavs.forEach(nav => {
          if (!nav.querySelector('.nav-logout-btn')) {
            const logoutLink = document.createElement('a');
            logoutLink.href = '#';
            logoutLink.className = 'icon-btn nav-logout-btn';
            logoutLink.title = 'Sign Out';
            logoutLink.setAttribute('aria-label', 'Sign Out');
            logoutLink.innerHTML = '<i data-lucide="log-out"></i>';
            logoutLink.addEventListener('click', async (e) => {
              e.preventDefault();
              await BRI.auth.logout();
              window.location.href = '/authorization/login.html';
            });
            nav.appendChild(logoutLink);
          }
        });

        mobileFooters.forEach(footer => {
          if (!footer.querySelector('.mobile-logout-link')) {
            const mobileLogout = document.createElement('a');
            mobileLogout.href = '#';
            mobileLogout.className = 'mobile-utility-link mobile-logout-link';
            mobileLogout.innerHTML = '<i data-lucide="log-out" style="width:18px;height:18px;"></i> Sign Out';
            mobileLogout.addEventListener('click', async (e) => {
              e.preventDefault();
              await BRI.auth.logout();
              window.location.href = '/authorization/login.html';
            });
            footer.appendChild(mobileLogout);
          }
        });
      } else {
        document.querySelectorAll('.nav-logout-btn, .mobile-logout-link').forEach(el => el.remove());
        document.querySelectorAll('a[href="account.html"]').forEach(link => {
          link.href = '/authorization/login.html?redirect=account.html';
        });
      }
    },

    updateHeaderCounts() {
      const bagCount = BRI.cart.getCount();
      const wishlistCount = BRI.wishlist.getCount();

      document.querySelectorAll('.bag-count-badge').forEach(el => {
        el.textContent = bagCount;
        el.style.display = bagCount > 0 ? 'flex' : 'none';
      });

      document.querySelectorAll('.wishlist-count-badge').forEach(el => {
        el.textContent = wishlistCount;
        el.style.display = wishlistCount > 0 ? 'flex' : 'none';
      });
    },

    setupHeaderScroll() {
      const header = document.querySelector('.site-header');
      if (!header) return;
      window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
          header.classList.add('scrolled');
        } else {
          header.classList.remove('scrolled');
        }
      });
    },

    setupMobileMenu() {
      const toggle = document.querySelector('.mobile-nav-toggle');
      const drawer = document.querySelector('.mobile-nav-drawer');
      const closeBtn = document.querySelector('.mobile-drawer-close');

      if (toggle && drawer) {
        toggle.addEventListener('click', () => {
          drawer.classList.add('open');
          document.body.classList.add('no-scroll');
        });
      }

      if (closeBtn && drawer) {
        closeBtn.addEventListener('click', () => {
          drawer.classList.remove('open');
          document.body.classList.remove('no-scroll');
        });
      }

      if (drawer) {
        drawer.addEventListener('click', (e) => {
          if (e.target === drawer) {
            drawer.classList.remove('open');
            document.body.classList.remove('no-scroll');
          }
        });
      }
    },

    setupSearchOverlay() {
      const searchBtns = document.querySelectorAll('.trigger-search-btn');
      let overlay = document.getElementById('bri-search-overlay');

      if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'bri-search-overlay';
        overlay.className = 'search-overlay';
        overlay.innerHTML = `
          <div class="search-overlay-inner">
            <div class="search-bar-wrap">
              <input type="text" id="bri-search-input" class="search-main-input" placeholder="Search apparel, categories, materials..." autocomplete="off">
              <button class="search-close-btn" id="bri-search-close" aria-label="Close search">
                <i data-lucide="x" style="width:28px;height:28px;"></i>
              </button>
            </div>
            <div style="margin-top: 1.5rem; display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
              <span class="eyebrow" style="color: rgba(255,255,255,0.6); margin-bottom: 0;">TRENDING:</span>
              <a href="shop.html?category=Tops" style="color:#fff; font-size:0.75rem; text-decoration:underline; letter-spacing:0.05em;">Oversized Tees</a>
              <a href="shop.html?category=Outerwear" style="color:#fff; font-size:0.75rem; text-decoration:underline; letter-spacing:0.05em;">Wool Coats</a>
              <a href="shop.html?category=Bottoms" style="color:#fff; font-size:0.75rem; text-decoration:underline; letter-spacing:0.05em;">Wide-Leg Trousers</a>
              <a href="promotions.html" style="color:#fff; font-size:0.75rem; text-decoration:underline; letter-spacing:0.05em;">Seasonal Sale</a>
            </div>
            <div class="search-results-area" id="bri-search-results">
              <p style="color: rgba(255,255,255,0.5); font-size: 0.875rem; margin-top: 2rem;">Type at least 2 characters to explore BRI APPARELL pieces.</p>
            </div>
          </div>
        `;
        document.body.appendChild(overlay);
      }

      const input = document.getElementById('bri-search-input');
      const resultsContainer = document.getElementById('bri-search-results');
      const closeBtn = document.getElementById('bri-search-close');

      const openSearch = () => {
        overlay.classList.add('open');
        document.body.classList.add('no-scroll');
        setTimeout(() => input.focus(), 150);
      };

      const closeSearch = () => {
        overlay.classList.remove('open');
        document.body.classList.remove('no-scroll');
        input.value = '';
      };

      searchBtns.forEach(btn => btn.addEventListener('click', openSearch));
      if (closeBtn) closeBtn.addEventListener('click', closeSearch);

      // Instant search typing
      if (input) {
        input.addEventListener('input', (e) => {
          const query = e.target.value.trim().toLowerCase();
          if (query.length < 2) {
            resultsContainer.innerHTML = `<p style="color: rgba(255,255,255,0.5); font-size: 0.875rem; margin-top: 2rem;">Type at least 2 characters to explore BRI APPARELL pieces.</p>`;
            return;
          }

          const matches = PRODUCTS.filter(p => 
            p.name.toLowerCase().includes(query) ||
            p.category.toLowerCase().includes(query) ||
            p.shortDesc.toLowerCase().includes(query) ||
            p.description.toLowerCase().includes(query)
          );

          if (matches.length === 0) {
            resultsContainer.innerHTML = `
              <div style="text-align:center; padding: 4rem 1rem; color: #fff;">
                <p style="font-size: 1.125rem; font-weight:600; margin-bottom: 0.5rem;">NO PIECES FOUND FOR "${query.toUpperCase()}"</p>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.875rem;">Check your spelling or explore our complete catalog.</p>
                <a href="shop.html" class="btn btn-primary-white btn-sm" style="margin-top: 1.5rem;">EXPLORE ALL PRODUCTS</a>
              </div>
            `;
            return;
          }

          resultsContainer.innerHTML = `
            <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
              ${matches.map(p => `
                <a href="product-detail.html?id=${p.id}" style="display:flex; flex-direction:column; gap:0.6rem; color:#fff; group">
                  <div style="aspect-ratio:3/4; overflow:hidden; background:#222;">
                    <img src="${p.images[0]}" alt="${p.name}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.4s ease;">
                  </div>
                  <span style="font-size:0.6875rem; font-weight:700; color:rgba(255,255,255,0.6); letter-spacing:0.1em; text-transform:uppercase;">${p.category}</span>
                  <span style="font-size:0.875rem; font-weight:600; line-height:1.3;">${p.name}</span>
                  <span style="font-size:0.875rem; font-weight:700;">${BRI.formatPrice(p.isSale ? p.salePrice : p.price)}</span>
                </a>
              `).join('')}
            </div>
          `;
        });
      }
    },

    setupQuickViewModal() {
      let modal = document.getElementById('bri-quickview-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'bri-quickview-modal';
        modal.className = 'modal-backdrop';
        modal.innerHTML = `
          <div class="modal-box" id="bri-quickview-content">
            <!-- Dynamic PDP Content -->
          </div>
        `;
        document.body.appendChild(modal);
      }

      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          modal.classList.remove('open');
          document.body.classList.remove('no-scroll');
        }
      });
    },

    openQuickView(productId) {
      const product = PRODUCTS.find(p => p.id === productId);
      if (!product) return;

      const modal = document.getElementById('bri-quickview-modal');
      const content = document.getElementById('bri-quickview-content');

      let selectedSize = product.sizes.find(s => s.inStock)?.size || product.sizes[0].size;
      let selectedColor = product.colors[0]?.name || '';

      content.innerHTML = `
        <button class="modal-close-btn" id="qv-close-btn" aria-label="Close">
          <i data-lucide="x" style="width:20px;height:20px;"></i>
        </button>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 2rem; padding: 2rem;">
          <div>
            <div style="aspect-ratio: 3/4; overflow:hidden; background:var(--color-bg-subtle);">
              <img id="qv-main-img" src="${product.images[0]}" alt="${product.name}" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div style="display:flex; gap:0.5rem; margin-top:0.75rem;">
              ${product.images.slice(0, 3).map((img, i) => `
                <div class="qv-thumb" data-src="${img}" style="width:60px; aspect-ratio:3/4; cursor:pointer; border:1px solid ${i === 0 ? 'var(--color-black)' : 'var(--border-color)'};">
                  <img src="${img}" alt="Thumb" style="width:100%; height:100%; object-fit:cover;">
                </div>
              `).join('')}
            </div>
          </div>
          <div style="display:flex; flex-direction:column; gap:1.25rem;">
            <div>
              <span class="eyebrow">${product.category}</span>
              <h2 style="font-size:1.35rem; font-weight:700; margin-bottom:0.5rem;">${product.name}</h2>
              <div style="display:flex; align-items:baseline; gap:0.75rem;">
                <span style="font-size:1.25rem; font-weight:700;">${BRI.formatPrice(product.isSale ? product.salePrice : product.price)}</span>
                ${product.isSale ? `<span style="font-size:0.9375rem; color:var(--text-muted); text-decoration:line-through;">${BRI.formatPrice(product.price)}</span>` : ''}
              </div>
            </div>

            <p style="font-size:0.875rem; color:var(--text-secondary); line-height:1.6;">${product.shortDesc}</p>

            <div>
              <div class="pdp-selector-label-row" style="margin-bottom:0.5rem;">
                <span>Color: <strong id="qv-color-text">${selectedColor}</strong></span>
              </div>
              <div class="color-swatch-list">
                ${product.colors.map((c, i) => `
                  <button class="color-swatch-btn qv-swatch ${i === 0 ? 'active' : ''}" data-name="${c.name}" style="background-color:${c.hex};" title="${c.name}"></button>
                `).join('')}
              </div>
            </div>

            <div>
              <div class="pdp-selector-label-row" style="margin-bottom:0.5rem;">
                <span>Size: <strong id="qv-size-text">${selectedSize}</strong></span>
              </div>
              <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:0.5rem;">
                ${product.sizes.map(s => `
                  <button class="size-btn qv-size-btn ${s.size === selectedSize ? 'active' : ''}" data-size="${s.size}" ${!s.inStock ? 'disabled' : ''}>
                    ${s.size}
                  </button>
                `).join('')}
              </div>
            </div>

            <div style="display:flex; gap:0.75rem; margin-top:0.5rem;">
              <button class="btn btn-primary btn-block" id="qv-add-to-bag">ADD TO BAG</button>
            </div>

            <a href="product-detail.html?id=${product.id}" class="btn-text" style="text-align:center; font-size:0.75rem;">VIEW FULL PRODUCT DETAILS</a>
          </div>
        </div>
      `;

      modal.classList.add('open');
      document.body.classList.add('no-scroll');
      if (window.lucide) window.lucide.createIcons();

      // Quick View Event Listeners
      document.getElementById('qv-close-btn').addEventListener('click', () => {
        modal.classList.remove('open');
        document.body.classList.remove('no-scroll');
      });

      // Thumbnail click
      content.querySelectorAll('.qv-thumb').forEach(thumb => {
        thumb.addEventListener('click', () => {
          document.getElementById('qv-main-img').src = thumb.getAttribute('data-src');
          content.querySelectorAll('.qv-thumb').forEach(t => t.style.borderColor = 'var(--border-color)');
          thumb.style.borderColor = 'var(--color-black)';
        });
      });

      // Swatch click
      content.querySelectorAll('.qv-swatch').forEach(sw => {
        sw.addEventListener('click', () => {
          content.querySelectorAll('.qv-swatch').forEach(s => s.classList.remove('active'));
          sw.classList.add('active');
          selectedColor = sw.getAttribute('data-name');
          document.getElementById('qv-color-text').textContent = selectedColor;
        });
      });

      // Size click
      content.querySelectorAll('.qv-size-btn').forEach(sb => {
        sb.addEventListener('click', () => {
          content.querySelectorAll('.qv-size-btn').forEach(s => s.classList.remove('active'));
          sb.classList.add('active');
          selectedSize = sb.getAttribute('data-size');
          document.getElementById('qv-size-text').textContent = selectedSize;
        });
      });

      // Add to bag
      document.getElementById('qv-add-to-bag').addEventListener('click', () => {
        BRI.cart.addItem(product.id, selectedSize, selectedColor, 1);
        modal.classList.remove('open');
        document.body.classList.remove('no-scroll');
      });
    },

    renderHeaderAndFooter() {
      // Header and Footer can be embedded statically in HTML or dynamically verified
    }
  },

  // --- PRODUCT CARD HTML GENERATOR ---
  renderProductCard(product) {
    const isWishlisted = BRI.wishlist.has(product.id);
    const primaryImg = product.images[0];
    const secondaryImg = product.images[1] || product.images[0];

    return `
      <div class="product-card" data-id="${product.id}" data-category="${product.category}" data-price="${product.isSale ? product.salePrice : product.price}">
        <div class="product-image-wrap">
          <div class="product-badge-wrap">
            ${product.isNew ? `<span class="badge badge-dark">NEW</span>` : ''}
            ${product.isSale ? `<span class="badge badge-sale">SALE</span>` : ''}
            ${product.tag && !product.isNew && !product.isSale ? `<span class="badge badge-outline">${product.tag}</span>` : ''}
          </div>
          <button class="product-wishlist-btn ${isWishlisted ? 'active' : ''}" data-wishlist-id="${product.id}" aria-label="Add to wishlist">
            <i data-lucide="heart" style="width:16px;height:16px;"></i>
          </button>
          <a href="product-detail.html?id=${product.id}">
            <img src="${primaryImg}" alt="${product.name}" class="product-img-primary" loading="lazy">
            <img src="${secondaryImg}" alt="${product.name} back view" class="product-img-secondary" loading="lazy">
          </a>
          <button class="product-quick-view-btn" data-quickview-id="${product.id}">
            <i data-lucide="eye" style="width:15px;height:15px;"></i>
            QUICK VIEW
          </button>
        </div>
        <div class="product-meta">
          <span class="product-category">${product.category}</span>
          <a href="product-detail.html?id=${product.id}" class="product-title">${product.name}</a>
          <div class="product-price-wrap">
            <span class="product-price ${product.isSale ? 'sale' : ''}">${BRI.formatPrice(product.isSale ? product.salePrice : product.price)}</span>
            ${product.isSale ? `<span class="product-price-original">${BRI.formatPrice(product.price)}</span>` : ''}
          </div>
        </div>
      </div>
    `;
  },

  // Attach card event listeners (Wishlist & Quick View)
  bindProductCardEvents(container = document) {
    container.querySelectorAll('.product-wishlist-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const id = btn.getAttribute('data-wishlist-id');
        const added = BRI.wishlist.toggle(id);
        btn.classList.toggle('active', added);
      });
    });

    container.querySelectorAll('.product-quick-view-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const id = btn.getAttribute('data-quickview-id');
        BRI.ui.openQuickView(id);
      });
    });

    if (window.lucide) window.lucide.createIcons();
  }
};

// Auto-initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  BRI.ui.init();
});
