/**
 * BRI APPARELL — Centralized Authentication & Access Controller
 * Role-Based Access Control, Session Synchronization & Token Management
 */

const AuthPortal = {
  API_BASE: '/api',

  // Get current query params
  getParams() {
    return new URLSearchParams(window.location.search);
  },

  // Show contextual alert banner
  showBanner(message, type = 'error') {
    const banner = document.getElementById('auth-banner');
    if (!banner) return;
    
    banner.className = `auth-banner ${type}`;
    let iconName = 'alert-circle';
    if (type === 'success') iconName = 'check-circle';
    if (type === 'info') iconName = 'info';

    banner.innerHTML = `
      <i data-lucide="${iconName}" style="width:18px;height:18px;flex-shrink:0;"></i>
      <div>${message}</div>
    `;
    banner.style.display = 'flex';
    if (window.lucide) window.lucide.createIcons();
  },

  hideBanner() {
    const banner = document.getElementById('auth-banner');
    if (banner) banner.style.display = 'none';
  },

  // Setup password visibility toggles
  setupPasswordToggles() {
    const toggles = document.querySelectorAll('.password-toggle-btn');
    toggles.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const input = document.getElementById(targetId);
        if (!input) return;

        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        
        btn.innerHTML = isPassword 
          ? '<i data-lucide="eye-off" style="width:18px;height:18px;"></i>'
          : '<i data-lucide="eye" style="width:18px;height:18px;"></i>';
          
        if (window.lucide) window.lucide.createIcons();
      });
    });
  },

  // Check if session is already active and redirect appropriately
  async checkExistingSession() {
    const token = localStorage.getItem('bri_token') || localStorage.getItem('bri_admin_token');
    if (!token) return;

    try {
      const res = await fetch(`${this.API_BASE}/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();

      if (data.authenticated && data.user) {
        this.redirectByRole(data.user);
      }
    } catch (e) {
      // Offline / server reboot fallback
    }
  },

  // Centralized role redirection
  redirectByRole(user) {
    const params = this.getParams();
    const redirectUrl = params.get('redirect');

    if (user.role === 'admin') {
      window.location.href = (redirectUrl && redirectUrl.includes('/admin')) ? redirectUrl : '/admin/index.html';
    } else if (user.role === 'staff') {
      window.location.href = (redirectUrl && redirectUrl.includes('/staff')) ? redirectUrl : '/staff/dashboard.html';
    } else {
      // Customer
      if (redirectUrl && !redirectUrl.includes('/admin') && !redirectUrl.includes('/staff')) {
        window.location.href = redirectUrl;
      } else {
        window.location.href = '/account.html';
      }
    }
  },

  // Store authentication credentials across all module keys
  persistAuth(token, user) {
    // Primary unified keys
    localStorage.setItem('bri_token', token);
    localStorage.setItem('bri_user', JSON.stringify(user));

    // Admin module synchronization
    if (user.role === 'admin') {
      localStorage.setItem('bri_admin_token', token);
      localStorage.setItem('bri_admin_user', JSON.stringify(user));
    }

    // Staff module synchronization
    if (user.role === 'staff' || user.role === 'admin') {
      localStorage.setItem('bri_staff_token', token);
      localStorage.setItem('bri_staff_user', JSON.stringify(user));
    }
  },

  // Initialize Login Page
  initLogin() {
    const form = document.getElementById('login-form');
    if (!form) return;

    this.setupPasswordToggles();

    // Check URL parameters for contextual banners
    const params = this.getParams();
    const reason = params.get('reason');
    if (reason === 'checkout') {
      this.showBanner('Authentication Required: Please sign in or create an account to complete your purchase. Your bag items have been preserved.', 'info');
    } else if (reason === 'admin_required') {
      this.showBanner('Administrator Privileges Required: Please sign in with an executive administrator account to access the Admin Management Portal.', 'info');
    } else if (reason === 'staff_required') {
      this.showBanner('Staff Operations Login: Please sign in with an authorized retail or fulfillment staff account.', 'info');
    } else if (reason === 'session_expired') {
      this.showBanner('Your session has expired. Please sign in again to continue.', 'info');
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      this.hideBanner();

      const email = (document.getElementById('login-email').value || '').trim();
      const password = document.getElementById('login-password').value || '';
      const submitBtn = document.getElementById('login-submit-btn');
      const spinner = submitBtn.querySelector('.btn-spinner');
      const btnText = submitBtn.querySelector('.btn-text');

      if (!email || !password) {
        this.showBanner('Please provide both your registered email and password.', 'error');
        return;
      }

      // UI Loading state
      submitBtn.disabled = true;
      if (spinner) spinner.style.display = 'inline-block';
      if (btnText) btnText.textContent = 'AUTHENTICATING...';

      try {
        const res = await fetch(`${this.API_BASE}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || 'Authentication failed. Please verify your credentials.');
        }

        this.showBanner(`Welcome back, ${data.user.full_name}. Redirecting to your dashboard...`, 'success');
        this.persistAuth(data.token, data.user);

        setTimeout(() => {
          this.redirectByRole(data.user);
        }, 600);

      } catch (err) {
        this.showBanner(err.message, 'error');
        submitBtn.disabled = false;
        if (spinner) spinner.style.display = 'none';
        if (btnText) btnText.textContent = 'SIGN IN';
      }
    });

    // Preset Demo Fillers for testing
    const demoBadges = document.querySelectorAll('.demo-account-badge');
    demoBadges.forEach(badge => {
      badge.addEventListener('click', () => {
        const email = badge.getAttribute('data-email');
        const pass = badge.getAttribute('data-pass');
        if (email && pass) {
          document.getElementById('login-email').value = email;
          document.getElementById('login-password').value = pass;
          this.showBanner(`Demo credentials loaded for ${email}. Click Sign In to test.`, 'info');
        }
      });
    });
  },

  // Initialize Sign-Up Page
  initSignup() {
    const form = document.getElementById('signup-form');
    if (!form) return;

    this.setupPasswordToggles();

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      this.hideBanner();

      const fullName = (document.getElementById('reg-name').value || '').trim();
      const email = (document.getElementById('reg-email').value || '').trim().toLowerCase();
      const phone = (document.getElementById('reg-phone').value || '').trim();
      const password = document.getElementById('reg-password').value || '';
      const confirmPassword = document.getElementById('reg-confirm-password').value || '';
      const street = (document.getElementById('reg-street')?.value || '').trim();
      const city = (document.getElementById('reg-city')?.value || '').trim();
      const province = (document.getElementById('reg-province')?.value || '').trim();
      const postalCode = (document.getElementById('reg-postal')?.value || '').trim();

      const submitBtn = document.getElementById('signup-submit-btn');
      const spinner = submitBtn.querySelector('.btn-spinner');
      const btnText = submitBtn.querySelector('.btn-text');

      // Validations
      if (!fullName) {
        this.showBanner('Please provide your full legal or preferred name.', 'error');
        return;
      }
      if (!email || !email.includes('@')) {
        this.showBanner('Please enter a valid email address.', 'error');
        return;
      }
      if (password.length < 6) {
        this.showBanner('Password must be at least 6 characters in length.', 'error');
        return;
      }
      if (password !== confirmPassword) {
        this.showBanner('Passwords do not match. Please re-enter your password confirmation.', 'error');
        return;
      }

      // UI Loading state
      submitBtn.disabled = true;
      if (spinner) spinner.style.display = 'inline-block';
      if (btnText) btnText.textContent = 'CREATING ACCOUNT...';

      try {
        const res = await fetch(`${this.API_BASE}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            full_name: fullName,
            email: email,
            phone: phone,
            password: password,
            street: street,
            city: city || 'Taguig',
            province: province || 'Metro Manila',
            postal_code: postalCode || '1634'
          })
        });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || 'Registration failed. Please check your information.');
        }

        this.showBanner(`Account created successfully! Welcome to BRI APPARELL, ${data.user.full_name}. Redirecting...`, 'success');
        this.persistAuth(data.token, data.user);

        setTimeout(() => {
          this.redirectByRole(data.user);
        }, 800);

      } catch (err) {
        this.showBanner(err.message, 'error');
        submitBtn.disabled = false;
        if (spinner) spinner.style.display = 'none';
        if (btnText) btnText.textContent = 'CREATE ACCOUNT';
      }
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();
  AuthPortal.checkExistingSession();
});
