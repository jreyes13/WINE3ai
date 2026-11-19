// WINE³ai — Service Worker (Modo Offline PWA)
// Versión de caché: wine3ai-cache-v2 (Identidad Visual Triqueta WINE³ai)

const CACHE_NAME = 'wine3ai-cache-v2';

const PRECACHE_ASSETS = [
  './',
  './index_es.html',
  './index.html',
  './winepedia.html',
  './map.html',
  './grapes.html',
  './style.css',
  './grapes.css',
  './app.js',
  './grapes.js',
  './libs/sommelier_engine.js',
  './libs/sommelier_ui.js',
  './data/study_cards.js',
  './data/winepedia_articles.js',
  './data/grape_varieties.json',
  './data/pairing_rules.js',
  './assets/logo.svg',
  './assets/logo_horizontal.svg',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/apple-touch-icon.png',
  './manifest.json'
];

// 1. INSTALACIÓN: Precarga de activos críticos y forzar activación inmediata
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[WINE³ai SW] Precacheando versión v2...');
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('[WINE³ai SW] Fallo parcial precarga:', err);
      });
    })
  );
});

// 2. ACTIVACIÓN: Eliminar inmediatamente todas las cachés antiguas
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[WINE³ai SW] Purgando caché obsoleta:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. ESTRATEGIA DE RED:
// - Para navegación HTML: Network-First (actualizaciones instantáneas cuando hay red)
// - Para estáticos (imágenes, css, js): Stale-While-Revalidate con cache fallback
self.addEventListener('fetch', (event) => {
  const req = event.request;

  if (req.method !== 'GET' || !req.url.startsWith('http')) {
    return;
  }

  const isNavigation = req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html');

  if (isNavigation) {
    // Network First para HTML
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const copy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          }
          return networkResponse;
        })
        .catch(() => caches.match(req).then((cached) => cached || caches.match('./index_es.html')))
    );
    return;
  }

  // Stale-While-Revalidate para recursos estáticos
  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      const fetchPromise = fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const copy = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          }
          return networkResponse;
        })
        .catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});
