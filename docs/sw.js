/**
 * Guru Kula Desam — Offline Hermitage Service Worker (PWA)
 * Caches core curriculum, scriptures, and styles for remote offline ashram study.
 */

const CACHE_NAME = 'gurukuladesam-v1';

const STATIC_ASSETS = [
  './',
  'index.html',
  'kalvi.html',
  'school.html',
  'about.html',
  'syllabus.html',
  'classes.html',
  'virtues.html',
  'higher-studies.html',
  'thirukkural.html',
  'saiva-neri.html',
  'sanmargam.html',
  'murugan.html',
  'sakthi.html',
  'vinayagar.html',
  'vaishnava.html',
  'irai-isai-virundhu.html',
  'assets/css/style.css',
  'assets/js/main.js',
  'manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Gurukula Cache] ஆசிரமக் களஞ்சியம் சேமிக்கப்படுகிறது (Caching static assets for offline use)...');
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('Non-blocking asset cache failure:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Skip YouTube and external third-party streaming
  if (url.origin.includes('youtube.com') || url.origin.includes('googlevideo.com') || url.origin.includes('youtu.be')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Return cached asset, fetch update in background (Stale-While-Revalidate)
        fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
          }
        }).catch(() => {});
        return cachedResponse;
      }

      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }

        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return networkResponse;
      }).catch(() => {
        // If offline and request is an HTML page, serve cached index.html
        if (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) {
          return caches.match('index.html');
        }
      });
    })
  );
});
