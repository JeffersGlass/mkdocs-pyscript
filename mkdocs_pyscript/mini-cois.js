/*! coi-serviceworker v0.1.7 - Guido Zuidhof and contributors, licensed under MIT */
/*! mini-coi - Andrea Giammarchi and contributors, licensed under MIT */
/*mini-coi.js. Verison 0.2.1. Copyright 2023 Andrea Giammarchi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*/

(({ document: d, navigator: { serviceWorker: s } }) => {
    if (d) {
      const { currentScript: c } = d;
      s.register(c.src, { scope: c.getAttribute('scope') || '.' }).then(r => {
        r.addEventListener('updatefound', () => location.reload());
        if (r.active && !s.controller) location.reload();
      });
    }
    else {
      addEventListener('install', () => skipWaiting());
      addEventListener('activate', e => e.waitUntil(clients.claim()));
      addEventListener('fetch', e => {
        const { request: r } = e;
        if (r.cache === 'only-if-cached' && r.mode !== 'same-origin') return;
        e.respondWith(fetch(r).then(r => {
          const { body, status, statusText } = r;
          if (!status || status > 399) return r;
          const h = new Headers(r.headers);
          h.set('Cross-Origin-Opener-Policy', 'same-origin');
          h.set('Cross-Origin-Embedder-Policy', 'require-corp');
          h.set('Cross-Origin-Resource-Policy', 'cross-origin');
          return new Response(body, { status, statusText, headers: h });
        }));
      });
    }
  })(self);