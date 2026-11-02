/* RKK social v4 — compact native cards in two equal-height channel panels. */
(function () {
  'use strict';
  var host = document.getElementById('rkk-social-unified');
  if (!host || host.dataset.socialVersion === '4') return;
  host.dataset.socialVersion = '4';
  host.dataset.initialized = '1';
  var BASE = 'https://glesima.github.io/kehaketut-feed/';
  host.innerHTML = String.raw`
<style>
#rkk-social-unified{--rk-red:#b91c2b;--rk-ink:#171a1f;--rk-muted:#687681;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;max-width:1160px;margin:24px auto 32px;color:var(--rk-ink);line-height:1.5}
#rkk-social-unified *{box-sizing:border-box}
#rkk-social-unified .rkk-rule{height:2px;margin:0 0 29px;background:linear-gradient(90deg,transparent,#d6dbe0 13%,#d6dbe0 46%,#b91c2b 46%,#b91c2b 54%,#d6dbe0 54%,#d6dbe0 87%,transparent)}
#rkk-social-unified .rkk-kicker{font-size:11px;font-weight:850;letter-spacing:.14em;color:#a7192b}
#rkk-social-unified h2{font-size:clamp(26px,3vw,32px)!important;letter-spacing:-.02em;line-height:1.15;margin:5px 0 22px!important;font-weight:850;color:#171a1f}
#rkk-social-unified .rkk-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:stretch;gap:16px}
#rkk-social-unified .rkk-channel{display:grid;grid-template-rows:auto 1fr auto;min-width:0;border:1px solid #e2e5e9;border-radius:14px;background:#fff;padding:19px 18px}
#rkk-social-unified .rkk-channel-head{display:flex;justify-content:space-between;align-items:start;gap:8px;min-height:76px;padding-bottom:12px;border-bottom:1px solid #eceff2;margin-bottom:14px}
#rkk-social-unified .rkk-channel h3{font-size:21px!important;line-height:1.2!important;font-weight:850!important;margin:0 0 6px!important;color:#171a1f!important}
#rkk-social-unified .rkk-channel p{margin:0;color:var(--rk-muted);font-size:12px;line-height:1.6}
#rkk-social-unified a{color:#a7192b!important;text-decoration:none!important;font-size:12px;font-weight:800}
#rkk-social-unified a:focus-visible{outline:3px solid #b91c2b;outline-offset:3px}
#rkk-social-unified .rkk-channel-head>a{white-space:nowrap}
#rkk-social-unified .rkk-post-list{display:grid;grid-auto-rows:1fr;align-content:start;gap:12px;min-width:0}
#rkk-social-unified .rkk-post-card{display:grid;gap:13px;align-items:center;border:1px solid #e1e5e9;border-radius:11px;padding:12px;min-width:0;min-height:122px;background:#fff;transition:border-color .15s,background .15s}
#rkk-social-unified .rkk-ig-card{grid-template-columns:88px minmax(0,1fr)}
#rkk-social-unified .rkk-fb-card{grid-template-columns:minmax(0,1fr)}
#rkk-social-unified .rkk-post-card:hover{border-color:#c45b68;background:#fffbfb}
#rkk-social-unified .rkk-ig-image{position:relative;display:flex;align-items:center;justify-content:center;width:88px;height:96px;overflow:hidden;border-radius:7px;background:#171d25;color:#fff}
#rkk-social-unified .rkk-ig-image img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 22%;margin:0;display:block}
#rkk-social-unified .rkk-ig-play{position:absolute;left:8px;bottom:8px;display:flex;align-items:center;justify-content:center;width:25px;height:25px;border-radius:50%;background:rgba(13,18,24,.82);color:white;font-size:12px;line-height:1}
#rkk-social-unified .rkk-ig-fallback{font-size:11px;letter-spacing:.05em}
#rkk-social-unified .rkk-post-copy{min-width:0;display:grid;gap:5px}
#rkk-social-unified .rkk-post-meta{color:#78828c;font-size:10px;font-weight:500;letter-spacing:.01em}
#rkk-social-unified .rkk-post-title{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;color:#202830;font-size:14px;font-weight:800;line-height:1.3;overflow-wrap:anywhere}
#rkk-social-unified .rkk-post-excerpt{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:12px;line-height:1.45;font-weight:400;color:#5e6a76;overflow-wrap:anywhere}
#rkk-social-unified .rkk-post-link{font-size:11px;font-weight:800}
#rkk-social-unified .rkk-channel-footer{margin-top:15px;padding-top:13px;border-top:1px solid #eceff2;align-self:end;min-width:0}
#rkk-social-unified .rkk-channel-footer>a{display:inline-block}
#rkk-social-unified .rkk-social-status{display:block;margin:10px 0 0;color:#78828c;font-size:10px;line-height:1.5;font-weight:400;overflow-wrap:anywhere}
#rkk-social-unified .rkk-social-empty{padding:20px 14px;border:1px solid #e1e5e9;border-radius:10px;color:#687681;font-size:13px;line-height:1.6;align-self:start}
@media(max-width:700px){#rkk-social-unified .rkk-grid{grid-template-columns:1fr;align-items:start}#rkk-social-unified .rkk-channel{padding:16px;grid-template-rows:auto auto auto}#rkk-social-unified .rkk-channel-head{min-height:0}#rkk-social-unified .rkk-post-list{grid-auto-rows:auto}}
@media(max-width:360px){#rkk-social-unified .rkk-ig-card{grid-template-columns:64px minmax(0,1fr);gap:10px;padding:10px}#rkk-social-unified .rkk-ig-image{width:64px;height:88px}}
@media(prefers-reduced-motion:reduce){#rkk-social-unified .rkk-post-card{transition:none}}
</style>
<div class="rkk-rule"></div><div class="rkk-kicker">KUVIA JA KUULUMISIA</div>
<h2>Seuraa Kehä-Kettuja</h2>
<div class="rkk-grid">
<section class="rkk-channel" aria-label="Instagram">
<div class="rkk-channel-head"><div><h3>Instagram</h3><p>Kolme uusinta julkaisua</p></div><a href="https://www.instagram.com/kehaketut/" target="_blank" rel="noopener noreferrer">Avaa ↗</a></div>
<div class="rkk-post-list rkk-ig-list" aria-label="Instagram-julkaisut" aria-live="polite"><div class="rkk-social-empty">Haetaan seuran julkaisuja…</div></div>
<div class="rkk-channel-footer"><a href="https://www.instagram.com/kehaketut/" target="_blank" rel="noopener noreferrer">Katso lisää Instagramissa ↗</a><small class="rkk-social-status rkk-ig-status">Julkaisut avautuvat Instagramissa.</small></div>
</section>
<section class="rkk-channel" aria-label="Facebook">
<div class="rkk-channel-head"><div><h3>Facebook</h3><p>Seuran tiedotteet ja kuulumiset</p></div><a href="https://www.facebook.com/160875127258478/" target="_blank" rel="noopener noreferrer">Avaa ↗</a></div>
<div class="rkk-post-list rkk-fb-list" aria-label="Facebook-julkaisut" aria-live="polite"><div class="rkk-social-empty">Haetaan seuran julkaisuja…</div></div>
<div class="rkk-channel-footer"><a href="https://www.facebook.com/160875127258478/" target="_blank" rel="noopener noreferrer">Katso lisää Facebookissa ↗</a><small class="rkk-social-status rkk-fb-status">Julkaisut avautuvat Facebookissa.</small></div>
</section></div>`;

  function node(tag, cls, text) {
    var n=document.createElement(tag);n.className=cls;if(text!=null)n.textContent=text;return n;
  }
  function postURL(value, network) {
    try {
      var u=new URL(value);
      if(u.protocol!=='https:' || u.username || u.password || u.port)return null;
      if(network==='instagram') {
        if(!['instagram.com','www.instagram.com'].includes(u.hostname) || !/^\/(reel|p|tv)\/[A-Za-z0-9_-]+\/$/.test(u.pathname))return null;
        return 'https://www.instagram.com'+u.pathname;
      }
      if(!['facebook.com','www.facebook.com'].includes(u.hostname) || u.pathname==='/')return null;
      return 'https://www.facebook.com'+u.pathname+u.search;
    } catch(e) {return null;}
  }
  function dateLabel(value) {
    if(!/^\d{4}-\d{2}-\d{2}$/.test(value||''))return '';
    var d=new Date(value+'T12:00:00Z');
    if(!Number.isFinite(d.getTime()) || d.toISOString().slice(0,10)!==value)return '';
    return Number(value.slice(8,10))+'.'+Number(value.slice(5,7))+'.'+value.slice(0,4);
  }
  function cardLink(url, title, network, cls) {
    var a=node('a','rkk-post-card '+cls);a.href=url;a.target='_blank';a.rel='noopener noreferrer';
    a.setAttribute('aria-label',title.slice(0,150)+' – avaa '+network+' (uusi välilehti)');
    return a;
  }
  function copyBlock(p, title, excerpt, label, suffix) {
    var copy=node('span','rkk-post-copy');
    var time=node('time','rkk-post-meta',dateLabel(p.date)+(suffix||''));time.dateTime=p.date;
    copy.append(time,node('span','rkk-post-title',title.slice(0,150)));
    if(excerpt)copy.append(node('span','rkk-post-excerpt',excerpt.slice(0,240)));
    copy.append(node('span','rkk-post-link',label));return copy;
  }
  function sorted(posts) {
    return posts.filter(function(p){return p && typeof p==='object';}).sort(function(a,b){
      return String(b.published_at||b.date||'').localeCompare(String(a.published_at||a.date||''));
    });
  }
  function statusText(selector, source, synced) {
    var sync=dateLabel(String(synced||'').slice(0,10));
    host.querySelector(selector).textContent='Lähde: '+source+(sync?' · päivitetty '+sync:'')+'.';
  }
  function fail(selector, network) {
    host.querySelector(selector).replaceChildren(node('div','rkk-social-empty',
      'Julkaisunostot eivät juuri nyt lataudu. Kaikki julkaisut löydät alla olevasta '+network+'-linkistä.'));
  }
  function renderInstagram(d) {
    if(!d || d.brand_id!==7632678 || d.instagram_username!=='kehaketut' || !Array.isArray(d.posts))throw Error('Wrong Instagram feed');
    var seen=new Set(), cards=[];
    sorted(d.posts).some(function(p){
      var url=postURL(p.url,'instagram');
      if(!url || !dateLabel(p.date) || seen.has(url) || typeof p.title!=='string' || !p.title.trim())return false;
      seen.add(url);
      var a=cardLink(url,p.title,'Instagramissa','rkk-ig-card');
      var image=node('span','rkk-ig-image');image.setAttribute('aria-hidden','true');
      image.append(node('span','rkk-ig-fallback',p.type==='REEL'?'REEL':'KUVA'));
      var code=new URL(url).pathname.split('/')[2];
      if(p.thumbnail==='assets/instagram/'+code+'.jpg'){
        var img=document.createElement('img');img.alt='';img.loading='lazy';img.decoding='async';img.width=88;img.height=96;img.referrerPolicy='no-referrer';
        img.onerror=function(){this.remove();};img.src=BASE+p.thumbnail;image.append(img);
      }
      if(p.type==='REEL')image.append(node('span','rkk-ig-play','▶'));
      a.append(image,copyBlock(p,p.title,typeof p.excerpt==='string'?p.excerpt:'',p.type==='REEL'?'Katso Instagramissa ↗':'Avaa julkaisu ↗',p.type==='REEL'?' · REEL':''));
      cards.push(a);return cards.length===3;
    });
    if(!cards.length){fail('.rkk-ig-list','Instagram');return;}
    host.querySelector('.rkk-ig-list').replaceChildren.apply(host.querySelector('.rkk-ig-list'),cards);
    statusText('.rkk-ig-status','@kehaketut',d.synced_at);
  }
  function renderFacebook(d) {
    if(!d || d.brand_id!==7632678 || d.facebook_page_id!=='160875127258478' || !Array.isArray(d.posts))throw Error('Wrong Facebook feed');
    var seen=new Set(), cards=[];
    sorted(d.posts).some(function(p){
      var url=postURL(p.url,'facebook');
      if(!url || !dateLabel(p.date) || seen.has(url) || typeof p.text!=='string' || !p.text.trim())return false;
      seen.add(url);
      var text=p.text.trim(), lines=text.split(/\r?\n+/).filter(function(line){return line.trim();});
      var title=lines[0].trim(), excerpt=lines.slice(1).join(' ').replace(/\s+/g,' ').trim();
      var a=cardLink(url,title,'Facebookissa','rkk-fb-card');
      a.append(copyBlock(p,title,excerpt,'Lue Facebookissa ↗',''));
      cards.push(a);return cards.length===3;
    });
    if(!cards.length){fail('.rkk-fb-list','Facebook');return;}
    host.querySelector('.rkk-fb-list').replaceChildren.apply(host.querySelector('.rkk-fb-list'),cards);
    statusText('.rkk-fb-status','Kehä-Ketut',d.synced_at);
  }
  function load(file, render, selector, network) {
    var controller=new AbortController(), timer=setTimeout(function(){controller.abort();},8000);
    fetch(BASE+file+'?v='+Math.floor(Date.now()/300000),{cache:'no-store',credentials:'omit',signal:controller.signal})
      .then(function(r){if(!r.ok)throw Error('Social feed unavailable');return r.json();})
      .then(render).catch(function(){fail(selector,network);}).finally(function(){clearTimeout(timer);});
  }
  // Independent feeds: one unavailable channel must not hide the other.
  // Both share intrinsic grid layout; no iframe viewport or height message loop.
  load('instagram.json',renderInstagram,'.rkk-ig-list','Instagram');
  load('facebook.json',renderFacebook,'.rkk-fb-list','Facebook');
})();
