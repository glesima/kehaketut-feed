/* RKK social channels v2: two aligned columns in ONE Yhdistysavain section */
(function(){
"use strict";
var host=document.getElementById("rkk-social-unified");
if(!host || host.dataset.initialized==="1")return;
host.dataset.initialized="1";
host.innerHTML=String.raw`
<style>
#rkk-social-unified{--rk-red:#b91c2b;--rk-ink:#171a1f;--rk-muted:#687681;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;max-width:1160px;margin:24px auto 32px;color:var(--rk-ink);line-height:1.5}
#rkk-social-unified *{box-sizing:border-box}
#rkk-social-unified .rkk-rule{height:2px;margin:0 0 29px;background:linear-gradient(90deg,transparent,#d6dbe0 13%,#d6dbe0 46%,#b91c2b 46%,#b91c2b 54%,#d6dbe0 54%,#d6dbe0 87%,transparent)}
#rkk-social-unified .rkk-kicker{font-size:11px;font-weight:850;letter-spacing:.14em;color:#a7192b}
#rkk-social-unified h2{font-size:clamp(26px,3vw,32px);letter-spacing:-.02em;line-height:1.15;margin:5px 0 22px;font-weight:850;color:#171a1f}
#rkk-social-unified .rkk-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start;gap:16px}
#rkk-social-unified .rkk-channel{min-width:0;border:1px solid #e2e5e9;border-radius:14px;background:#fff;padding:19px 18px}
#rkk-social-unified .rkk-channel-head{display:flex;justify-content:space-between;align-items:start;gap:8px;min-height:76px;padding-bottom:12px;border-bottom:1px solid #eceff2;margin-bottom:14px}
#rkk-social-unified .rkk-channel h3{font-size:21px!important;line-height:1.2!important;font-weight:850!important;margin:0 0 6px!important;color:#171a1f!important}
#rkk-social-unified .rkk-channel p{margin:0;color:var(--rk-muted);font-size:12px;line-height:1.6}
#rkk-social-unified a{font-size:12px;font-weight:800;color:#a7192b!important;text-decoration:none!important;white-space:nowrap}
#rkk-social-unified a:focus-visible{outline:3px solid #b91c2b;outline-offset:4px}
#rkk-social-unified .juicer-feed{max-width:100%;min-height:160px;overflow:hidden}
#rkk-social-unified iframe{display:block;width:100%;height:530px;border:0;background:transparent}
@media(max-width:700px){
#rkk-social-unified .rkk-grid{grid-template-columns:1fr}
#rkk-social-unified .rkk-channel{padding:16px}
#rkk-social-unified .rkk-channel-head{min-height:0}
}
</style>
<div class="rkk-rule"></div>
<div class="rkk-kicker">KUVIA JA KUULUMISIA</div>
<h2>Seuraa Kehä-Kettuja</h2>
<div class="rkk-grid">
<section class="rkk-channel" aria-label="Instagram">
<div class="rkk-channel-head"><div><h3>Instagram</h3><p>Uusimmat kuvat ja julkaisut</p></div>
<a href="https://www.instagram.com/kehaketut/" target="_blank" rel="noopener noreferrer">Avaa ↗</a></div>
<div class="juicer-feed" data-feed-id="my-feed-1c928928-458e-4481-830b-2fe7fb9c430e"></div>
</section>
<section class="rkk-channel" aria-label="Facebook">
<div class="rkk-channel-head"><div><h3>Facebook</h3><p>Seuran tiedotteet ja kuulumiset</p></div>
<a href="https://www.facebook.com/160875127258478/" target="_blank" rel="noopener noreferrer">Avaa ↗</a></div>
<iframe id="rkk-social-facebook-frame" loading="lazy" scrolling="no"
title="Kehä-Kettujen Facebook-julkaisut"
src="https://glesima.github.io/kehaketut-feed/facebook.html?embed=1"></iframe>
</section>
</div>
`;
var frame=document.getElementById("rkk-social-facebook-frame");
window.addEventListener("message",function(e){
 if(!frame || e.origin!=="https://glesima.github.io" || e.source!==frame.contentWindow)return;
 if(!e.data || e.data.type!=="RKK_WIDGET_HEIGHT" || e.data.view!=="facebook")return;
 var h=Number(e.data.height);
 if(h>70 && h<2000)frame.style.height=Math.ceil(h+12)+"px";
});
if(!document.querySelector('script[data-rkk-juicer-v2]')){
 var js=document.createElement("script");
 js.dataset.rkkJuicerV2="1";
 js.src="https://www.juicer.io/embed/my-feed-1c928928-458e-4481-830b-2fe7fb9c430e/embed-code.js";
 js.async=true;
 js.defer=true;
 host.appendChild(js);
}
})();
