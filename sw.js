/* Guarda los archivos de la app en el dispositivo para que abra sin internet.
   Si se cambia algún archivo, se debe cambiar también el número de VERSION. */
const VERSION = "sunny-spa-v1";

const ARCHIVOS = [
  "./",
  "index.html",
  "app.py",
  "manifest.webmanifest",
  "icons/icon-180.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png",
  "pyodide/pyodide.js",
  "pyodide/pyodide.asm.js",
  "pyodide/pyodide.asm.wasm",
  "pyodide/python_stdlib.zip",
  "pyodide/pyodide-lock.json"
];

self.addEventListener("install", evento => {
  evento.waitUntil(caches.open(VERSION).then(cache => cache.addAll(ARCHIVOS)));
  self.skipWaiting();
});

self.addEventListener("activate", evento => {
  evento.waitUntil(
    caches.keys().then(nombres =>
      Promise.all(nombres.filter(n => n !== VERSION).map(n => caches.delete(n)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", evento => {
  if (evento.request.method !== "GET") return;
  evento.respondWith(
    caches.match(evento.request).then(guardado => guardado || fetch(evento.request))
  );
});
