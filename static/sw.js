// MedScribe service worker — caches the app shell so the interface
// loads instantly and works offline once installed. API calls
// (/health, /upload, /records) are NOT cached here — they always
// hit the live backend, since they depend on real-time local
// OCR/AI processing rather than static content.

const CACHE_NAME = "medscribe-shell-v1";
const APP_SHELL = [
  "/static/index.html",
  "/static/manifest.json",
  "/static/icon.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Only handle GET requests for our own static app-shell files.
  // Everything else (API calls) goes straight to the network.
  if (event.request.method !== "GET" || !url.pathname.startsWith("/static/")) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const networkFetch = fetch(event.request)
        .then((response) => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => cached);
      return cached || networkFetch;
    })
  );
});