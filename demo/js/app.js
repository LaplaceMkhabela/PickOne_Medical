/*
 * Shared demo runtime: mock session (localStorage), navbar, flash messages,
 * route guarding and small DOM helpers. Mirrors Flask-Login + base.html.
 */
(function (global) {
  'use strict';

  const SESSION_KEY = 'pickone_demo_session';
  const FLASH_KEY = 'pickone_demo_flash';

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function writeJSON(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) { /* storage unavailable */ }
  }

  const Session = {
    get() { return readJSON(SESSION_KEY, null); },

    create(user) {
      const session = {
        user_name: user.user_name,
        user_id: user.user_id,
        user_email: user.user_email,
        user_role: user.user_role,
        subscription_tier: user.subscription_tier || 'trial'
      };
      writeJSON(SESSION_KEY, session);
      return session;
    },

    update(fields) {
      const current = Session.get();
      if (!current) return null;
      const next = Object.assign(current, fields);
      writeJSON(SESSION_KEY, next);
      return next;
    },

    destroy() {
      try { localStorage.removeItem(SESSION_KEY); } catch (e) { /* noop */ }
    },

    dashboardUrl() {
      const user = Session.get();
      if (!user) return '/login';
      if (user.user_role === 'doctor') return '/doctor/dashboard';
      if (user.user_role === 'nurse') return '/nurse/dashboard';
      if (user.user_role === 'patient') return '/patient/dashboard';
      return '/login';
    }
  };

  const Flash = {
    push(category, message) {
      const queue = readJSON(FLASH_KEY, []);
      queue.push({ category, message });
      writeJSON(FLASH_KEY, queue);
    },

    consume() {
      const queue = readJSON(FLASH_KEY, []);
      if (queue.length) {
        try { localStorage.removeItem(FLASH_KEY); } catch (e) { /* noop */ }
      }
      return queue;
    },

    render(container) {
      const target = container || document.getElementById('flashZone');
      if (!target) return;
      const queue = Flash.consume();
      if (!queue.length) return;
      target.innerHTML = queue.map((item) => {
        const isError = item.category === 'error';
        return '<div class="p-4 mb-4 text-sm rounded-lg ' + (
          isError
            ? 'bg-red-50 text-red-800 border border-red-200'
            : 'bg-green-50 text-green-800 border border-green-200'
        ) + '" role="alert">' + escapeHtml(item.message) + '</div>';
      }).join('');
    }
  };

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function queryString(name) {
    return new URLSearchParams(window.location.search).get(name) || '';
  }

  function redirect(url) {
    window.location.href = url;
  }

  function redirectWithQuery(base, params) {
    const search = new URLSearchParams();
    Object.keys(params || {}).forEach((key) => {
      if (params[key] !== '' && params[key] != null) search.set(key, params[key]);
    });
    const qs = search.toString();
    window.location.href = base + (qs ? '?' + qs : '');
  }

  /* Replaces base.html's authenticated navbar. */
  function renderNavbar(active) {
    const user = Session.get();
    const root = document.getElementById('navbar');
    if (!root) return;
    if (!user) { root.innerHTML = ''; return; }

    const dashboard = Session.dashboardUrl();
    const links = [
      { href: dashboard, label: 'Dashboard', key: 'dashboard' },
      { href: '/pricing', label: 'Pricing', key: 'pricing' },
      { href: '/support', label: 'Support', key: 'support' }
    ].map((link) => {
      const isActive = link.key === active;
      return '<a href="' + link.href + '" class="text-sm font-medium transition-colors ' + (
        isActive ? 'text-blue-600' : 'text-gray-500 hover:text-blue-600'
      ) + '">' + link.label + '</a>';
    }).join('');

    root.innerHTML = `
      <nav class="bg-white border-b border-gray-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center gap-8">
              <a href="${dashboard}" class="text-2xl font-bold text-blue-600 tracking-tight hover:opacity-80 transition-opacity">PickOne<span class="text-gray-800">Med</span></a>
              <div class="hidden sm:flex items-center gap-6">${links}</div>
            </div>

            <div class="flex items-center gap-4">
              <div class="text-right hidden sm:block">
                <p class="text-sm font-semibold text-gray-900">${escapeHtml(user.user_name)}</p>
                <p class="text-xs font-medium text-blue-600 uppercase tracking-wider">${escapeHtml(user.user_role)}</p>
              </div>

              <div class="relative">
                <img class="h-10 w-10 rounded-full border-2 border-white shadow-sm object-cover"
                     src="https://ui-avatars.com/api/?name=${encodeURIComponent(user.user_name)}&background=EBF5FF&color=1E3A8A&bold=true"
                     alt="User Avatar">
                <span class="absolute bottom-0 right-0 block h-3 w-3 rounded-full bg-green-500 ring-2 ring-white"></span>
              </div>

              <a href="/logout" class="ml-4 text-sm font-medium text-gray-500 hover:text-red-600 transition-colors">Logout</a>
            </div>
          </div>
          <div class="sm:hidden flex items-center gap-4 pb-3 -mt-1">${links}</div>
        </div>
      </nav>`;
  }

  /*
   * Guard a page. Returns the session or null (and redirects when null).
   * options: { role, active, anonymous }
   */
  function guard(options) {
    const opts = options || {};
    const user = Session.get();

    if (opts.anonymous) {
      if (user) { redirect(Session.dashboardUrl()); return null; }
      Flash.render();
      return null;
    }

    if (!user) {
      Flash.push('error', 'Please sign in to access the dashboard.');
      redirect('/login');
      return null;
    }

    if (opts.role && user.user_role !== opts.role) {
      Flash.push('error', 'Unauthorized access.');
      redirect(Session.dashboardUrl());
      return null;
    }

    renderNavbar(opts.active);
    Flash.render();
    return user;
  }

  function demoBanner() {
    if (document.getElementById('demoBanner')) return;
    const banner = document.createElement('div');
    banner.id = 'demoBanner';
    banner.className = 'bg-amber-50 border-b border-amber-200 text-amber-800 text-xs text-center py-1.5 px-4';
    banner.innerHTML = 'Interactive demo — all data is mocked locally in your browser. Seed accounts use password <strong>password123</strong>.';
    document.body.insertBefore(banner, document.body.firstChild);
  }

  global.POM = Object.assign(global.POM || {}, {
    Session,
    Flash,
    guard,
    demoBanner,
    escapeHtml,
    queryString,
    redirect,
    redirectWithQuery
  });
})(window);
