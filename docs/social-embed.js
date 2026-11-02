/* RKK social v3 — three compact Instagram links, no third-party feed widget. */
(function () {
  'use strict';
  var host = document.getElementById('rkk-social-unified');
  if (!host || host.dataset.socialVersion === '3') return;
  host.dataset.socialVersion = '3';
  host.dataset.initialized = '1';
  var BASE = 'https://glesima.github.io/kehaketut-feed/';
  var PROFILE = 'https://www.instagram.com/kehaketut/';
  host.innerHTML = String.raw`
<style>
#rkk-social-unified{--rk-red:#b91c2b;--rk-ink:#171a1f;--rk-muted:#687681;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;max-width:1160px;margin:24px auto 32px;color:var(--rk-ink);line-height:1.5}
#rkk-social-unified *{box-sizing:border-box}
#rkk-social-unified .rkk-rule{height:2px;margin:0 0 29px;background:linear-gradient(90deg,transparent,#d6dbe0 13%,#d6dbe0 46%,#b91c2b 46%,#b91c2b 54%,#d6dbe0 87%,transparent)}
#rkk-social-unified .rkk-kicker{font-size:11px;font-weight:850;letter-spacing:.14em;color:#a7192b}
#rkk-social-unified h2{font-size:clamp(26px,3vw,32px)!important;letter-spacing:-.02em;line-height:1.15;margin:5px 0 22px!important;font-weight:850;color:#171a1f}
#rkk-social-unified .rkk-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start;gap:16px}
#rkk-social-unified .rkk-channel{min-width:0;border:1px solid #e2e5e9;border-radius:14px;background:#fff;padding:19px 18px}
#rkk-social-unified .rkk-channel-head{display:flex;justify-content:space-between;align-items:start;gap:8px;min-height:76px;padding-bottom:12px;border-bottom:1px solid #eceff2;margin-bottom:14px}
#rkk-social-unified .rkk-channel h3{font-size:21px!important;line-height:1.2!important;font-weight:850!important;margin:0 0 6px!important;color:#171a1f!important}
#rkk-social-unified .rkk-channel p{margin:0;color:var(--rk-muted);font-size:12px;line-height:1.6}
#rkk-social-unified a{color:#a7192b!important;text-decoration:none!important;font-size:12px;font-weight:800}
#rkk-social-unified a:focus-visible{outline:3px solid #b91c2b;outline-offset:3px}
#rkk-social-unified .rkk-channel-head>a{white-space:nowrap}
#rkk-social-unified .rkk-ig-list{display:grid;gap:12px}
#rkk-social-unified .rkk-ig-card{display:grid;grid-template-columns:88px minmax(0,1fr);gap:13px;align-items:center;border:1px solid #e1e5e9;border-radius:11px;padding:12px;min-width:0;min-height:118px;background:#fff;transition:border-color .15s,background .15s}
#rkk-social-unified .rkk-ig-card:hover{border-color:#c45b68;background:#fffbfb}
#rkk-social-unified .rkk-ig-image{position:relative;display:flex;align-items:center;justify-content:center;width:88px;height:96px;overflow:hidden;border-radius:7px;background:#171d25;color:#fff}
#rkk-social-unified .rkk-ig-image img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 22%;margin:0;display:block}
#rkk-social-unified .rkk-ig-play{position:absolute;left:8px;bottom:8px;display:flex;align-items:center;justify-content:center;width:25px;height:25px;border-radius:50%;background:rgba(13,18,24,.82);color:white;font-size:12px;line-height:1}
#rkk-social-unified .rkk-ig-fallback{font-size:11px;letter-spacing:.05em}
#rkk-social-unified .rkk-ig-copy{min-width:0;display:grid;gap:5px}
#rkk-social-unified .rkk-ig-meta{color:#78828c;font-size:10px;font-weight:500;letter-spacing:.01em}
#rkk-social-unified .rkk-ig-title{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;color:#202830;font-size:14px;font-weight:800;line-height:1.3;overflow-wrap:anywhere}
#rkk-social-unified .rkk-ig-excerpt{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:12px;line-height:1.45;font-weight:400;color:#5e6a76;overflow-wrap:anywhere}
#rkk-social-unified .rkk-ig-link{font-size:11px;font-weight:800}
#rkk-social-unified .rkk-ig-footer{display:block;margin-top:15px;padding-top:13px;border-top:1px solid #eceff2}
#rkk-social-unified .rkk-ig-status{display:block;margin:10px 0 0;color:#78828c;font-size:10px;line-height:1.5;font-weight:400}
#rkk-social-unified .rkk-ig-empty{padding:20px 14px;border:1px solid #e1e5e9;border-radius:10px;color:#687681;font-size:13px;line-height:1.6}
#rkk-social-unified iframe{display:block;width:100%;height:530px;border:0;background:transparent}
@media(max-width:700px){#rkk-social-unified .rkk-grid{grid-template-columns:1fr}#rkk-social-unified .rkk-channel{padding:16px}#rkk-social-unified .rkk-channel-head{min-height:0}}
@media(max-width:360px){#rkk-social-unified .rkk-ig-card{grid-template-columns:64px minmax(0,1fr);gap:10px;padding:10px}#rkk-social-unified .rkk-ig-image{width:64px;height:88px}}
@media(prefers-reduced-motion:reduce){#rkk-social-unified .rkk-ig-card{transition:none}}
</style>
<div class="rkk-rule"></div><div class="rkk-kicker">KUVIA JA KUULUMISIA</div>
<h2>Seuraa Kehä-Kettuja</h2>
<div class="rkk-grid">
<section class="rkk-channel" aria-label="Instagram">
<div class="rkk-channel-head"><div><h3>Instagram</h3><p>Kolme uusinta julkaisua</p></div><a href="https://www.instagram.com/kehaketut/" target="_blank" rel="noopener noreferrer">Avaa ↗</a></div>
<div class="rkk-ig-list" aria-live="polite"><div class="rkk-ig-empty">Haetaan seuran julkaisuja…</div></div>
<a class="rkk-ig-footer" href="https://www.instagram.com/kehaketut/" target="_blank" rel="noopener noreferrer">Katso lisää Instagramissa ↗</a>
<small class="rkk-ig-status">Videot ja kokonaiset julkaisut avautuvat Instagramissa.</small>
</section>
<section class="rkk-channel" aria-label="Facebook">
<div class="rkk-channel-head"><div><h3>Facebook</h3><p>Seuran tiedotteet ja kuulumiset</p></div><a href="https://www.facebook.com/160875127258478/" target="_blank" rel="noopener noreferrer">Avaa ↗</a></div>
<iframe id="rkk-social-facebook-frame" loading="lazy" scrolling="no" title="Kehä-Kettujen Facebook-julkaisut" src="https://glesima.github.io/kehaketut-feed/facebook.html?embed=1"></iframe>
</section></div>`;
  var frame = host.querySelector('#rkk-social-facebook-frame');
  window.addEventListener('message', function (e) {
    if (!frame || e.origin !== 'https://glesima.github.io' || e.source !== frame.contentWindow) return;
    if (!e.data || e.data.type !== 'RKK_WIDGET_HEIGHT' || e.data.view !== 'facebook') return;
    var h = Number(e.data.height);
    if (Number.isFinite(h) && h > 70 && h < 2000) frame.style.height = Math.ceil(h + 12) + 'px';
  });
  var list = host.querySelector('.rkk-ig-list');
  var status = host.querySelector('.rkk-ig-status');
  function node(tag, cls, text) { var n=document.createElement(tag);n.className=cls;if(text!=null)n.textContent=text;return n; }
  function postURL(value) {
    try {var u=new URL(value);if(u.protocol!=='https:' || !['instagram.com','www.instagram.com'].includes(u.hostname) || u.username || u.password || u.port || !/^\/(reel|p|tv)\/[A-Za-z0-9_-]+\/$/.test(u.pathname)) return null;return u.origin+u.pathname;}catch(e){return null;}
  }
  function dateLabel(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value||'')) return '';
    var d=new Date(value+'T12:00:00Z');
    if(!Number.isFinite(d.getTime()) || d.toISOString().slice(0,10)!==value)return '';
    return Number(value.slice(8,10))+'.'+Number(value.slice(5,7))+'.'+value.slice(0,4);
  }
  function fail() {list.replaceChildren(node('div','rkk-ig-empty','Julkaisunostot eivät juuri nyt lataudu. Kaikki julkaisut löydät alla olevasta Instagram-linkistä.'));}
  function render(d) {
    if(!d || d.brand_id!==7632678 || d.instagram_username!=='kehaketut' || !Array.isArray(d.posts))throw Error('Wrong Instagram feed');
    var seen=new Set(), cards=[];
    d.posts.slice().sort(function(a,b){return String(b.published_at||b.date||'').localeCompare(String(a.published_at||a.date||''));}).some(function(p){
      var url=postURL(p.url), date=dateLabel(p.date);
      if(!url || !date || seen.has(url) || typeof p.title!=='string' || !p.title.trim())return false;
      seen.add(url);
      var a=node('a','rkk-ig-card');a.href=url;a.target='_blank';a.rel='noopener noreferrer';
      a.setAttribute('aria-label',p.title.slice(0,150)+' – avaa Instagramissa (uusi välilehti)');
      var image=node('span','rkk-ig-image');image.setAttribute('aria-hidden','true');
      image.append(node('span','rkk-ig-fallback',p.type==='REEL'?'REEL':'KUVA'));
      var code=new URL(url).pathname.split('/')[2];
      if(p.thumbnail==='assets/instagram/'+code+'.jpg'){
        var img=document.createElement('img');img.alt='';img.loading='lazy';img.decoding='async';img.width=88;img.height=96;img.referrerPolicy='no-referrer';img.onerror=function(){this.remove();};img.src=BASE+p.thumbnail;image.append(img);
      }
      if(p.type==='REEL')image.append(node('span','rkk-ig-play','▶'));
      var copy=node('span','rkk-ig-copy');
      var time=node('time','rkk-ig-meta',date+(p.type==='REEL'?' · REEL':''));time.dateTime=p.date;
      copy.append(time,node('span','rkk-ig-title',p.title.slice(0,150)));
      if(p.excerpt)copy.append(node('span','rkk-ig-excerpt',String(p.excerpt).slice(0,240)));
      copy.append(node('span','rkk-ig-link',p.type==='REEL'?'Katso Instagramissa ↗':'Avaa julkaisu ↗'));
      a.append(image,copy);cards.push(a);return cards.length===3;
    });
    if(!cards.length){fail();return;}
    list.replaceChildren.apply(list,cards);
    var sync=dateLabel(String(d.synced_at||'').slice(0,10));
    status.textContent='Lähde: @kehaketut'+(sync?' · päivitetty '+sync:'')+'. Videot avautuvat Instagramissa.';
  }
  var controller=new AbortController(), timer=setTimeout(function(){controller.abort();},8000);
  fetch(BASE+'instagram.json?v='+Math.floor(Date.now()/300000),{cache:'no-store',credentials:'omit',signal:controller.signal}).then(function(r){if(!r.ok)throw Error('Instagram feed unavailable');return r.json();}).then(render).catch(fail).finally(function(){clearTimeout(timer);});
})();
