---
name: pwa-development
description: Progressive Web Apps - service workers, caching strategies, offline, Workbox
---

# PWA Development Skill

*Load with: base.md*

**Purpose:** Build Progressive Web Apps that work offline, install like native apps, and deliver fast, reliable experiences across all devices.

---

## Core PWA Requirements

```
┌─────────────────────────────────────────────────────────────────┐
│  THE THREE PILLARS OF PWA                                       │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  1. HTTPS                                                       │
│     Required for service workers and security.                  │
│     localhost allowed for development.                          │
│                                                                 │
│  2. SERVICE WORKER                                              │
│     JavaScript that runs in background.                         │
│     Enables offline, caching, push notifications.               │
│                                                                 │
│  3. WEB APP MANIFEST                                            │
│     JSON file describing app metadata.                          │
│     Enables installation and app-like experience.               │
├─────────────────────────────────────────────────────────────────┤
│  INSTALLABILITY CRITERIA (Chrome)                               │
│  ─────────────────────────────────────────────────────────────  │
│  • HTTPS (or localhost)                                         │
│  • Service worker with fetch handler                            │
│  • Web app manifest with: name, icons (192px + 512px),          │
│    start_url, display: standalone/fullscreen/minimal-ui         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Web App Manifest

### Required Fields

```json
{
  "name": "My Progressive Web App",
  "short_name": "MyPWA",
  "description": "A description of what the app does",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512-maskable.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

### Enhanced Manifest (Full Features)

```json
{
  "name": "My Progressive Web App",
  "short_name": "MyPWA",
  "description": "A full-featured PWA",
  "start_url": "/?source=pwa",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#ffffff",
  "theme_color": "#3367D6",
  "dir": "ltr",
  "lang": "en",
  "categories": ["productivity", "utilities"],

  "icons": [
    { "src": "/icons/icon-72.png", "sizes": "72x72", "type": "image/png" },
    { "src": "/icons/icon-96.png", "sizes": "96x96", "type": "image/png" },
    { "src": "/icons/icon-128.png", "sizes": "128x128", "type": "image/png" },
    { "src": "/icons/icon-144.png", "sizes": "144x144", "type": "image/png" },
    { "src": "/icons/icon-152.png", "sizes": "152x152", "type": "image/png" },
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-384.png", "sizes": "384x384", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],

  "screenshots": [
    {
      "src": "/screenshots/desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    },
    {
      "src": "/screenshots/mobile.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ],

  "shortcuts": [
    {
      "name": "New Item",
      "short_name": "New",
      "description": "Create a new item",
      "url": "/new?source=shortcut",
      "icons": [{ "src": "/icons/shortcut-new.png", "sizes": "192x192" }]
    }
  ],

  "share_target": {
    "action": "/share",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url",
      "files": [{ "name": "files", "accept": ["image/*"] }]
    }
  },

  "protocol_handlers": [
    {
      "protocol": "web+myapp",
      "url": "/handle?url=%s"
    }
  ],

  "file_handlers": [
    {
      "action": "/open-file",
      "accept": {
        "text/plain": [".txt"]
      }
    }
  ]
}
```

### Manifest Checklist

- [ ] `name` and `short_name` defined
- [ ] `start_url` set (use query param for analytics)
- [ ] `display` set to `standalone` or `fullscreen`
- [ ] Icons: 192x192 and 512x512 minimum
- [ ] Maskable icon included for Android adaptive icons
- [ ] `theme_color` matches app design
- [ ] `background_color` for splash screen
- [ ] Screenshots for richer install UI (optional)
- [ ] Shortcuts for quick actions (optional)

---

## Service Worker Patterns

### Basic Service Worker

```javascript
// sw.js
const CACHE_NAME = 'app-cache-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/styles/main.css',
  '/scripts/app.js',
  '/offline.html'
];

// Install: Cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate: Clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch: Serve from cache, fall back to network
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((cached) => cached || fetch(event.request))
      .catch(() => caches.match('/offline.html'))
  );
});
```

### Registration

```javascript
// main.js
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/'
      });
      console.log('SW registered:', registration.scope);
    } catch (error) {
      console.error('SW registration failed:', error);
    }
  });
}
```

---

## Caching Strategies

### Strategy Selection Guide

| Strategy | Use Case | Description |
|----------|----------|-------------|
| **Cache First** | Static assets (CSS, JS, images) | Check cache, fall back to network |
| **Network First** | API responses, dynamic content | Try network, fall back to cache |
| **Stale While Revalidate** | Semi-static content (avatars, articles) | Serve cache immediately, update in background |
| **Network Only** | Non-cacheable requests (analytics) | Always use network |
| **Cache Only** | Offline-only assets | Only serve from cache |

### Cache First (Offline First)

```javascript
// Best for: Static assets that rarely change
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image' ||
      event.request.destination === 'style' ||
      event.request.destination === 'script') {
    event.respondWith(
      caches.match(event.request)
        .then((cached) => {
          if (cached) return cached;
          return fetch(event.request).then((response) => {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, clone);
            });
            return response;
          });
        })
    );
  }
});
```

### Network First (Fresh First)

```javascript
// Best for: API data, frequently updated content
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, clone);
          });
          return response;
        })
        .catch(() => caches.match(event.request))
    );
  }
});
```

### Stale While Revalidate

```javascript
// Best for: Content that's okay to be slightly outdated
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/articles/')) {
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((cached) => {
          const fetchPromise = fetch(event.request).then((response) => {
            cache.put(event.request, response.clone());
            return response;
          });
          return cached || fetchPromise;
        });
      })
    );
  }
});
```

---

## Workbox (Recommended)

### Why Workbox?

- Battle-tested caching strategies
- Precaching with revision management
- Background sync for offline forms
- Automatic cache cleanup
- TypeScript support

### Installation

```bash
npm install workbox-webpack-plugin  # Webpack
npm install @vite-pwa/vite-plugin   # Vite
```

### Workbox with Vite

```javascript
// vite.config.js
import { VitePWA } from 'vite-plugin-pwa';

export default {
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt', 'apple-touch-icon.png'],
      manifest: {
        name: 'My App',
        short_name: 'App',
        theme_color: '#ffffff',
        icons: [
          { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\.example\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24 // 24 hours
              }
            }
          },
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif)$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'image-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
              }
            }
          }
        ]
      }
    })
  ]
};
```

### Workbox Manual Service Worker

```javascript
// sw.js
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// Precache static assets (generated by build tool)
precacheAndRoute(self.__WB_MANIFEST);

// Cache images
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
      })
    ]
  })
);

// Cache API responses
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-responses',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 24 * 60 * 60 // 24 hours
      })
    ]
  })
);

// Cache page navigations
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({
    cacheName: 'pages',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] })
    ]
  })
);
```

---

## Offline Experience

### Offline Page

```html
<!-- offline.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Offline - App Name</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      background: #f5f5f5;
    }
    .offline-content {
      text-align: center;
      padding: 2rem;
    }
    .offline-icon { font-size: 4rem; }
    h1 { color: #333; }
    p { color: #666; }
    button {
      background: #3367D6;
      color: white;
      border: none;
      padding: 0.75rem 1.5rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 1rem;
    }
  </style>
</head>
<body>
  <div class="offline-content">
    <div class="offline-icon">📡</div>
    <h1>You're offline</h1>
    <p>Check your connection and try again.</p>
    <button onclick="location.reload()">Retry</button>
  </div>
</body>
</html>
```

### Offline Detection

```javascript
// Online/offline status handling
function updateOnlineStatus() {
  const status = navigator.onLine ? 'online' : 'offline';
  document.body.dataset.connectionStatus = status;

  if (!navigator.onLine) {
    showNotification('You are offline. Some features may be unavailable.');
  }
}

window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
updateOnlineStatus();
```

### Background Sync (Queue Offline Actions)

```javascript
// sw.js with Workbox
import { BackgroundSyncPlugin } from 'workbox-background-sync';
import { registerRoute } from 'workbox-routing';
import { NetworkOnly } from 'workbox-strategies';

const bgSyncPlugin = new BackgroundSyncPlugin('formQueue', {
  maxRetentionTime: 24 * 60 // Retry for 24 hours
});

registerRoute(
  ({ url }) => url.pathname === '/api/submit',
  new NetworkOnly({
    plugins: [bgSyncPlugin]
  }),
  'POST'
);
```

```javascript
// main.js - Queue form submission
async function submitForm(data) {
  try {
    const response = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return response.json();
  } catch (error) {
    // Will be retried by background sync when online
    showNotification('Saved offline. Will sync when connected.');
  }
}
```

---

## App-Like Features

### Install Prompt

```javascript
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  showInstallButton();
});

async function installApp() {
  if (!deferredPrompt) return;

  deferredPrompt.prompt();
  const { outcome } = await deferredPrompt.userChoice;

  console.log(`User ${outcome === 'accepted' ? 'accepted' : 'dismissed'} install`);
  deferredPrompt = null;
  hideInstallButton();
}

window.addEventListener('appinstalled', () => {
  console.log('App installed');
  deferredPrompt = null;
});
```

### Detecting Standalone Mode

```javascript
// Check if running as installed PWA
function isInstalledPWA() {
  return window.matchMedia('(display-mode: standalone)').matches ||
         window.navigator.standalone === true; // iOS
}

// Listen for display mode changes
window.matchMedia('(display-mode: standalone)')
  .addEventListener('change', (e) => {
    console.log('Display mode:', e.matches ? 'standalone' : 'browser');
  });
```

### Push Notifications

```javascript
// Request permission
async function requestNotificationPermission() {
  const permission = await Notification.requestPermission();
  if (permission === 'granted') {
    await subscribeToPush();
  }
  return permission;
}

// Subscribe to push
async function subscribeToPush() {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
  });

  // Send subscription to server
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription)
  });
}

// sw.js - Handle push events
self.addEventListener('push', (event) => {
  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icons/icon-192.png',
      badge: '/icons/badge-72.png',
      data: { url: data.url }
    })
  );
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
```

### Share Target

```javascript
// sw.js - Handle share target
self.addEventListener('fetch', (event) => {
  if (event.request.url.endsWith('/share') &&
      event.request.method === 'POST') {
    event.respondWith((async () => {
      const formData = await event.request.formData();
      const title = formData.get('title');
      const text = formData.get('text');
      const url = formData.get('url');

      // Store or process shared content
      // Redirect to app with shared data
      return Response.redirect(`/?shared=true&title=${encodeURIComponent(title)}`);
    })());
  }
});
```

---

## Performance Optimization

### Critical Rendering Path

```html
<!-- Inline critical CSS -->
<style>
  /* Critical above-the-fold styles */
</style>

<!-- Preload important resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/scripts/app.js" as="script">

<!-- Defer non-critical CSS -->
<link rel="stylesheet" href="/styles/main.css" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/styles/main.css"></noscript>
```

### Image Optimization

```html
<!-- Responsive images -->
<img
  src="/images/hero-800.webp"
  srcset="
    /images/hero-400.webp 400w,
    /images/hero-800.webp 800w,
    /images/hero-1200.webp 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Hero image"
  loading="lazy"
  decoding="async"
>

<!-- Modern formats with fallback -->
<picture>
  <source srcset="/images/hero.avif" type="image/avif">
  <source srcset="/images/hero.webp" type="image/webp">
  <img src="/images/hero.jpg" alt="Hero image" loading="lazy">
</picture>
```

### Code Splitting

```javascript
// Dynamic imports for route-based splitting
const routes = {
  '/': () => import('./pages/Home.js'),
  '/about': () => import('./pages/About.js'),
  '/settings': () => import('./pages/Settings.js')
};

async function loadPage(path) {
  const loader = routes[path];
  if (loader) {
    const module = await loader();
    return module.default;
  }
}
```

---

## Testing PWA

### Lighthouse Audit

```bash
# Run Lighthouse from CLI
npx lighthouse https://your-app.com --view

# Key metrics to check:
# - PWA badge (installable, offline-ready)
# - Performance score
# - Best practices
# - Accessibility
```

### Manual Testing Checklist

- [ ] **Installability**
  - [ ] Install prompt appears on desktop Chrome
  - [ ] Can be added to home screen on mobile
  - [ ] App opens in standalone mode after install

- [ ] **Offline Support**
  - [ ] App loads when offline (airplane mode)
  - [ ] Cached pages display correctly
  - [ ] Offline fallback page shows for uncached routes
  - [ ] Background sync works when coming back online

- [ ] **Performance**
  - [ ] First Contentful Paint < 1.8s
  - [ ] Largest Contentful Paint < 2.5s
  - [ ] Time to Interactive < 3.8s
  - [ ] Cumulative Layout Shift < 0.1

- [ ] **Service Worker**
  - [ ] SW registers successfully
  - [ ] Static assets cached on install
  - [ ] SW updates correctly (new version)
  - [ ] No stale cache issues

- [ ] **Manifest**
  - [ ] All required fields present
  - [ ] Icons display correctly
  - [ ] Theme color applied
  - [ ] Splash screen shows on launch

### Testing Service Worker Updates

```javascript
// Force update check
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.ready.then((registration) => {
    registration.update();
  });
}

// Listen for updates
navigator.serviceWorker.addEventListener('controllerchange', () => {
  // New service worker activated
  window.location.reload();
});
```

---

## Project Structure

```
project/
├── public/
│   ├── manifest.json           # Web app manifest
│   ├── sw.js                   # Service worker (if not bundled)
│   ├── offline.html            # Offline fallback page
│   ├── robots.txt
│   └── icons/
│       ├── icon-72.png
│       ├── icon-96.png
│       ├── icon-128.png
│       ├── icon-144.png
│       ├── icon-152.png
│       ├── icon-192.png
│       ├── icon-384.png
│       ├── icon-512.png
│       ├── icon-maskable.png   # For adaptive icons
│       ├── apple-touch-icon.png
│       └── favicon.ico
├── src/
│   ├── sw.js                   # Service worker source (if bundled)
│   ├── pwa/
│   │   ├── install.js          # Install prompt handling
│   │   ├── offline.js          # Offline detection
│   │   └── push.js             # Push notification handling
│   └── ...
└── tests/
    └── pwa/
        ├── manifest.test.js
        ├── sw.test.js
        └── offline.test.js
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing maskable icon | Add icon with `"purpose": "maskable"` |
| No offline fallback | Create `offline.html` and cache it |
| Cache never expires | Use `ExpirationPlugin` with Workbox |
| SW caches too aggressively | Use appropriate strategies per resource type |
| No update mechanism | Implement `skipWaiting()` + reload prompt |
| Broken install prompt | Ensure manifest meets all criteria |
| No HTTPS in production | Configure SSL certificate |
| Large cache size | Set `maxEntries` and `maxAgeSeconds` |
| Stale API responses | Use `NetworkFirst` for dynamic data |
| Missing start_url tracking | Add query param: `/?source=pwa` |

---

## PWA Development Checklist

### Before Launch

- [ ] HTTPS configured (production)
- [ ] Manifest complete with all required fields
- [ ] Icons in all required sizes (192, 512, maskable)
- [ ] Service worker registered and working
- [ ] Offline page created and cached
- [ ] Cache strategies defined for all resource types
- [ ] Install prompt handling implemented
- [ ] Lighthouse PWA audit passes

### After Launch

- [ ] Monitor cache sizes
- [ ] Test SW updates don't break app
- [ ] Track PWA installs via analytics
- [ ] Test on multiple devices/browsers
- [ ] Monitor Core Web Vitals
- [ ] Set up push notification flow (if needed)

---

## Framework-Specific Guides

### Next.js

```bash
npm install next-pwa
```

```javascript
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development'
});

module.exports = withPWA({
  // Your Next.js config
});
```

### Create React App

```bash
# CRA 4+ has PWA support built-in
npx create-react-app my-pwa --template cra-template-pwa
```

### Vite (Any Framework)

```bash
npm install vite-plugin-pwa -D
```

See Workbox with Vite section above for configuration.

---

## Quick Reference

### Caching Strategy Cheat Sheet

```
Static Assets (CSS, JS, images)     → Cache First
API Responses                        → Network First
User-generated content              → Stale While Revalidate
Analytics, non-cacheable            → Network Only
Offline-only assets                 → Cache Only
```

### Manifest Minimum Requirements

```json
{
  "name": "App Name",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### Service Worker Lifecycle

```
1. Register → 2. Install → 3. Activate → 4. Fetch
     ↓              ↓            ↓           ↓
  Load app    Cache assets  Clean old   Serve requests
                            caches      from cache/network
```
