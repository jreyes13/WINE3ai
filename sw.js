// WINE³ai — Service Worker (Modo Offline PWA)
// Versión de caché: v20261119_v1

const CACHE_NAME = 'wine3ai-cache-v1';

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
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/apple-touch-icon.png',
  './manifest.json'
];

// 1. INSTALACIÓN: Precarga de activos críticos en la caché local
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[WINE³ai SW] Precacheando archivos críticos para modo offline...');
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('[WINE³ai SW] Fallo precacheando algunos elementos no críticos:', err);
      });
    })
  );
});

// 2. ACTIVACIÓN: Limpieza de versiones obsoletas de caché
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[WINE³ai SW] Eliminando caché obsoleta:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. ESTRATEGIA DE RED / CACHÉ: Stale-While-Revalidate con Fallback Offline
self.addEventListener('fetch', (event) => {
  const req = event.request;

  // Ignorar peticiones que no sean GET o esquemas extraños (chrome-extension, etc.)
  if (req.method !== 'GET' || !req.url.startsWith('http')) {
    return;
  }

  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      // Si tenemos copia en caché, la devolvemos de inmediato (velocidad offline)
      // y en segundo plano intentamos actualizar desde la red si hay internet
      const fetchPromise = fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(req, responseToCache);
            });
          }
          return networkResponse;
        })
        .catch(() => {
          // Si no hay red, cachedResponse salva la petición
          return cachedResponse;
        });

      return cachedResponse || fetchPromise;
    })
  );
});
