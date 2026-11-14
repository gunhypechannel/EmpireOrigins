/* Empire Origins offline support: the page is fetched fresh when online (so updates arrive on the next launch),
   art is cached the first time it loads so the game starts instantly and plays offline. */
const V="eo-v122";
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>c.addAll(["./","manifest.webmanifest","icon-192.png","icon-512.png"])))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n!==V).map(n=>caches.delete(n)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);if(u.pathname.includes("/music/")||u.pathname.includes("/voice/"))return; /* streamed media (range requests) goes straight to the network */
 if(u.origin===location.origin&&u.pathname.includes("/art/")){e.respondWith(caches.open(V).then(c=>c.match(r).then(h=>h||fetch(r).then(res=>{if(res.ok)c.put(r,res.clone());return res}))));return}
 if(r.mode==="navigate"){e.respondWith(fetch(r).then(res=>{const cl=res.clone();caches.open(V).then(c=>c.put("./",cl));return res}).catch(()=>caches.match("./")));return}
 if(u.host.endsWith("fonts.googleapis.com")||u.host.endsWith("fonts.gstatic.com")){e.respondWith(caches.open(V).then(c=>c.match(r).then(h=>h||fetch(r).then(res=>{c.put(r,res.clone());return res}))))}});
