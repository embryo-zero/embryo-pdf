// Embryo PDF (2026-11-16): the upstream offline cache is switched off so every visitor gets our current pages.
// This worker clears what the old one stored, unregisters itself and reloads open pages once.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil((async () => {
  for (const k of await caches.keys()) await caches.delete(k);
  await self.registration.unregister();
  for (const c of await self.clients.matchAll({type: "window"})) c.navigate(c.url);
})()));
